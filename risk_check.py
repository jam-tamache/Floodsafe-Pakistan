import os
import time
from flask import Flask, jsonify, render_template, request
import requests
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
        "low_max": 20, "medium_max": 45,
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
        "low_max": 25, "medium_max": 55,
        "color": "#28a745",
    },
    "arid_plains_desert": {
        "label": "Arid Plains & Deserts",
        "cities": [
            "jacobabad", "mithi", "umerkot", "sanghar"
        ],
        "low_max": 35, "medium_max": 65,
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


def score_to_risk_key(score):
    if score <= 35:
        return "Low Risk"
    elif score <= 65:
        return "Medium Risk"
    else:
        return "High Risk"


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
    normalized = normalize_city(city)
    profile = get_profile(city)  # raises MapOnlyCityError / UnsupportedCityError
    profile_label = profile["label"]  # internal English key, used for lookups
    profile_key = _CITY_TO_PROFILE[normalized]

    rain_pts = rainfall_component(rainfall_mm, profile)
    elev_pts, elevation_used, elevation_m = elevation_component(city, profile_key)
    total_score = round(rain_pts + elev_pts, 1)
    risk_key = score_to_risk_key(total_score)

    color_map = {"Low Risk": "#28a745", "Medium Risk": "#ffc107", "High Risk": "#dc3545"}

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
        "risk_level_key": risk_key,  # used for CSS class (risk-low/medium/high)
        "risk_level": risk_level_display,
        "plain_explanation": plain_explanation,
        "rainfall": rainfall_mm,
        "score": total_score,
        "rainfall_points": rain_pts,
        "elevation_points": elev_pts,
        "elevation_used": elevation_used,
        "elevation_note": elevation_note,
        "safety_tips": t["safety_tips"][risk_key],
        "shelter_message": t["shelter_message"],
        "terrain_profile": t["terrain_profile_labels"][profile_label],
        "terrain_warning": t["terrain_warnings"][profile_label],
        "risk_color": color_map[risk_key],
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
        f"?q={city}&appid={api_key}&units=metric"
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
    using OpenWeatherMap's free 5-day/3-hour forecast endpoint. Also
    validates the city exists in Pakistan - no need to call OpenWeatherMap
    twice for forecast mode, unlike scenario mode which validates separately
    via check_city_exists_in_pakistan.

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
        f"?q={city}&appid={api_key}&units=metric"
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


def _render_risk_result(result, city, rainfall, mode, t, lang, forecast_hours=None):
    """Shared render for both /result (scenario) and /forecast - mode
    controls which source-note copy is shown, so the user always knows
    whether the rainfall behind their score was forecasted or hypothetical.
    """
    if mode == "forecast":
        source_note = t["source_forecast"].format(hours=forecast_hours, mm=rainfall)
    else:
        source_note = t["source_scenario"].format(mm=rainfall)

    return render_template(
        "check.html", t=t, lang=lang,
        city=city, rainfall=rainfall, mode=mode, source_note=source_note,
        plain_explanation=result["plain_explanation"],
        safety_tips=result["safety_tips"], shelter_message=result["shelter_message"],
        risk_level=result["risk_level"], risk_level_key=result["risk_level_key"],
        terrain_profile=result["terrain_profile"], terrain_warning=result["terrain_warning"],
        risk_color=result["risk_color"],
        score=result["score"], rainfall_points=result["rainfall_points"],
        elevation_points=result["elevation_points"], elevation_note=result["elevation_note"],
    )


@app.route("/")
def home():
    lang = get_lang()
    t = get_translation(lang)
    return render_template("index.html", t=t, lang=lang)


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