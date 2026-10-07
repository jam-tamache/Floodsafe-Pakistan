import os
import re
import time
from flask import Flask, abort, jsonify, render_template, request
import requests
import csv
from markupsafe import Markup, escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_city_coordinates():
    """Reads city_coordinates.csv for the Leaflet map.
    This is display data only (name, lat, lon, profile). It is not used
    in any risk calculation.
    """
    cities = []
    try:
        with open(os.path.join(BASE_DIR, "city_coordinates.csv"), newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("status") != "OK":
                    continue  # skip rows not marked OK
                cities.append({
                    "city": row["city"],
                    "profile_key": row["profile_key"],
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"]),
                })
    except FileNotFoundError:
        pass  # the map route handles an empty list
    return cities


CITY_COORDINATES = load_city_coordinates()

# city -> (lat, lon), built once at startup so the result page can place
# a marker without re-reading the CSV. Keys are lowercase to match
# normalize_city().
_CITY_COORDS_LOOKUP = {c["city"]: (c["lat"], c["lon"]) for c in CITY_COORDINATES}
from dotenv import load_dotenv
from translations import get_translation, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
import elevation_data

# Back-test case data for the /back-test pages. If the file is missing,
# the site still runs and /back-test just shows no cases.
try:
    from backtest_cases import ALL_CASES as BACKTEST_CASES
except ImportError:
    BACKTEST_CASES = []


# Returns case[field] in the chosen language. Falls back to English if a
# translation is missing or backtest_cases.py has no case_text().
def _case_text(case, field, lang):
    return case.get(field)


try:
    from backtest_cases import case_text as _case_text  # noqa: F811
except ImportError:
    pass

load_dotenv()  # reads variables from the .env file

app = Flask(__name__)

# ---- Regional terrain-based rainfall risk profiles ----
#
# The low_max / medium_max values are project-defined scenario thresholds,
# not official PMD or NDMA numbers. See METHODOLOGY.md for how they were
# chosen. Do not describe them as official anywhere.
#
# Scope: Sindh. Only Sindh is supported for V1. A few non-Sindh cities are
# kept for the map only (see MAP_ONLY_CITIES).
#
# The profile labels (e.g. "Mega-Urban & Coastal") are lookup keys in
# translations.py. Do not rename them without updating that file.

REGIONAL_PROFILES = {
    "mega_urban_coastal": {
        "label": "Mega-Urban & Coastal",
        "cities": [
            "karachi", "hyderabad", "badin", "thatta"
        ],
        "low_max": 40, "medium_max": 100,
        "color": "#28a745",
    },
    "central_plains": {
        "label": "Central Agricultural Plains",
        "cities": [
            "sukkur", "larkana", "nawabshah", "khairpur", "dadu", "ghotki",
            "moro", "sakrand", "kotri", "mirpurkhas", "shikarpur", "jamshoro",
            "naushahro feroze", "tando allahyar", "tando muhammad khan",
            "kashmore", "ranipur", "rohri", "shahdadkot", "matiari"
        ],
        "low_max": 50, "medium_max": 120,
        "color": "#28a745",
    },
    "arid_plains_desert": {
        "label": "Arid Plains & Deserts",
        "cities": [
            "jacobabad", "mithi", "umerkot", "sanghar"
        ],
        "low_max": 70, "medium_max": 140,
        "color": "#dc3545",
    },
}
# The old "mountainous_rugged" profile was removed. Its only cities were
# in Balochistan, not Sindh.

# Cities shown on the map for context only. They are not part of the Sindh
# model and must never get a risk score. get_profile() refuses them.
MAP_ONLY_CITIES = {
    "lahore", "islamabad", "peshawar", "quetta",
    "gwadar", "pasni", "turbat", "sibi", "chaman", "cholistan",
}

# city -> profile_key lookup, built once at startup
_CITY_TO_PROFILE = {}
for _key, _profile in REGIONAL_PROFILES.items():
    for _city in _profile["cities"]:
        _CITY_TO_PROFILE[_city] = _key


def normalize_city(city):
    """Lowercase, trim spaces, and drop a trailing country code like ',PK'."""
    if not city:
        return ""
    city = city.strip().lower()
    if "," in city:
        city = city.split(",")[0].strip()
    city = " ".join(city.split())  # collapse extra spaces
    return city


class MapOnlyCityError(Exception):
    """Raised when a risk check is attempted for a map-only city."""
    pass


class UnsupportedCityError(Exception):
    """Raised for a city that is not scored and not map-only.
    There is no fallback profile. An unknown city is refused, not guessed.
    """
    pass


def get_profile(city):
    normalized = normalize_city(city)
    if normalized in MAP_ONLY_CITIES:
        raise MapOnlyCityError(city)
    if normalized not in _CITY_TO_PROFILE:
        raise UnsupportedCityError(city)
    profile_key = _CITY_TO_PROFILE[normalized]
    return REGIONAL_PROFILES[profile_key]


# ---- Elevation scoring ----
#
# Each city's elevation is scored against the other cities in its own
# region, not on one national scale. The min and max per region are
# computed once at startup from the loaded elevation data.
#
# If elevation data is missing for a city, elevation_component() returns
# (0, False) and the score uses rainfall only. The result page says so.

_REGION_ELEVATION_RANGES = {}  # profile_key -> (min_m, max_m)


def _build_region_ranges():
    for profile_key, profile in REGIONAL_PROFILES.items():
        elevations = []
        for city in profile["cities"]:
            e = elevation_data.get_elevation(city)
            if e is not None:
                elevations.append(e)
        if elevations:
            _REGION_ELEVATION_RANGES[profile_key] = (min(elevations), max(elevations))


_build_region_ranges()

ELEVATION_COMPONENT_MAX = 30
# Documentation only: rainfall_component() hardcodes its own values.
# The real rainfall ceiling is about 54, so the max total score is about
# 84 out of 100, not 100.
RAINFALL_COMPONENT_MAX = 54

# Rainfall points below this count as "dry" for wording only. It does not
# change the score. It decides three things, through is_dry_conditions():
#   1. the "terrain baseline" sentence in build_plain_explanation()
#   2. whether the terrain warning text is shown
#   3. whether the rain-event safety tips are shown
RAINFALL_NEGLIGIBLE_THRESHOLD = 2.0


def is_dry_conditions(rain_pts):
    """True when rainfall is negligible. Takes points, not mm, so it
    scales with each region's own low_max.
    """
    return rain_pts < RAINFALL_NEGLIGIBLE_THRESHOLD


def elevation_component(city, profile_key):
    """Returns (points_0_to_30, elevation_was_used, elevation_m_or_None).

    This is the raw terrain-position score. The lowest city in its region
    gets 30 points and the highest gets 0. If a region has only one
    elevation value, it returns the midpoint (15).

    It knows nothing about rainfall on purpose. The rainfall scaling
    happens in _compute_risk_core().
    """
    normalized = normalize_city(city)
    elevation_m = elevation_data.get_elevation(normalized)

    if elevation_m is None:
        return 0, False, None

    region_range = _REGION_ELEVATION_RANGES.get(profile_key)
    if region_range is None:
        return 0, False, elevation_m

    region_min, region_max = region_range
    if region_max == region_min:
        return ELEVATION_COMPONENT_MAX / 2, True, elevation_m

    # lowest elevation in the region -> full points
    fraction_high_ground = (elevation_m - region_min) / (region_max - region_min)
    points = ELEVATION_COMPONENT_MAX * (1 - fraction_high_ground)
    return round(points, 1), True, elevation_m


def rainfall_component(rainfall_mm, profile):
    """Returns rainfall's points for the total score, scaled to this
    region's low_max and medium_max.

    - up to low_max: 0 to 25 points
    - low_max to medium_max: 25 to 50 points
    - above medium_max: 50 rising toward 54, reaching it at 2x medium_max
      (the "dead zone" described in METHODOLOGY.md)

    Rounding to 1 decimal here is fine. An earlier boundary bug came from
    rounding the final score before classifying it, not from this
    function (see _compute_risk_core).
    """
    low_max = profile["low_max"]
    medium_max = profile["medium_max"]

    if rainfall_mm <= low_max:
        fraction = rainfall_mm / low_max if low_max > 0 else 0
        return round(25 * fraction, 1)
    elif rainfall_mm <= medium_max:
        fraction = (rainfall_mm - low_max) / (medium_max - low_max)
        return round(25 + 25 * fraction, 1)
    else:
        # full saturation at 2x medium_max, see METHODOLOGY.md
        excess_range = medium_max
        fraction = min((rainfall_mm - medium_max) / excess_range, 1) if excess_range > 0 else 1
        return round(50 + 4 * fraction, 1)


# ---- Risk tiers: 4 tiers on a 0-1 scale ----
#
# RISK_SLUGS gives the CSS class for each tier. It is set here in Python
# because deriving it from the label broke "Very High Risk".
RISK_SLUGS = {
    "Low Risk": "low",
    "Moderate Risk": "moderate",
    "High Risk": "high",
    "Very High Risk": "very-high",
}

# One color table for the result pages and the map cache.
RISK_COLORS = {
    "Low Risk": "#28a745",
    "Moderate Risk": "#ffc107",
    "High Risk": "#fd7e14",
    "Very High Risk": "#dc3545",
}


def score_to_risk_key(score_0_1):
    if score_0_1 <= 0.25:
        return "Low Risk"
    elif score_0_1 <= 0.50:
        return "Moderate Risk"
    elif score_0_1 <= 0.75:
        return "High Risk"
    else:
        return "Very High Risk"


def _compute_risk_core(city, rainfall_mm):
    """Scoring only, no translations, so results can be cached and reused
    in all three languages. Raises MapOnlyCityError or UnsupportedCityError.

    Two fixes are built in here:

    1. Rounding. The tier is chosen from the unrounded score. Rounding
       first turned 0.254 into 0.25 and wrongly gave Low Risk.

    2. Elevation. A low-lying city used to score Moderate even at 0 mm of
       rain. Elevation points are now multiplied by
       min(rainfall_mm / low_max, 1.0), so at 0 mm elevation adds nothing.
       See METHODOLOGY.md.

    Both values are returned: "elevation_terrain_points" (raw, describes
    the city) and "elevation_points" (rain-scaled, what was added to the
    total).
    """
    normalized = normalize_city(city)
    profile = get_profile(city)
    profile_label = profile["label"]
    profile_key = _CITY_TO_PROFILE[normalized]

    rain_pts = rainfall_component(rainfall_mm, profile)
    elev_terrain_pts, elevation_used, elevation_m = elevation_component(city, profile_key)

    low_max = profile["low_max"]
    elevation_rain_fraction = min(rainfall_mm / low_max, 1.0) if low_max > 0 else 1.0
    elev_pts = round(elev_terrain_pts * elevation_rain_fraction, 1)

    total_score = round(rain_pts + elev_pts, 1)   # 0-100 scale

    raw_score_0_1 = total_score / 100             # unrounded, used to classify
    risk_key = score_to_risk_key(raw_score_0_1)
    score_0_1 = round(raw_score_0_1, 2)           # rounded for display only

    return {
        "profile_key": profile_key,
        "profile_label": profile_label,
        "rainfall_mm": rainfall_mm,
        "rainfall_points": rain_pts,
        "elevation_points": elev_pts,                     # rain-scaled, added to the total
        "elevation_terrain_points": elev_terrain_pts,      # raw terrain position
        "elevation_rain_fraction": elevation_rain_fraction,
        "elevation_used": elevation_used,
        "elevation_m": elevation_m,
        "dry_conditions": is_dry_conditions(rain_pts),
        "score": total_score,                # 0-100, shown in "How is this calculated?"
        "score_0_1": score_0_1,              # drives the gauge
        "risk_level_key": risk_key,
        "risk_slug": RISK_SLUGS[risk_key],
        "risk_color": RISK_COLORS[risk_key],
    }


# Sorted city names for the home page dropdown, built from
# REGIONAL_PROFILES so it always matches the model. Map-only cities are
# left out because they cannot be scored.
SUPPORTED_CITY_DISPLAY_NAMES = sorted({
    city.title() for profile in REGIONAL_PROFILES.values() for city in profile["cities"]
})


def localized_city(city, t):
    """City name in the active language from translations.py's city_names.
    Falls back to the English title-cased name if there is no entry.
    """
    return t.get("city_names", {}).get(normalize_city(city), city.title())


def get_lang():
    """Reads ?lang= from the URL, falls back to English."""
    lang = request.args.get("lang", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    return lang


def build_plain_explanation(rainfall_mm, elevation_used, elev_terrain_pts, rain_pts, risk_key, city, risk_level_display, t):
    """One plain-language sentence explaining why the score came out as it
    did. The detailed breakdown is behind the "How is this calculated?"
    toggle in check.html.

    elev_terrain_pts must be the raw terrain score, not the rain-scaled
    one, because this sentence describes geography and geography does not
    change on a dry day.

    The first branch ("terrain baseline") is for a Moderate or higher
    score with almost no rain. After the elevation scaling fix it should
    rarely happen, so it is kept only as a safety net.
    """
    if elevation_used and is_dry_conditions(rain_pts) and risk_key != "Low Risk":
        position_key = (
            "elevation_position_low"
            if elev_terrain_pts >= (ELEVATION_COMPONENT_MAX / 2)
            else "elevation_position_high"
        )
        return t["explanation_terrain_baseline"].format(
            rainfall=rainfall_mm, city=localized_city(city, t),
            elevation_position=t[position_key], risk_level=risk_level_display,
        )
    elif elevation_used:
        position_key = (
            "elevation_position_low"
            if elev_terrain_pts >= (ELEVATION_COMPONENT_MAX / 2)
            else "elevation_position_high"
        )
        return t["explanation_with_elevation"].format(
            rainfall=rainfall_mm, city=localized_city(city, t),
            elevation_position=t[position_key], risk_level=risk_level_display,
        )
    else:
        return t["explanation_without_elevation"].format(
            rainfall=rainfall_mm, city=localized_city(city, t), risk_level=risk_level_display,
        )


def check_risk(rainfall_mm, city, t):
    """Builds the full result for one city and rainfall total, in the
    language of the translation dict t. Raises MapOnlyCityError or
    UnsupportedCityError, so callers must catch both.

    When conditions are dry, the terrain warning is empty and generic
    preparedness tips replace the storm tips. The score and tier do not
    change. check.html must handle an empty terrain_warning.

    elevation_note uses the rain-scaled elevation points.
    """
    core = _compute_risk_core(city, rainfall_mm)
    profile_label = core["profile_label"]
    rain_pts = core["rainfall_points"]
    elev_pts = core["elevation_points"]                     # rain-scaled, matches the breakdown
    elev_terrain_pts = core["elevation_terrain_points"]      # raw terrain position
    elevation_used = core["elevation_used"]
    elevation_m = core["elevation_m"]
    total_score = core["score"]
    score_0_1 = core["score_0_1"]
    risk_key = core["risk_level_key"]
    risk_slug = core["risk_slug"]
    dry_conditions = core["dry_conditions"]

    if elevation_used:
        # points and max_points tell the reader the bar is points, not meters
        elevation_note = t["elevation_note_available"].format(
            city=localized_city(city, t), elevation=elevation_m, profile=t["terrain_profile_labels"][profile_label],
            points=elev_pts, max_points=ELEVATION_COMPONENT_MAX,
        )
    else:
        elevation_note = t["elevation_note_unavailable"].format(city=localized_city(city, t))

    risk_level_display = t["risk_levels"][risk_key]
    plain_explanation = build_plain_explanation(
        rainfall_mm, elevation_used, elev_terrain_pts, rain_pts, risk_key, city, risk_level_display, t
    )

    return {
        "risk_level_key": risk_key,   # for translation lookups
        "risk_slug": risk_slug,       # for the CSS class
        "risk_level": risk_level_display,
        "plain_explanation": plain_explanation,
        "rainfall": rainfall_mm,
        "score": total_score,
        "score_0_1": score_0_1,
        "rainfall_points": rain_pts,
        "elevation_points": elev_pts,
        "elevation_terrain_points": elev_terrain_pts,
        "elevation_used": elevation_used,
        "elevation_note": elevation_note,
        "dry_conditions": dry_conditions,
        "safety_tips_note": t["safety_tips_dry_note"] if dry_conditions else "",
        "safety_tips": t["safety_tips_dry"] if dry_conditions else t["safety_tips"][risk_key],
        "shelter_message": t["shelter_message"],
        "terrain_profile": t["terrain_profile_labels"][profile_label],
        "terrain_warning": "" if dry_conditions else t["terrain_warnings"][profile_label],
        "risk_color": core["risk_color"],
    }


def sanitize_rainfall(raw_value):
    """Returns (valid, value_or_none)."""
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return False, None
    if value < 0:
        return False, None
    return True, value


def check_city_exists_in_pakistan(city):
    """Checks that the city is a real place in Pakistan, using
    OpenWeatherMap as a lookup only. No weather data is read or kept.

    Returns (is_valid, error_reason). error_reason is one of
    "missing_api_key", "timeout", "network_error", "not_found",
    "not_pakistan", "malformed_response", or None if valid.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return False, "missing_api_key"

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},PK&appid={api_key}&units=metric"
    )
    try:
        response = requests.get(url, timeout=8)
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.RequestException:
        return False, "network_error"

    try:
        data = response.json()
    except ValueError:
        return False, "malformed_response"

    if data.get("cod") != 200:
        return False, "not_found"

    country = data.get("sys", {}).get("country")
    if country != "PK":
        return False, "not_pakistan"

    return True, None


def get_forecast_rainfall(city, hours=72):
    """Gets forecast rainfall (mm) for the next `hours` hours from
    OpenWeatherMap's 5-day/3-hour forecast, looked up by city name. It
    also checks the city is in Pakistan. Used for /forecast, where the
    city is typed by the visitor.

    Returns (is_valid, rainfall_mm_or_None, error_reason_or_None).

    This endpoint differs from the current-weather one: "cod" is a string
    and the country is under data["city"]["country"].
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return False, None, "missing_api_key"

    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city},PK&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=8)
    except requests.exceptions.Timeout:
        return False, None, "timeout"
    except requests.exceptions.RequestException:
        return False, None, "network_error"

    try:
        data = response.json()
    except ValueError:
        return False, None, "malformed_response"

    if str(data.get("cod")) != "200":
        return False, None, "not_found"

    country = data.get("city", {}).get("country")
    if country != "PK":
        return False, None, "not_pakistan"

    cutoff = time.time() + hours * 3600
    total_rainfall = 0.0
    for entry in data.get("list", []):
        entry_time = entry.get("dt")
        if entry_time is None or entry_time > cutoff:
            continue
        total_rainfall += entry.get("rain", {}).get("3h", 0.0)

    return True, round(total_rainfall, 1), None


