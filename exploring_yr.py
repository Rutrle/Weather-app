import requests
import json
import datetime

url = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=50&lon=20"
header = {
    "Accept": 'application/json',
    'User-Agent': 'weather app tryout https://github.com/Rutrle/Weather-app'
}


api_request = requests.get(url, headers=header)
api_request = api_request.json()
# print(api_request)

with open('yr.json', 'w') as writefile:
    json.dump(api_request, writefile, indent=4)


relevant_data = api_request['properties']['timeseries']

with open('cleaned_data.json', 'w') as f:
    json.dump(relevant_data, f, indent=4)

for weather_log in relevant_data:
    print(weather_log['time'])
    print(weather_log['data']['instant']['details']['air_temperature'])



'2021-01-17T03:00:00Z'