import os
import time
from flask import Flask, jsonify, render_template, request
import requests
import csv

def load_city_coordinates():
    """Loads city_coordinates.csv into a list of dicts for the Leaflet map.
    Kept separate from elevation_data.py's loading since this is purely
    display data (name/lat/lon/profile), not used in any risk calculation.
    """
    cities = []
    try:
        with open("city_coordinates.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("status") != "OK":
                    continue  # skip any row not marked OK, don't guess
                cities.append({
                    "city": row["city"],
                    "profile_key": row["profile_key"],
                    "lat": float(row["lat"]),
                    "lon": float(row["lon"]),
                })
    except FileNotFoundError:
        pass  # map route below handles an empty list gracefully
    return cities


CITY_COORDINATES = load_city_coordinates()

# Flat city -> (lat, lon) lookup, built once at startup, so the result page
# can place a single marker for the checked city without re-reading the CSV
# or re-deriving anything. Keys are normalized (lowercase) to match
# normalize_city()'s output, since city names arrive from user input /
# query strings in inconsistent casing.
_CITY_COORDS_LOOKUP = {c["city"]: (c["lat"], c["lon"]) for c in CITY_COORDINATES}
from dotenv import load_dotenv
from translations import get_translation, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
import elevation_data

load_dotenv()  # reads variables from a .env file in the same folder as this script

app = Flask(__name__)

# ---- Regional terrain-based rainfall risk profiles ----
#
# IMPORTANT - methodology honesty note:
# The low_max/medium_max thresholds below are PROJECT-DEFINED SCENARIO
# THRESHOLDS, not official PMD/NDMA figures. They were originally
# commented as "PMD/NDMA-style" - that phrasing was misleading and has
# been corrected. If you cannot point to a specific published source that
# justifies an exact number, do not describe it as official anywhere in
# the app or scholarship writeup. Document the actual reasoning behind
# these numbers in METHODOLOGY.md before submission - "why does 55mm
# become a boundary" needs a real answer, not "it seemed reasonable."
#
# Scope: Sindh-focused. Cities/towns below are Sindh's major population
# centers plus well-known towns. A handful of major non-Sindh cities are
# tracked only for map context (see MAP_ONLY_CITIES below), not as a claim
# of full national coverage. Project architecture is designed to extend to
# the rest of Pakistan; only Sindh is validated for V1.
#
# Internal profile labels below (e.g. "Mega-Urban & Coastal") are used as
# lookup keys into translations.py's terrain_warnings / terrain_profile_labels
# dicts - do not rename these without updating translations.py to match.

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
# NOTE: "mountainous_rugged" profile was deleted (previously held Gwadar,
# Pasni, Turbat - all Balochistan, not Sindh, and were the only members).
# An empty scored category with real thresholds attached was misleading -
# looked like a validated terrain model with nothing behind it. If Sindh
# terrain (e.g. Kirthar range areas near Dadu/Jamshoro) genuinely needs a
# distinct profile, that's a data-backed addition, not a placeholder to
# keep alive on spec.

# Cities shown on the map for national context only. They are NOT part of
# this app's Sindh-focused risk model and must never be silently assigned
# a rainfall risk profile (previously a bug: they fell into scored profiles
# and got real thresholds meant for Sindh terrain, e.g. Quetta at 1676m
# elevation getting Karachi's coastal flood thresholds, or Gwadar getting
# a "mountainous_rugged" score despite being coastal Balochistan). Risk
# checks for these cities are explicitly refused - see get_profile() /
# check_risk(). Per project scope: architecture is Pakistan-wide, but only
# Sindh is validated for V1 - these stay map markers until real regional
# data justifies scoring them.
MAP_ONLY_CITIES = {
    "lahore", "islamabad", "peshawar", "quetta",
    "gwadar", "pasni", "turbat", "sibi", "chaman", "cholistan",
}

# Build a flat, normalized city -> profile_key lookup once at startup
_CITY_TO_PROFILE = {}
for _key, _profile in REGIONAL_PROFILES.items():
    for _city in _profile["cities"]:
        _CITY_TO_PROFILE[_city] = _key


def normalize_city(city):
    """Lowercase, strip whitespace, and drop a trailing country code like ',PK'."""
    if not city:
        return ""
    city = city.strip().lower()
    if "," in city:
        city = city.split(",")[0].strip()
    city = " ".join(city.split())  # collapse internal extra spaces
    return city


class MapOnlyCityError(Exception):
    """Raised when a risk check is attempted for a map-context-only city."""
    pass


class UnsupportedCityError(Exception):
    """Raised for a city that is neither in a scored profile nor in
    MAP_ONLY_CITIES - i.e. genuinely unrecognized by the V1 model. There is
    no silent fallback profile: an unrecognized city - a typo, a village,
    a real Pakistani city not yet added - must be refused, not guessed at.
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
# Per-region elevation ranges, computed once at startup from whatever real
# data elevation_data.py actually loaded (never hardcoded). A city's
# elevation is scored RELATIVE TO ITS OWN REGION, not on a single national
# scale - 7m in coastal Karachi and 7m inland mean different things, so
# comparing every city on one nationwide min/max would flatten that out.
#
# If elevation_data.py failed to load (see elevation_data.ELEVATION_LOAD_ERROR)
# or a specific city has no elevation row, elevation_component() returns
# (0, False) - the risk score falls back to rainfall alone and the caller
# is told explicitly that elevation was not used, rather than pretending a
# neutral score is a real measurement.

_REGION_ELEVATION_RANGES = {}  # profile_key -> (min_m, max_m) across that region's cities with data


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

ELEVATION_COMPONENT_MAX = 30  # points out of 100 contributed by elevation
RAINFALL_COMPONENT_MAX = 70   # points out of 100 contributed by rainfall


def elevation_component(city, profile_key):
    """Returns (points_0_to_30, elevation_was_used: bool, elevation_m_or_None).

    Lower elevation within its own region scores higher (more flood risk),
    since low-lying land pools water. A city at its region's minimum
    elevation gets the full 30 points; at the region's maximum, 0 points.
    A region with only one elevation value (min == max) can't be scored
    relatively, so it falls back to a fixed midpoint (15) rather than a
    division by zero or a fabricated distinction.
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

    # Inverse scale: lowest elevation in region -> full points
    fraction_high_ground = (elevation_m - region_min) / (region_max - region_min)
    points = ELEVATION_COMPONENT_MAX * (1 - fraction_high_ground)
    return round(points, 1), True, elevation_m


def rainfall_component(rainfall_mm, profile):
    """Returns points 0-70, scaled against this region's own low_max/medium_max.

    <= low_max scales 0-35 (still "low" territory but shows gradation).
    low_max..medium_max scales 35-60.
    > medium_max scales 60-70, capped at 70 for very extreme scenarios.
    """
    low_max = profile["low_max"]
    medium_max = profile["medium_max"]

    if rainfall_mm <= low_max:
        fraction = rainfall_mm / low_max if low_max > 0 else 0
        return round(35 * fraction, 1)
    elif rainfall_mm <= medium_max:
        fraction = (rainfall_mm - low_max) / (medium_max - low_max)
        return round(35 + 25 * fraction, 1)
    else:
        # Extreme scenarios: approach but do not exceed RAINFALL_COMPONENT_MAX.
        # Anything 2x medium_max or beyond is treated as maximal.
        excess_range = medium_max  # somewhat arbitrary saturation distance, documented in METHODOLOGY.md
        fraction = min((rainfall_mm - medium_max) / excess_range, 1) if excess_range > 0 else 1
        return round(60 + 10 * fraction, 1)


# ---- Risk tiers: 4-tier, 0-1 normalized scale ----
#
# CHANGED this session: was 3-tier (Low/Medium/High) on the raw 0-100
# score. Now 4-tier (Low/Moderate/High/Very High) on a 0-1 normalized
# score, to match the mockup's gauge design Hammad approved.
#
# IMPORTANT: this does NOT change the underlying rainfall/elevation point
# math above (still 0-70 / 0-30) - only the labeling and the scale shown
# to the user changed. The METHODOLOGY.md reasoning behind low_max/
# medium_max thresholds is still valid and does not need to be redone.
#
# RISK_SLUGS exists to fix a real bug: check.html previously derived its
# CSS class via risk_level_key.split(' ')[0].lower(), which silently broke
# for "Very High Risk" (-> "risk-very", matching no CSS class, badge
# renders uncolored). The slug is now computed once here, in Python, and
# passed straight to the template - no more guessing from a label string.
RISK_SLUGS = {
    "Low Risk": "low",
    "Moderate Risk": "moderate",
    "High Risk": "high",
    "Very High Risk": "very-high",
}

# FIX (this session): RISK_COLORS is now module-level and used by BOTH
# check_risk() (scenario/forecast result pages) AND _compute_risk_core()
# (the map cache, via get_all_city_risk_data()). Previously the color map
# was a local dict defined only inside check_risk() - the language-
# independent map-cache path (_compute_risk_core) never got a color at
# all, so every scored city on the map rendered with no color value,
# which the frontend fell back to grey for (indistinguishable from the
# genuinely-unscored MAP_ONLY_CITIES grey markers). One dict, one place,
# used everywhere a risk_key needs a color - this class of bug can't
# reoccur if a 5th tier is ever added.
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
    """Language-independent scoring only - no translation dict involved.
    Exists so results can be cached once and reused across all three
    languages, instead of caching a specific language's rendered text.
    Raises MapOnlyCityError / UnsupportedCityError, same as get_profile().
    """
    normalized = normalize_city(city)
    profile = get_profile(city)
    profile_label = profile["label"]
    profile_key = _CITY_TO_PROFILE[normalized]

    rain_pts = rainfall_component(rainfall_mm, profile)
    elev_pts, elevation_used, elevation_m = elevation_component(city, profile_key)
    total_score = round(rain_pts + elev_pts, 1)      # 0-100, methodology unchanged
    score_0_1 = round(total_score / 100, 2)           # NEW - normalized, drives the gauge/4-tier
    risk_key = score_to_risk_key(score_0_1)

    return {
        "profile_key": profile_key,
        "profile_label": profile_label,
        "rainfall_mm": rainfall_mm,
        "rainfall_points": rain_pts,
        "elevation_points": elev_pts,
        "elevation_used": elevation_used,
        "elevation_m": elevation_m,
        "score": total_score,                # 0-100 - still shown in "How is this calculated?"
        "score_0_1": score_0_1,              # NEW - drives the gauge
        "risk_level_key": risk_key,
        "risk_slug": RISK_SLUGS[risk_key],    # fixes the CSS-class bug described above
        "risk_color": RISK_COLORS[risk_key],  # FIX (this session) - see RISK_COLORS note above
    }


# Sorted, display-cased list of every scored city, for the home page's
# city dropdown - built once at startup from REGIONAL_PROFILES itself, so
# it can never drift out of sync with what the model actually supports.
# Deliberately excludes MAP_ONLY_CITIES - those aren't scoreable, so
# offering them in a form whose whole point is getting a score would just
# recreate the error path a dropdown is supposed to eliminate.
SUPPORTED_CITY_DISPLAY_NAMES = sorted({
    city.title() for profile in REGIONAL_PROFILES.values() for city in profile["cities"]
})


def get_lang():
    """Read ?lang= from the query string, fall back to English if missing/invalid."""
    lang = request.args.get("lang", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    return lang


def build_plain_explanation(rainfall_mm, elevation_used, elev_pts, city, risk_level_display, t):
    """One always-visible sentence explaining WHY the score came out the way
    it did, in plain language - the raw "Score: 67.0/100 (rainfall 37.0/70,
    elevation 30.0/30)" breakdown means nothing to someone deciding whether
    to evacuate. That breakdown still exists (moved behind a "How is this
    calculated?" toggle in check.html) for people who want the methodology
    transparency, but this sentence is the thing an ordinary person reads.
    """
    if elevation_used:
        position_key = (
            "elevation_position_low"
            if elev_pts >= (ELEVATION_COMPONENT_MAX / 2)
            else "elevation_position_high"
        )
        return t["explanation_with_elevation"].format(
            rainfall=rainfall_mm, city=city.title(),
            elevation_position=t[position_key], risk_level=risk_level_display,
        )
    else:
        return t["explanation_without_elevation"].format(
            rainfall=rainfall_mm, city=city.title(), risk_level=risk_level_display,
        )


def check_risk(rainfall_mm, city, t):
    """t = translation dict for the active language (from translations.py).
    Raises MapOnlyCityError / UnsupportedCityError - callers must catch
    both before rendering a result.
    """
    core = _compute_risk_core(city, rainfall_mm)
    profile_label = core["profile_label"]
    rain_pts = core["rainfall_points"]
    elev_pts = core["elevation_points"]
    elevation_used = core["elevation_used"]
    elevation_m = core["elevation_m"]
    total_score = core["score"]
    score_0_1 = core["score_0_1"]
    risk_key = core["risk_level_key"]
    risk_slug = core["risk_slug"]

    if elevation_used:
        elevation_note = t["elevation_note_available"].format(
            city=city.title(), elevation=elevation_m, profile=t["terrain_profile_labels"][profile_label]
        )
    else:
        elevation_note = t["elevation_note_unavailable"].format(city=city.title())

    risk_level_display = t["risk_levels"][risk_key]
    plain_explanation = build_plain_explanation(
        rainfall_mm, elevation_used, elev_pts, city, risk_level_display, t
    )

    return {
        "risk_level_key": risk_key,   # used for translation lookups
        "risk_slug": risk_slug,       # used for CSS class (risk-low/moderate/high/very-high)
        "risk_level": risk_level_display,
        "plain_explanation": plain_explanation,
        "rainfall": rainfall_mm,
        "score": total_score,
        "score_0_1": score_0_1,
        "rainfall_points": rain_pts,
        "elevation_points": elev_pts,
        "elevation_used": elevation_used,
        "elevation_note": elevation_note,
        "safety_tips": t["safety_tips"][risk_key],
        "shelter_message": t["shelter_message"],
        "terrain_profile": t["terrain_profile_labels"][profile_label],
        "terrain_warning": t["terrain_warnings"][profile_label],
        "risk_color": core["risk_color"],  # FIX (this session) - pulled from shared RISK_COLORS via core
    }


def sanitize_rainfall(raw_value):
    """Returns (valid: bool, value_or_none)."""
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return False, None
    if value < 0:
        return False, None
    return True, value


def check_city_exists_in_pakistan(city):
    """Validates that `city` is a real, locatable place in Pakistan, using
    OpenWeatherMap purely as a lookup - NOT for its weather data. Current
    weather is a live snapshot; this app's rainfall input is a hypothetical
    scenario, and mixing the two in the result page was confusing users
    about what was actually being measured. This function only returns
    True/False plus an error reason; no temp/description is read or kept.

    Returns (is_valid: bool, error_reason: str or None). error_reason is
    one of "missing_api_key", "timeout", "network_error", "not_found",
    "not_pakistan", "malformed_response" - or None if is_valid is True.
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
    """Fetches forecasted rainfall total (mm) over the next `hours` hours
    using OpenWeatherMap's free 5-day/3-hour forecast endpoint, by CITY
    NAME. Also validates the city exists in Pakistan - no need to call
    OpenWeatherMap twice for forecast mode, unlike scenario mode which
    validates separately via check_city_exists_in_pakistan.

    This is the right choice when the city name is arbitrary user input
    (the /forecast route) - there's no coordinate to fall back on for a
    city typed by a visitor. For the 38 known map cities, use
    get_forecast_rainfall_by_coords() instead (see note there for why).

    Returns (is_valid, rainfall_mm_or_None, error_reason_or_None).
    error_reason mirrors check_city_exists_in_pakistan's reasons.

    NOTE: this endpoint's `cod` field is a STRING ("200"), and country is
    nested under data["city"]["country"] - both differ from the current-
    weather endpoint used above. Do not reuse that validation logic here
    without adjusting for the shape difference.
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
    """Same as get_forecast_rainfall(), but queries OpenWeatherMap by
    coordinates instead of city name. Used for the map cache
    (get_all_city_risk_data) - every city in CITY_COORDINATES was already
    validated once via Nominatim at CSV-build time, so re-validating by
    name through OWM's separate, less complete geocoder was redundant AND
    the actual cause of a real bug: OWM's city-name search doesn't
    reliably index smaller Sindh towns (Mirpurkhas, Naushahro Feroze,
    Kashmore, Umerkot all returned "not_found" by name despite being real,
    correctly-coordinated cities). Querying by lat/lon sidesteps that
    entire class of failure.

    No country check here - CITY_COORDINATES only contains Pakistani
    cities by construction, so a "not_pakistan" result isn't a meaningful
    failure mode on this path.

    Scope note: this does NOT replace get_forecast_rainfall() or
    check_city_exists_in_pakistan() - /result and /forecast still take
    arbitrary user-typed city names with no known coordinate, so they
    still need name-based lookup and validation.

    Returns (is_valid, rainfall_mm_or_None, error_reason_or_None), same
    shape as get_forecast_rainfall() for drop-in use in the cache loop.
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
    """Shared render for both /result (scenario) and /forecast - mode
    controls which source-note copy is shown, so the user always knows
    whether the rainfall behind their score was forecasted or hypothetical.
    """
    if mode == "forecast":
        source_note = t["source_forecast"].format(hours=forecast_hours, mm=rainfall)
    else:
        source_note = t["source_scenario"].format(mm=rainfall)

    # Look up this city's coordinates for the single-marker result-page map.
    # Not every checked city is guaranteed to be in CITY_COORDINATES (e.g. a
    # real, correctly-scored city whose name doesn't exactly match the CSV
    # row for some reason) - city_lat/city_lon come through as None in that
    # case, and check.html must skip rendering the map rather than guess a
    # location or crash on a missing value.
    coords = _CITY_COORDS_LOOKUP.get(normalize_city(city))
    city_lat, city_lon = coords if coords else (None, None)

    return render_template(
        "check.html", t=t, lang=lang,
        city=city, rainfall=rainfall, mode=mode, source_note=source_note,
        plain_explanation=result["plain_explanation"],
        safety_tips=result["safety_tips"], shelter_message=result["shelter_message"],
        risk_level=result["risk_level"], risk_level_key=result["risk_level_key"],
        risk_slug=result["risk_slug"],
        terrain_profile=result["terrain_profile"], terrain_warning=result["terrain_warning"],
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


@app.route("/how-it-works")
def how_it_works():
    lang = get_lang()
    t = get_translation(lang)
    return render_template("how_it_works.html", t=t, lang=lang)


_city_risk_cache = {}
_cache_last_refreshed = None
CACHE_TTL_SECONDS = 3600  # refresh hourly - forecast rainfall doesn't meaningfully shift minute to minute


def get_all_city_risk_data(force_refresh=False):
    """Numeric-only risk data for all map cities, cached and refreshed on a
    TTL rather than fetched live per page view or per click.

    Uses get_forecast_rainfall_by_coords() (not the name-based
    get_forecast_rainfall()) since every entry in CITY_COORDINATES already
    has a verified lat/lon - see that function's docstring for why the
    name-based lookup was actually the bug for several Sindh towns.
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
        if entry.get("scored"):
            item["risk_level"] = t["risk_levels"][entry["risk_level_key"]]
            item["plain_explanation"] = build_plain_explanation(
                entry["rainfall_mm"], entry["elevation_used"], entry["elevation_points"],
                city, item["risk_level"], t
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
        # NOTE: city_error_reason (missing_api_key/timeout/network_error/
        # malformed_response/not_found/not_pakistan) is not yet surfaced as
        # distinct user-facing messages - all still show error_city. Worth
        # splitting further so "our weather service is down, try again" is
        # distinguished from "that's not a real city" - flagged, not done
        # yet.
        return render_template("check.html", error=t["error_city"], t=t, lang=lang)

    try:
        risk_result = check_risk(rainfall, city, t)
    except MapOnlyCityError:
        # City is real and outside Sindh - shown on the map for national
        # context only. Distinct message from a genuinely unrecognized city.
        return render_template("check.html", error=t["error_city_outside_coverage"], t=t, lang=lang)
    except UnsupportedCityError:
        # City passed the OpenWeatherMap validity check but isn't in this
        # app's V1 model yet (typo, village, or a real Pakistani city not
        # yet added) - refused rather than silently scored with a guessed
        # profile.
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
        # error_reason splitting is still an open item app-wide (see the
        # note in /result above) - collapsing to one message for now, but
        # flagging the failure so check.html can point the user to
        # scenario mode as a fallback.
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
    app.run(debug=True)