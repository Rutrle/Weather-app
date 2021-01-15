import requests
import json

url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=50&lon=20"
header = {
    "Accept": 'application/json',
    'User-Agent': 'weather app tryout https://github.com/Rutrle/Weather-app'


}


api_request = requests.get(url, headers=header)
api_request = api_request.json()
print(api_request)