def get_forecast_rainfall_by_coords(lat, lon, hours=72):
    """Same as get_forecast_rainfall(), but looked up by coordinates.
    Used for the map cache. OpenWeatherMap's name search misses some
    smaller Sindh towns (Mirpurkhas, Umerkot and others), and every city
    in CITY_COORDINATES already has verified coordinates.

    There is no country check because the coordinates are all in Pakistan.
    /result and /forecast still use the name-based lookups.

    Returns (is_valid, rainfall_mm_or_None, error_reason_or_None).
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return False, None, "missing_api_key"

    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=8)
    except requests.exceptions.Timeout:
        return False, None, "timeout"
    except requests.exceptions.RequestException:
        return False, None, "network_error"

    try:
        data = response.json()
    except ValueError:
        return False, None, "malformed_response"

    if str(data.get("cod")) != "200":
        return False, None, "not_found"

    cutoff = time.time() + hours * 3600
    total_rainfall = 0.0
    for entry in data.get("list", []):
        entry_time = entry.get("dt")
        if entry_time is None or entry_time > cutoff:
            continue
        total_rainfall += entry.get("rain", {}).get("3h", 0.0)

    return True, round(total_rainfall, 1), None


def _render_risk_result(result, city, rainfall, mode, t, lang, forecast_hours=None):
    """Shared render for /result (scenario) and /forecast. `mode` decides
    whether the note says the rainfall was forecast or hypothetical.
    """
    if mode == "forecast":
        source_note = t["source_forecast"].format(hours=forecast_hours, mm=rainfall)
    else:
        source_note = t["source_scenario"].format(mm=rainfall)

    # Coordinates for the result-page map. If the city is not in the CSV,
    # these are None and check.html skips the map.
    coords = _CITY_COORDS_LOOKUP.get(normalize_city(city))
    city_lat, city_lon = coords if coords else (None, None)

    return render_template(
        "check.html", t=t, lang=lang,
        city=city, city_display=localized_city(city, t),
        rainfall=rainfall, mode=mode, source_note=source_note,
        plain_explanation=result["plain_explanation"],
        safety_tips=result["safety_tips"], shelter_message=result["shelter_message"],
        risk_level=result["risk_level"], risk_level_key=result["risk_level_key"],
        risk_slug=result["risk_slug"],
        terrain_profile=result["terrain_profile"], terrain_warning=result["terrain_warning"],
        dry_conditions=result["dry_conditions"],
        safety_tips_note=result["safety_tips_note"],
        elevation_used=result["elevation_used"],
        risk_color=result["risk_color"],
        score=result["score"], score_0_1=result["score_0_1"],
        rainfall_points=result["rainfall_points"],
        elevation_points=result["elevation_points"], elevation_note=result["elevation_note"],
        city_lat=city_lat, city_lon=city_lon,
    )


@app.route("/")
def home():
    lang = get_lang()
    t = get_translation(lang)
    return render_template("index.html", t=t, lang=lang, cities=SUPPORTED_CITY_DISPLAY_NAMES)


@app.route("/about")
def about():
    lang = get_lang()
    t = get_translation(lang)
    return render_template("about.html", t=t, lang=lang)


@app.route("/floods-2022")
def floods_2022():
    """Sourced page on the 2022 floods, linked from About. Not in the nav.
    English only for now. The endpoint name must stay "floods_2022"
    because about.html uses url_for('floods_2022').
    """
    lang = get_lang()
    t = get_translation(lang)
    return render_template("floods_2022.html", t=t, lang=lang)


@app.route("/how-it-works")
def how_it_works():
    lang = get_lang()
    t = get_translation(lang)
    return render_template("how_it_works.html", t=t, lang=lang)


@app.route("/data-methodology")
def data_methodology():
    """The region thresholds come straight from REGIONAL_PROFILES, so the
    page cannot disagree with the code. Order matches METHODOLOGY.md.
    """
    lang = get_lang()
    t = get_translation(lang)
    regions_for_template = [
        {
            "label": profile["label"],
            "low_max": profile["low_max"],
            "medium_max": profile["medium_max"],
        }
        for profile in REGIONAL_PROFILES.values()
    ]
    return render_template("data_methodology.html", t=t, lang=lang, regions=regions_for_template)


# Turns plain-text source strings with URLs into safe clickable links.
# Jinja's urlize swallowed the closing ")" and ";" into the link, so this
# stops each URL at whitespace or ")". Each link is wrapped in <bdi> so a
# left-to-right URL does not scramble Urdu/Sindhi (right-to-left) text.
_URL_RE = re.compile(r"https?://[^\s)<>\"]+")


@app.template_filter("linkify")
def linkify(text):
    text = text or ""
    parts, last = [], 0
    for m in _URL_RE.finditer(text):
        parts.append(escape(text[last:m.start()]))
        url = m.group(0).rstrip(".,;:")
        parts.append(Markup('<bdi><a href="{0}" target="_blank" rel="noopener">{0}</a></bdi>').format(url))
        parts.append(escape(m.group(0)[len(url):]))
        last = m.end()
    parts.append(escape(text[last:]))
    return Markup("").join(parts)


# ---- Historical back-test ----
#
# /back-test lists every case in backtest_cases.py with the model's score
# and outcome. /back-test/<case_id> shows one case. Scores come from the
# same _compute_risk_core() as the live tool. All cases are shown,
# including false alarms and the skipped Jacobabad case. Never filter
# the list down to the hits.
#
# An "alert" is Moderate Risk or higher. This must match run_backtest.py.
BACKTEST_ALERT_TIERS = {"Moderate Risk", "High Risk", "Very High Risk"}

# Baseline from BACKTEST_PROTOCOL.md section 7: alert if 72h rainfall is
# at least this many mm, with no terrain logic. This value is typed here,
# not read from the file, so re-check it if the protocol ever changes.
BACKTEST_BASELINE_MM = 50.0

_BACKTEST_OUTCOME_KEYS = ["HIT", "MISS", "FALSE ALARM", "CORRECT (quiet)"]

# CSS class for each outcome badge
_BACKTEST_BADGE_CLASS = {
    "HIT": "risk-low",
    "CORRECT (quiet)": "risk-low",
    "FALSE ALARM": "risk-high",
    "MISS": "risk-very-high",
}


def _classify_backtest(actual_flood, alerted):
    if actual_flood and alerted:
        return "HIT"
    if actual_flood:
        return "MISS"
    if alerted:
        return "FALSE ALARM"
    return "CORRECT (quiet)"


def evaluate_backtest_case(case):
    """Scores one back-test case and returns a dict. If the case has no
    rainfall figure (Jacobabad), core is None and outcome is "SKIPPED".
    """
    actual_flood = case["actual_outcome"] == "flood"
    rainfall = case["rainfall_mm"]
    row = {
        "id": case["id"],
        "name": f"{case['city'].title()}, {case['date_window']}",
        "actual_flood": actual_flood,
        "rainfall_mm": rainfall,
        "has_caveat": bool(case.get("rainfall_caveat")),
        "scored": rainfall is not None,
        "core": None,
        "outcome": "SKIPPED",
        "baseline_outcome": "SKIPPED",
    }
    if rainfall is None:
        return row
    core = _compute_risk_core(case["city"], rainfall)
    row["core"] = core
    row["outcome"] = _classify_backtest(actual_flood, core["risk_level_key"] in BACKTEST_ALERT_TIERS)
    row["baseline_outcome"] = _classify_backtest(actual_flood, rainfall >= BACKTEST_BASELINE_MM)
    return row


@app.route("/back-test")
def back_test():
    """Back-test results page: verdict, results table (each row links to
    its case), baseline comparison, deviations and limitations. Strings
    are under t["bt"] in translations.py. The verdict and limitation text
    in templates/backtest.html comes from BACKTEST_RESULTS.md, so update
    it if the cases or protocol change.
    """
    lang = get_lang()
    t = get_translation(lang)
    rows = [evaluate_backtest_case(c) for c in BACKTEST_CASES]
    scored = [r for r in rows if r["scored"]]
    model_totals = {k: sum(1 for r in scored if r["outcome"] == k) for k in _BACKTEST_OUTCOME_KEYS}
    baseline_totals = {k: sum(1 for r in scored if r["baseline_outcome"] == k) for k in _BACKTEST_OUTCOME_KEYS}
    return render_template(
        "backtest.html", t=t, lang=lang, rows=rows,
        scored_count=len(scored), total_count=len(rows),
        model_totals=model_totals, baseline_totals=baseline_totals,
        baseline_mm=BACKTEST_BASELINE_MM,
    )


@app.route("/back-test/<case_id>")
def back_test_case(case_id):
    """Shows one historical case: the model's score next to what actually
    happened. An unknown id returns 404.

    case_i holds the caveat, impact and source text in the active
    language. The template must use case_i for those three fields.
    """
    lang = get_lang()
    t = get_translation(lang)
    case = next((c for c in BACKTEST_CASES if c["id"] == case_id), None)
    if case is None:
        abort(404)
    row = evaluate_backtest_case(case)
    profile = REGIONAL_PROFILES.get(case.get("profile_key"), {})
    case_i = {
        field: _case_text(case, field, lang)
        for field in ("rainfall_caveat", "impact", "source")
    }
    return render_template(
        "backtest_case.html", t=t, lang=lang, case=case, case_i=case_i, row=row,
        terrain_label=profile.get("label", ""),
        badge_class=_BACKTEST_BADGE_CLASS.get(row["outcome"]),
    )


_city_risk_cache = {}
_cache_last_refreshed = None
CACHE_TTL_SECONDS = 3600  # refresh hourly


def get_all_city_risk_data(force_refresh=False):
    """Risk data for all map cities, cached and refreshed hourly instead
    of fetched on every page view. Uses the coordinate-based forecast
    lookup, see get_forecast_rainfall_by_coords().
    """
    global _city_risk_cache, _cache_last_refreshed
    now = time.time()
    if force_refresh or _cache_last_refreshed is None or (now - _cache_last_refreshed) > CACHE_TTL_SECONDS:
        fresh = {}
        for coord in CITY_COORDINATES:
            city = coord["city"]
            entry = {**coord, "scored": False}
            try:
                forecast_valid, rainfall_mm, error_reason = get_forecast_rainfall_by_coords(
                    coord["lat"], coord["lon"]
                )
                if not forecast_valid:
                    entry["error"] = error_reason
                else:
                    entry.update(_compute_risk_core(city, rainfall_mm))
                    entry["scored"] = True
            except MapOnlyCityError:
                pass
            except UnsupportedCityError:
                entry["error"] = "unsupported_city"
            fresh[city] = entry

            if not entry.get("scored") and city.lower() not in MAP_ONLY_CITIES:
                print(f"UNSCORED: {city} -> {entry.get('error')}")
        _city_risk_cache = fresh
        _cache_last_refreshed = now
    return _city_risk_cache


@app.route("/map")
def map_view():
    lang = get_lang()
    t = get_translation(lang)
    city_data = get_all_city_risk_data()

    cities_for_template = []
    for city, entry in city_data.items():
        item = dict(entry)
        item["city_display"] = localized_city(city, t)
        if entry.get("scored"):
            item["risk_level"] = t["risk_levels"][entry["risk_level_key"]]
            # elevation_terrain_points (raw) is passed here, not the
            # rain-scaled value, so the wording describes geography.
            item["plain_explanation"] = build_plain_explanation(
                entry["rainfall_mm"], entry["elevation_used"], entry["elevation_terrain_points"],
                entry["rainfall_points"], entry["risk_level_key"], city, item["risk_level"], t
            )
        cities_for_template.append(item)

    return render_template("map.html", t=t, lang=lang, cities=cities_for_template)


@app.route("/result")
def result():
    lang = get_lang()
    t = get_translation(lang)

    city = request.args.get("city")
    rainfall_raw = request.args.get("rainfall")

    rainfall_valid, rainfall = sanitize_rainfall(rainfall_raw)
    city_valid, city_error_reason = check_city_exists_in_pakistan(city) if city else (False, "not_found")

    if not rainfall_valid and not city_valid:
        return render_template("check.html", error=t["error_both"], t=t, lang=lang)
    elif not rainfall_valid:
        return render_template("check.html", error=t["error_rainfall"], t=t, lang=lang)
    elif not city_valid:
        # TODO: city_error_reason is not shown to the user yet. All
        # failures show error_city. "Weather service is down" should be
        # told apart from "not a real city".
        return render_template("check.html", error=t["error_city"], t=t, lang=lang)

    try:
        risk_result = check_risk(rainfall, city, t)
    except MapOnlyCityError:
        # A real city outside Sindh, shown on the map only.
        return render_template("check.html", error=t["error_city_outside_coverage"], t=t, lang=lang)
    except UnsupportedCityError:
        # Passed the OpenWeatherMap check but is not in the model. Refused,
        # not guessed.
        return render_template("check.html", error=t["error_city"], t=t, lang=lang)
    else:
        return _render_risk_result(risk_result, city, rainfall, "scenario", t, lang)


@app.route("/forecast")
def forecast():
    lang = get_lang()
    t = get_translation(lang)
    city = request.args.get("city")

    if not city or not city.strip():
        return render_template("check.html", error=t["error_city"], t=t, lang=lang)

    forecast_valid, forecast_rainfall, error_reason = get_forecast_rainfall(city)

    if not forecast_valid:
        # TODO: same as /result, error_reason is not shown separately yet.
        # forecast_failed lets check.html point the user to scenario mode.
        return render_template(
            "check.html", error=t["error_city"], t=t, lang=lang,
            forecast_failed=True,
        )

    try:
        risk_result = check_risk(forecast_rainfall, city, t)
    except MapOnlyCityError:
        return render_template("check.html", error=t["error_city_outside_coverage"], t=t, lang=lang)
    except UnsupportedCityError:
        return render_template("check.html", error=t["error_city"], t=t, lang=lang)
    else:
        return _render_risk_result(risk_result, city, forecast_rainfall, "forecast", t, lang, forecast_hours=72)


if __name__ == "__main__":
    app.run()