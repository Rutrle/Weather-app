import requests


api_request = requests.get(
    'https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324/')

print(api_request.content)
