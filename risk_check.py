import os
from flask import Flask, jsonify, render_template, request
import requests
from dotenv import load_dotenv
from translations import get_translation, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

load_dotenv()  # reads variables from a .env file in the same folder as this script

app = Flask(__name__)

# ---- Regional terrain-based rainfall risk profiles ----
# Thresholds based on PMD/NDMA-style regional rainfall classification.
# NOTE: city-to-profile placement below is a reasonable approximation, not an
# authoritative PMD/NDMA zone map. Before submitting for scholarship review,
# spot-check a handful of placements you know well - I'm not a verified
# source for exact zone boundaries.
#
# Scope: Sindh-focused. Cities/towns below are Sindh's major population
# centers plus well-known towns. A handful of major non-Sindh cities are
# included only for map context (Lahore, Islamabad, Peshawar, Quetta), not
# as a claim of full national coverage.
#
# Internal profile labels below (e.g. "Mega-Urban & Coastal") are used as
# lookup keys into translations.py's terrain_warnings / terrain_profile_labels
# dicts - do not rename these without updating translations.py to match.

REGIONAL_PROFILES = {
    "mega_urban_coastal": {
        "label": "Mega-Urban & Coastal",
        "cities": [
            "karachi", "hyderabad", "badin", "thatta",
            # non-Sindh, map-context only:
            "lahore", "islamabad", "peshawar", "quetta"
        ],
        "low_max": 20, "medium_max": 45,
        "color": "#28a745",
    },
    "mountainous_rugged": {
        "label": "Mountainous & Rugged Terrain",
        "cities": [
            "gwadar", "pasni", "turbat"
        ],
        "low_max": 15, "medium_max": 40,
        "color": "#ffc107",
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
            "jacobabad", "sibi", "cholistan", "tharparkar", "umerkot",
            "sanghar", "chaman"
        ],
        "low_max": 35, "medium_max": 65,
        "color": "#dc3545",
    },
}

DEFAULT_PROFILE_KEY = "central_plains"  # national fallback for unlisted towns/villages

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


def get_profile(city):
    normalized = normalize_city(city)
    profile_key = _CITY_TO_PROFILE.get(normalized, DEFAULT_PROFILE_KEY)
    return REGIONAL_PROFILES[profile_key]


def get_lang():
    """Read ?lang= from the query string, fall back to English if missing/invalid."""
    lang = request.args.get("lang", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    return lang


def check_risk(rainfall_mm, city, t):
    """t = translation dict for the active language (from translations.py)."""
    profile = get_profile(city)
    profile_label = profile["label"]  # internal English key, used for lookups

    if rainfall_mm <= profile["low_max"]:
        risk_key = "Low Risk"
    elif rainfall_mm <= profile["medium_max"]:
        risk_key = "Medium Risk"
    else:
        risk_key = "High Risk"

    color_map = {"Low Risk": "#28a745", "Medium Risk": "#ffc107", "High Risk": "#dc3545"}

    return {
        "risk_level_key": risk_key,  # used for CSS class (risk-low/medium/high)
        "risk_level": t["risk_levels"][risk_key],
        "rainfall": rainfall_mm,
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

    api_key = os.environ.get("OPENWEATHER_API_KEY")
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    response = requests.get(url)
    data = response.json()

    rainfall_valid, rainfall = sanitize_rainfall(rainfall_raw)

    if data.get("cod") == 200 and data.get("sys", {}).get("country") == "PK":
        city_valid = True
    else:
        city_valid = False

    if not rainfall_valid and not city_valid:
        return render_template("check.html", error=t["error_both"], t=t, lang=lang)
    elif not rainfall_valid:
        return render_template("check.html", error=t["error_rainfall"], t=t, lang=lang)
    elif not city_valid:
        return render_template("check.html", error=t["error_city"], t=t, lang=lang)
    else:
        result = check_risk(rainfall, city, t)
        return render_template(
            "check.html", t=t, lang=lang,
            city=city, rainfall=rainfall,
            safety_tips=result["safety_tips"], shelter_message=result["shelter_message"],
            risk_level=result["risk_level"], risk_level_key=result["risk_level_key"],
            terrain_profile=result["terrain_profile"], terrain_warning=result["terrain_warning"],
            risk_color=result["risk_color"],
            temp=data["main"]["temp"], description=data["weather"][0]["description"]
        )


if __name__ == "__main__":
    app.run(debug=True)