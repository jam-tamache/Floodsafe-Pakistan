from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)

safety_tips = {
    "Low Risk": [
        "No immediate danger, but keep an eye on local weather updates",
        "Clear roof drains and gutters in case rainfall picks up",
        "Keep your phone charged and know your nearest shelter location"
    ],
    "Medium Risk": [
        "Move important documents (CNIC, land papers) to a high, dry place",
        "Keep emergency cash and a charged phone/power bank ready",
        "Avoid parking vehicles in low-lying or riverside areas",
        "Check on elderly neighbors and family who may need help evacuating"
    ],
    "High Risk": [
        "Evacuate immediately if local authorities issue a warning",
        "Never walk or drive through moving floodwater, even if it looks shallow",
        "Turn off electricity and gas at the mains before leaving home",
        "Head to the nearest designated shelter with documents, medicines, and water",
        "Call 1122 (Pakistan's emergency rescue service) if you're trapped or need help"
    ]
}

# ---- Shelter data (normalized keys: lowercase, stripped) ----
shelter = {
    "nawabshah": ["Govt Boys High School"],
    "sakrand": ["Taluka Hospital"],
    "moro": ["Degree College Moro"],
    "kotri": ["Govt Girls High School"],
    "hyderabad": [
        "Government College Kali Mori",
        "Government College for Boys Pretabad",
        "Government High School Sir Ghulam Hussain Hidayatullah (Pucca Qila)",
        "Government Girls College Bakra Mandi",
        "Government City College Hyderabad"
    ],
    "karachi": [
        "Government Degree College Nazimabad",
        "Government College for Men Nazimabad",
        "Sindh Government Science College Federal B Area",
        "Government Boys Degree College North Karachi",
        "Government College of Commerce and Economics"
    ],
}

# ---- Regional terrain-based rainfall risk profiles ----
# Thresholds based on PMD/NDMA-style regional rainfall classification.
# NOTE: city-to-profile placement below is a reasonable approximation, not an
# authoritative PMD/NDMA zone map. Before submitting for scholarship review,
# spot-check a handful of placements you know well (e.g. does PMD classify
# Sargodha as plains or semi-arid in their own docs) - I'm not a verified
# source for exact zone boundaries.

REGIONAL_PROFILES = {
    "mega_urban_coastal": {
        "label": "Mega-Urban & Coastal",
        "cities": [
            "karachi", "hyderabad", "badin", "thatta", "lahore", "rawalpindi",
            "faisalabad", "multan", "gujranwala", "peshawar", "quetta",
            "sialkot", "islamabad"
        ],
        "low_max": 20, "medium_max": 45,
        "color": "#28a745",
        "warning": "Urban drainage systems can back up quickly - avoid clogged storm drains and underpasses."
    },
    "mountainous_rugged": {
        "label": "Mountainous & Rugged Terrain",
        "cities": [
            "swat", "abbottabad", "mansehra", "chitral", "dir", "gilgit",
            "skardu", "muzaffarabad", "mirpur", "murree", "gwadar", "pasni",
            "turbat", "panjgur", "kharan", "kalat", "khuzdar"
        ],
        "low_max": 15, "medium_max": 40,
        "color": "#ffc107",
        "warning": "Steep terrain increases landslide and flash flood risk - avoid hillside roads and dry riverbeds (nullahs) during and after rainfall."
    },
    "central_plains": {
        "label": "Central Agricultural Plains",
        "cities": [
            "sukkur", "larkana", "nawabshah", "khairpur", "dadu", "ghotki",
            "sahiwal", "sargodha", "jhang", "bahawalpur", "rahim yar khan",
            "dera ghazi khan", "moro", "sakrand", "kotri"
        ],
        "low_max": 25, "medium_max": 55,
        "color": "#28a745",
        "warning": "Low-lying farmland can pool water for days - keep livestock and stored grain away from field edges."
    },
    "arid_plains_desert": {
        "label": "Arid Plains & Deserts",
        "cities": [
            "jacobabad", "sibi", "cholistan", "tharparkar", "umerkot",
            "sanghar", "chaman"
        ],
        "low_max": 35, "medium_max": 65,
        "color": "#dc3545",
        "warning": "Dry, hard-packed ground sheds water fast - watch for sudden dry riverbed (nullah) overflows even hours after rain stops."
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


def check_risk(rainfall_mm, city):
    profile = get_profile(city)

    if rainfall_mm <= profile["low_max"]:
        risk_level = "Low Risk"
    elif rainfall_mm <= profile["medium_max"]:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    color_map = {"Low Risk": "#28a745", "Medium Risk": "#ffc107", "High Risk": "#dc3545"}
    normalized_city = normalize_city(city)

    return {
        "risk_level": risk_level,
        "rainfall": rainfall_mm,
        "safety_tips": safety_tips[risk_level],
        "shelter": shelter.get(normalized_city, ["No Shelter Information Available"]),
        "terrain_profile": profile["label"],
        "terrain_warning": profile["warning"],
        "risk_color": color_map[risk_level],
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
    return render_template("index.html")


@app.route("/check/<city>/<int:rainfall>")
def check(city, rainfall):
    result = check_risk(rainfall, city)
    return render_template(
        "check.html", city=city, rainfall=rainfall,
        safety_tips=result["safety_tips"], shelter=result["shelter"],
        risk_level=result["risk_level"], terrain_profile=result["terrain_profile"],
        terrain_warning=result["terrain_warning"], risk_color=result["risk_color"]
    )


@app.route("/result")
def result():
    city = request.args.get("city")
    rainfall_raw = request.args.get("rainfall")

    url = (f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=361ed44cd513bb31594d424beb00e243&units=metric")
    response = requests.get(url)
    data = response.json()

    rainfall_valid, rainfall = sanitize_rainfall(rainfall_raw)

    if data.get("cod") == 200 and data.get("sys", {}).get("country") == "PK":
        city_valid = True
    else:
        city_valid = False

    if not rainfall_valid and not city_valid:
        return render_template("check.html", error="Please enter a valid city and rainfall.")
    elif not rainfall_valid:
        return render_template("check.html", error="Please enter a valid rainfall (a positive number).")
    elif not city_valid:
        return render_template("check.html", error="Please enter a valid city.")
    else:
        result = check_risk(rainfall, city)
        return render_template(
            "check.html", city=city, rainfall=rainfall,
            safety_tips=result["safety_tips"], shelter=result["shelter"],
            risk_level=result["risk_level"], terrain_profile=result["terrain_profile"],
            terrain_warning=result["terrain_warning"], risk_color=result["risk_color"],
            temp=data["main"]["temp"], description=data["weather"][0]["description"]
        )


if __name__ == "__main__":
    app.run(debug=True)