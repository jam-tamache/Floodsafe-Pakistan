import os
import re
import time
from flask import Flask, abort, jsonify, render_template, request
import requests
import csv
from markupsafe import Markup, escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_city_coordinates():
    """Reads city_coordinates.csv. Used for the map and forecast lookups,
    never for the risk score.
    """
    cities = []
    try:
        with open(os.path.join(BASE_DIR, "city_coordinates.csv"), newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("status") != "OK":
                    continue
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

# city -> (lat, lon). Keys are lowercase, like normalize_city().
_CITY_COORDS_LOOKUP = {c["city"]: (c["lat"], c["lon"]) for c in CITY_COORDINATES}
from dotenv import load_dotenv
from translations import get_translation, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
import elevation_data

# Back-test cases. If the file is missing, /back-test shows no cases.
try:
    from backtest_cases import ALL_CASES as BACKTEST_CASES
except ImportError:
    BACKTEST_CASES = []


# Returns case[field] in the chosen language, English if none exists.
def _case_text(case, field, lang):
    return case.get(field)


try:
    from backtest_cases import case_text as _case_text  # noqa: F811
except ImportError:
    pass

load_dotenv()  # reads the .env file

app = Flask(__name__)

# ---- Regional risk profiles ----
#
# low_max and medium_max are my own scenario thresholds, not official
# PMD or NDMA numbers. See METHODOLOGY.md. Never call them official.
#
# Only Sindh is scored. The map also shows a few cities outside Sindh
# (MAP_ONLY_CITIES).
#
# The labels are keys in translations.py. Do not rename them.

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
# The old "mountainous_rugged" profile is gone. It only had Balochistan cities.

# Map only. These never get a score. get_profile() refuses them.
MAP_ONLY_CITIES = {
    "lahore", "islamabad", "peshawar", "quetta",
    "gwadar", "pasni", "turbat", "sibi", "chaman", "cholistan",
}

# city -> profile_key, built once at startup
_CITY_TO_PROFILE = {}
for _key, _profile in REGIONAL_PROFILES.items():
    for _city in _profile["cities"]:
        _CITY_TO_PROFILE[_city] = _key


def normalize_city(city):
    """Lowercase, trim spaces, drop a trailing ',PK'."""
    if not city:
        return ""
    city = city.strip().lower()
    if "," in city:
        city = city.split(",")[0].strip()
    city = " ".join(city.split())  # collapse extra spaces
    return city


class MapOnlyCityError(Exception):
    """Risk check attempted for a map-only city."""
    pass


class UnsupportedCityError(Exception):
    """City is not scored and not map-only. Unknown cities are refused,
    never guessed.
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
# A city's elevation is scored against the other cities in its own
# region. Min and max per region are computed once at startup.
#
# If a city has no elevation data, elevation_component() returns
# (0, False, None) and the score uses rainfall only.

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
# Documentation only. rainfall_component() has its own values. Rainfall
# tops out near 54, so the best possible total is about 84, not 100.
RAINFALL_COMPONENT_MAX = 54

# Rainfall points below this count as "dry". Wording only, the score
# does not change. It controls:
#   1. the "terrain baseline" sentence
#   2. the terrain warning text
#   3. the rain-event safety tips
RAINFALL_NEGLIGIBLE_THRESHOLD = 2.0


def is_dry_conditions(rain_pts):
    """True when rainfall is negligible. Takes points, not mm, so it
    fits each region's own low_max.
    """
    return rain_pts < RAINFALL_NEGLIGIBLE_THRESHOLD


def elevation_component(city, profile_key):
    """Returns (points_0_to_30, elevation_was_used, elevation_m_or_None).

    Raw terrain score: lowest city in the region gets 30, highest gets 0.
    One elevation value in a region gives the midpoint, 15. It ignores
    rainfall on purpose. Rain scaling is in _compute_risk_core().
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
    """Rainfall points, scaled to the region's low_max and medium_max.

    - up to low_max: 0 to 25
    - low_max to medium_max: 25 to 50
    - above medium_max: 50 up to 54, reached at 2x medium_max
      (the "dead zone" in METHODOLOGY.md)

    Rounding to 1 decimal is fine here. The old boundary bug came from
    rounding the final score (see _compute_risk_core).
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
        # full at 2x medium_max, see METHODOLOGY.md
        excess_range = medium_max
        fraction = min((rainfall_mm - medium_max) / excess_range, 1) if excess_range > 0 else 1
        return round(50 + 4 * fraction, 1)


# ---- Risk tiers: 4 tiers on a 0-1 scale ----
#
# RISK_SLUGS are the CSS classes. Set here because building them from
# the label broke "Very High Risk".
RISK_SLUGS = {
    "Low Risk": "low",
    "Moderate Risk": "moderate",
    "High Risk": "high",
    "Very High Risk": "very-high",
}

# One color table for result pages and the map cache.
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
    """Scoring only, no translations, so one result serves all three
    languages. Raises MapOnlyCityError or UnsupportedCityError.

    Two fixes live here:
    1. The tier uses the unrounded score. Rounding first turned 0.254
       into 0.25 and gave Low Risk by mistake.
    2. Elevation points are multiplied by min(rainfall_mm / low_max, 1),
       so at 0 mm elevation adds nothing. See METHODOLOGY.md.

    Returns both "elevation_terrain_points" (raw, describes the city)
    and "elevation_points" (rain-scaled, added to the total).
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

    raw_score_0_1 = total_score / 100             # unrounded, used for the tier
    risk_key = score_to_risk_key(raw_score_0_1)
    score_0_1 = round(raw_score_0_1, 2)           # rounded, display only

    return {
        "profile_key": profile_key,
        "profile_label": profile_label,
        "rainfall_mm": rainfall_mm,
        "rainfall_points": rain_pts,
        "elevation_points": elev_pts,                     # rain-scaled, added to total
        "elevation_terrain_points": elev_terrain_pts,      # raw terrain score
        "elevation_rain_fraction": elevation_rain_fraction,
        "elevation_used": elevation_used,
        "elevation_m": elevation_m,
        "dry_conditions": is_dry_conditions(rain_pts),
        "score": total_score,                # 0-100, shown in the breakdown
        "score_0_1": score_0_1,              # drives the gauge
        "risk_level_key": risk_key,
        "risk_slug": RISK_SLUGS[risk_key],
        "risk_color": RISK_COLORS[risk_key],
    }


# Sorted city names for the home dropdown, built from REGIONAL_PROFILES.
# Map-only cities are left out.
SUPPORTED_CITY_DISPLAY_NAMES = sorted({
    city.title() for profile in REGIONAL_PROFILES.values() for city in profile["cities"]
})


def localized_city(city, t):
    """City name in the active language, English if there is no entry."""
    return t.get("city_names", {}).get(normalize_city(city), city.title())


def get_lang():
    """Reads ?lang= from the URL, English if invalid."""
    lang = request.args.get("lang", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    return lang


def build_plain_explanation(rainfall_mm, elevation_used, elev_terrain_pts, rain_pts, risk_key, city, risk_level_display, t):
    """One plain sentence explaining the result. Details are behind the
    "How is this calculated?" toggle in check.html.

    Pass the raw terrain score, not the rain-scaled one. This sentence
    describes geography, which does not change on a dry day.

    The first branch (terrain baseline) is only a safety net now. After
    the elevation scaling fix it should rarely run.
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
    language of t. Raises MapOnlyCityError or UnsupportedCityError.

    In dry conditions the terrain warning is empty and general tips
    replace the storm tips. check.html must handle an empty
    terrain_warning. The elevation note uses the rain-scaled points.
    """
    core = _compute_risk_core(city, rainfall_mm)
    profile_label = core["profile_label"]
    rain_pts = core["rainfall_points"]
    elev_pts = core["elevation_points"]                     # rain-scaled
    elev_terrain_pts = core["elevation_terrain_points"]      # raw
    elevation_used = core["elevation_used"]
    elevation_m = core["elevation_m"]
    total_score = core["score"]
    score_0_1 = core["score_0_1"]
    risk_key = core["risk_level_key"]
    risk_slug = core["risk_slug"]
    dry_conditions = core["dry_conditions"]

    if elevation_used:
        # points and max_points show the bar is points, not meters
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
    """Checks that the city is a real place in Pakistan.

    Known cities (the 28 Sindh cities and the map-only ones) pass
    without calling OpenWeatherMap, because its name search misses some
    small Sindh towns. Any other name is looked up there. No weather
    data is read or kept.

    Returns (is_valid, error_reason). error_reason is "missing_api_key",
    "timeout", "network_error", "not_found", "not_pakistan",
    "malformed_response", or None if valid.
    """
    normalized = normalize_city(city)
    if normalized in _CITY_TO_PROFILE or normalized in MAP_ONLY_CITIES:
        return True, None

    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return False, "missing_api_key"

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": f"{city},PK", "appid": api_key, "units": "metric"},
            timeout=8,
        )
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


def _fetch_forecast_json(params):
    """Calls the OpenWeatherMap 5-day/3-hour forecast. Adds the API key.
    Returns (data_or_none, error_reason_or_none).
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return None, "missing_api_key"

    query = dict(params)
    query["appid"] = api_key
    query["units"] = "metric"

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params=query,
            timeout=8,
        )
    except requests.exceptions.Timeout:
        return None, "timeout"
    except requests.exceptions.RequestException:
        return None, "network_error"

    try:
        data = response.json()
    except ValueError:
        return None, "malformed_response"

    # "cod" is a string on this endpoint
    if str(data.get("cod")) != "200":
        return None, "not_found"

    return data, None


def _sum_forecast_rainfall(data, hours):
    """Adds up the 3-hour rain amounts in the next `hours` hours."""
    cutoff = time.time() + hours * 3600
    total_rainfall = 0.0
    for entry in data.get("list", []):
        entry_time = entry.get("dt")
        if entry_time is None or entry_time > cutoff:
            continue
        total_rainfall += entry.get("rain", {}).get("3h", 0.0)
    return round(total_rainfall, 1)


def get_forecast_rainfall_by_coords(lat, lon, hours=72):
    """Forecast rainfall (mm) for the next `hours` hours, by coordinates.
    Used for the map cache and for any city with coordinates in the CSV.
    The name search misses some small Sindh towns (Mirpurkhas, Umerkot).
    No country check, all coordinates are in Pakistan.

    Returns (is_valid, rainfall_mm_or_None, error_reason_or_None).
    """
    data, error_reason = _fetch_forecast_json({"lat": lat, "lon": lon})
    if error_reason:
        return False, None, error_reason
    return True, _sum_forecast_rainfall(data, hours), None


def get_forecast_rainfall(city, hours=72):
    """Forecast rainfall (mm) for the next `hours` hours. Used by
    /forecast.

    A city with coordinates in the CSV uses them. Any other name goes
    to the OpenWeatherMap name search, which also checks the country.
    That endpoint puts the country under data["city"]["country"].

    Returns (is_valid, rainfall_mm_or_None, error_reason_or_None).
    """
    coords = _CITY_COORDS_LOOKUP.get(normalize_city(city))
    if coords:
        return get_forecast_rainfall_by_coords(coords[0], coords[1], hours)

    data, error_reason = _fetch_forecast_json({"q": f"{city},PK"})
    if error_reason:
        return False, None, error_reason

    country = data.get("city", {}).get("country")
    if country != "PK":
        return False, None, "not_pakistan"

    return True, _sum_forecast_rainfall(data, hours), None


def _render_risk_result(result, city, rainfall, mode, t, lang, forecast_hours=None):
    """Shared render for /result and /forecast. `mode` decides whether
    the note says forecast or scenario.
    """
    if mode == "forecast":
        source_note = t["source_forecast"].format(hours=forecast_hours, mm=rainfall)
    else:
        source_note = t["source_scenario"].format(mm=rainfall)

    # Map coordinates. None if the city is not in the CSV, and
    # check.html then skips the map.
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
    """2022 floods page, linked from About, not in the nav. English only.
    Keep the endpoint name "floods_2022", about.html uses it.
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
    """Thresholds come from REGIONAL_PROFILES, so the page always
    matches the code. Order matches METHODOLOGY.md.
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


# Turns URLs in source text into safe links. Jinja's urlize pulled the
# closing ")" and ";" into the link, so each URL stops at whitespace or
# ")". <bdi> keeps a left-to-right URL from scrambling Urdu/Sindhi text.
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
# /back-test lists the cases in backtest_cases.py with the model's score
# and outcome. /back-test/<case_id> shows one case. Scores come from
# _compute_risk_core(), same as the live tool. Never hide false alarms
# or the skipped Jacobabad case.
#
# An "alert" is Moderate Risk or higher. Must match run_backtest.py.
BACKTEST_ALERT_TIERS = {"Moderate Risk", "High Risk", "Very High Risk"}

# Baseline from BACKTEST_PROTOCOL.md section 7: alert if 72h rainfall is
# at least this many mm. Typed here, not read from the file. Re-check
# it if the protocol changes.
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
    """Scores one case. With no rainfall figure (Jacobabad), core is
    None and the outcome is "SKIPPED".
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
    """Back-test page: verdict, results table, baseline comparison,
    deviations, limitations. Strings are under t["bt"] in
    translations.py. The verdict and limitation text in backtest.html
    comes from BACKTEST_RESULTS.md. Update it if the cases or protocol
    change.
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
    """One historical case: model score next to what happened. Unknown
    id gives 404. The template must use case_i for the caveat, impact
    and source text, so they show in the active language.
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
    """Risk data for all map cities. Cached, refreshed hourly. Uses
    get_forecast_rainfall_by_coords().
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
            # Pass the raw terrain points, not the rain-scaled ones, so
            # the wording describes geography.
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
        # TODO: city_error_reason is not shown yet. "Service is down"
        # should look different from "not a real city".
        return render_template("check.html", error=t["error_city"], t=t, lang=lang)

    try:
        risk_result = check_risk(rainfall, city, t)
    except MapOnlyCityError:
        # Real city outside Sindh, map only.
        return render_template("check.html", error=t["error_city_outside_coverage"], t=t, lang=lang)
    except UnsupportedCityError:
        # Real place, but not in the model. Refused, not guessed.
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
        # TODO: same as /result, error_reason is not shown yet.
        # forecast_failed lets check.html point to scenario mode.
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