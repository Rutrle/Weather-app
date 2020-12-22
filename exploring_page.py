import requests
import pprint
from bs4 import BeautifulSoup

api_request = requests.get(
    'https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324/?den=6#day6')

# pprint.pprint(api_request.content)
soup = BeautifulSoup(api_request.content, 'html.parser')
results = soup.find_all('script')
#results = results.find_all('var pd')
print(results)
