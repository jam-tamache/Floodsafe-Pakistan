safety_tips = {
    "Low Risk": ["Stay informed", "Monitor weather updates", "Keep emergency contacts ready"] ,
    "Medium Risk": ["Prepare an emergency kit", "Charge your phone", "Move valuables to higher places", "Be ready to evacuate"] ,
    "High Risk": ["Evacuate if advised by authorities", "Avoid walking or driving through floodwater",
              "Go to nearest safe shelter", "Carry documents and medicines", "Call emergency services if needed"]
}

shelters = {
     "Nawabshah" : "Govt Boys High School",
     "Sakrand" : "Taluka Hospital",
     "Moro" : "Degree College Moro",
     "Kotri" : "Govt Girls High School",
}

def check_risk(rainfall_mm, city):
    if rainfall_mm <= 20:
        risk_level = "Low Risk"
    elif rainfall_mm <+ 40:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return {
        "risk_level": risk_level,
        "rainfall": rainfall_mm,
        "safety_tips": safety_tips[risk_level],
        "shelter": shelters.get(city, "No Shelter Information Available")
    }

city = input("Enter Your City: ")
rainfall_mm = int(input("Enter The Rainfall in mm: "))
risk = check_risk(rainfall_mm, city)
print(f"Risk Level: {risk['risk_level']}")
print(f"Shelter: {risk['shelter']}")
print("Safety Tips:")
for tip in risk['safety_tips']:
    print(f"- {tip}")