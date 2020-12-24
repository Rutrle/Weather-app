import tkinter
import datetime
from PIL import ImageTk, Image
import requests
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict


class Weather_app:
    '''app for getting weather forecast from multiple websites and displaying those data'''

    def __init__(self):
        self.root = tkinter.Tk()

        self.customize_frame()
        self.fill_in_basics()
        self.fill_in_days()

        self.root.mainloop()

    def customize_frame(self):
        '''customizes basic frame for weather app'''
        self.root.title('Weather forecast comparison')
        self.root.geometry('650x400')

    def fill_in_basics(self):
        ''' fills in tkinter window with basic info'''
        city_label = tkinter.Label(self.root, text='City:')
        city_label.grid(row=2, column=0, columnspan=1, pady=20)

        options = ['Praha', 'Brno', 'Kvilda']

        self.place_selection = tkinter.StringVar()
        self.place_selection.set(options[0])
        self.place_dropmenu = tkinter.OptionMenu(
            self.root, self.place_selection, *options)
        self.place_dropmenu.grid(
            row=2, column=1, columnspan=1, padx=10)

        button_get_temperatures = tkinter.Button(self.root, text="get temperatures",
                                                 command=lambda: self.show_temperatures())
        button_get_temperatures.grid(
            row=2, column=2, columnspan=1, padx=10, pady=10)

        openweather_label = tkinter.Label(self.root, text='Openweather')
        openweather_label.grid(row=6, column=0, columnspan=1)
        in_pocasi_label = tkinter.Label(self.root, text='In Počasí')
        in_pocasi_label.grid(row=7, column=0, columnspan=1)

        '''for later commit
        button_exit = tkinter.Button(
            self.root, text="Zavřít", command=self.root.destroy)
        button_exit.grid(row=99, column=3, columnspan=1, padx=10, pady=10)
        '''

    def show_temperatures(self):
        print(self.place_selection.get())
        self.fill_in_days()

    def fill_in_days(self):
        '''fill in informations for all days'''
        temperatures_openweather, dates_openweather = self.get_data_openweather(
            self.place_selection.get())
        temperatures_in_pocasi, dates_in_pocasi = self.get_in_pocasi_data(
            self.place_selection.get())

        weather_data = self.prepare_weather_data(
            dates_openweather, temperatures_openweather, dates_in_pocasi, temperatures_in_pocasi)

        self.days_labels = []
        self.open_temperatures = {}
        self.in_temperatures = {}
        for i in range(weather_data['length']):
            self.fill_in_day(weather_data, i)

    def fill_in_day(self, weather_data, index):
        '''
        fills in forecast information in tkinter window for a single day
        :param weather_data: dict
                        dictionary with temperatures and respective dates
        :param index: int
                        list of temperatures from different sites
        '''
        self.days_labels.append(tkinter.Label(
            self.root, text=weather_data['dates'][index]))

        day_position = len(self.days_labels)
        print(day_position)

        self.days_labels[-1].grid(row=5,
                                  column=day_position, columnspan=1, padx=10)

        date = weather_data['dates'][index]

        self.open_temperatures[date] = tkinter.Label(
            self.root, text=str(weather_data['temperatures_openweather'][index]))
        self.open_temperatures[date].grid(
            row=6, column=day_position, columnspan=1, padx=10)

        self.in_temperatures[date] = tkinter.Label(
            self.root, text=str(weather_data['temperatures_in_pocasi'][index]))
        self.in_temperatures[date].grid(
            row=7, column=day_position, columnspan=1, padx=10)

    def prepare_weather_data(self, dates_openweather, temperatures_openweather, dates_in_pocasi, temperatures_in_pocasi):
        max_length = max(len(dates_in_pocasi), len(dates_openweather))

        temperatures_openweather = self.fill_in_vector(
            temperatures_openweather, max_length)
        dates_openweather = self.fill_in_vector(dates_openweather, max_length)
        temperatures_in_pocasi = self.fill_in_vector(
            temperatures_in_pocasi, max_length)
        dates_in_pocasi = self.fill_in_vector(dates_in_pocasi, max_length)

        weather_data = {}
        weather_data['dates'] = dates_in_pocasi
        weather_data['temperatures_openweather'] = temperatures_openweather
        weather_data['temperatures_in_pocasi'] = temperatures_in_pocasi
        weather_data['length'] = max_length

        return weather_data

    def fill_in_vector(self, vector, final_length):
        '''
        appends given vector with "NA" until it reaches length final_length
        :param vector: list
        :param final_length: int
        '''
        while len(vector) < final_length:
            vector.append('NA')
        return vector

    def get_data_openweather(self, place):
        '''get weather forecast data from openweather api and returns temperatures and dates lists'''
        token = '3826180b6619b9e8655cd67a2fa30f52'
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        city = 'praha'

        parametry = {
            'APIKEY': token,
            'q': city,
            'units': 'metric'
        }

        api_request = requests.get(url, params=parametry)
        api_request = api_request.json()

        dates, temperatures = [], []
        for item in api_request['list']:
            date = item['dt']
            temperature = item['main']['temp']

            date = datetime.datetime.fromtimestamp(date)

            dates.append(date)
            temperatures.append(temperature)
            '''used for exploring data
            print(date, '.'*int(temperature//1), temperature)
            print(date.strftime('%H'))
            '''

        ''' saving whole dataset from openweather to json file for exploring
        with open('weather.json', 'w') as file:
        json.dump(api_request, file, indent=4)
        '''

        temperatures, dates = self.prepare_openweather_data(
            temperatures, dates)

        return temperatures, dates

    def prepare_openweather_data(self, temperatures, dates):
        '''clears and prepares data from opeweather api'''
        max_day_temperatures, prepared_dates = [], []

        sorted_temperatures = defaultdict(list)

        for i in range(len(dates)):
            sorted_temperatures[dates[i].strftime(
                '%d. %m.')].append(temperatures[i])

        for date in sorted_temperatures:
            max_day_temperatures.append(
                str(max(sorted_temperatures[date])) + ' °C')
            prepared_dates.append(date)

        today_date = (datetime.date.today())
        if prepared_dates[0] != today_date.strftime('%d. %m.'):
            prepared_dates.insert(0, 'NA')
            max_day_temperatures.insert(0, 'NA')

        return max_day_temperatures, prepared_dates

    def max_day_temp(self, temperatures, dates):
        openweather_dictionary = {}

    def get_in_pocasi_data(self, place):
        '''get weather forecast data from in Počasí website and returns temperatures and dates lists'''
        urls = {'Praha': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324',
                'Kvilda': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/kvilda-4588/'}
        url = urls[place]
        api_request = requests.get(url)
        soup = BeautifulSoup(api_request.content, 'html.parser')

        temperatures, dates = [], []

        actual_temp = soup.find(class_='alfa mb-1')
        actual_temp = actual_temp.text
        actual_temp = re.findall(r"[-+]?\d*\.\d+|\d+", actual_temp)
        temperatures.append(str(actual_temp[0]) + '°C')
        dates.append(datetime.date.today().strftime('%d. %m.'))

        indexes = ['day'+str(i) for i in range(1, 8)]
        for i in range(len(indexes)):
            try:
                results = soup.find(id=indexes[i])
                results = results.find(class_="mt-1 strong")
                temperatures.append(results.text)
                date = datetime.date.today() + datetime.timedelta(days=(i+1))
                dates.append(date.strftime('%d. %m.'))

            except AttributeError:
                print(f"{indexes[i]} index was not found")

        return temperatures, dates


if __name__ == "__main__":
    Weather_app()
