from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)

safety_tips = {
    "Low Risk": ["Stay informed", "Monitor weather updates", "Keep emergency contacts ready"],
    "Medium Risk": ["Prepare an emergency kit", "Charge your phone", "Move valuables to higher places", "Be ready to evacuate"],
    "High Risk": ["Evacuate if advised by authorities", "Avoid walking or driving through floodwater",
              "Go to nearest safe shelter", "Carry documents and medicines", "Call emergency services if needed"]
}

shelter = {
     "Nawabshah": ["Govt Boys High School"],
     "Sakrand": ["Taluka Hospital"],
     "Moro": ["Degree College Moro"],
     "Kotri": ["Govt Girls High School"],
     "Hyderabad": [
        "Government College Kali Mori",
        "Government College for Boys Pretabad",
        "Government High School Sir Ghulam Hussain Hidayatullah (Pucca Qila)",
        "Government Girls College Bakra Mandi",
        "Government City College Hyderabad"
    ]
}


def check_risk(rainfall_mm, city):
    if rainfall_mm <= 20:
        risk_level = "Low Risk"
    elif rainfall_mm <= 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return {
        "risk_level": risk_level,
        "rainfall": rainfall_mm,
        "safety_tips": safety_tips[risk_level],
        "shelter": shelter.get(city, ["No Shelter Information Available"])
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check/<city>/<int:rainfall>")
def check(city, rainfall):
    result = check_risk(rainfall, city)
    return render_template("check.html", city=city, rainfall=rainfall, safety_tips=result["safety_tips"], shelter=result["shelter"], risk_level=result["risk_level"])

@app.route("/result")
def result():
    city = request.args.get("city")
    rainfall = request.args.get("rainfall")


    url = (f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=361ed44cd513bb31594d424beb00e243&units=metric")
    response = requests.get(url)
    data = response.json()
    print(data)

    rainfall_valid = True
    try:
        rainfall = int(rainfall)
    except ValueError:
        rainfall_valid = False

    if data["cod"] == 200:
        city_valid = True
    else:
        city_valid = False

    if not rainfall_valid and not city_valid:
        return render_template("check.html", error="Please enter a valid city and rainfall.")
    elif not rainfall_valid:
        return render_template("check.html", error="Please enter a valid rainfall.")
    elif not city_valid:
        return render_template("check.html", error="Please enter a valid city.")
    else:
        result = check_risk(rainfall, city)
        return render_template("check.html", city=city, rainfall=rainfall,
        safety_tips=result["safety_tips"], shelter=result["shelter"],
        risk_level=result["risk_level"],
        temp=data["main"]["temp"], description=data["weather"][0]["description"])
    
if __name__ == "__main__":
    app.run(debug=True)