import requests

url = "https://api.openweathermap.org/data/2.5/weather?q=Karachi&appid=361ed44cd513bb31594d424beb00e243"

response = requests.get(url)

data = response.json()

print(data)

rain_data = data.get("rain", {})
rainfall_1h = rain_data.get("1h", 0)
print(rainfall_1h)