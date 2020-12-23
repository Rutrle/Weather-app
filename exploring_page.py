import requests
import pprint
from bs4 import BeautifulSoup

api_request = requests.get(
    'https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324')

# pprint.pprint(api_request.content)
soup = BeautifulSoup(api_request.content, 'html.parser')
results = soup.find(id='day1')
results = results.find(class_="mt-1 strong")
print(results.text)

actual_temp = soup.find(class_='alfa mb-1')

print(actual_temp.text)
