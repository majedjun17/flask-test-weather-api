import requests

API_KEY = "f22892654725839a44ff6db985f0b151"
lat = "32.5568095"
lon = "35.846887"

response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}")
print(response.json()['main']['humidity'])