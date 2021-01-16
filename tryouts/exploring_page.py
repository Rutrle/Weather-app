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


'''
    def prepare_yr_data(self, temperatures, dates):
        max_day_temperatures, prepared_dates = [], []

        sorted_temperatures = defaultdict(list)

        for i in range(len(dates)):
            sorted_temperatures[dates[i].strftime(
                '%d. %m.')].append(temperatures[i])

        for date in sorted_temperatures:
            pass

        return max_day_temperatures, prepared_dates
'''

