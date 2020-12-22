import tkinter

from PIL import ImageTk, Image
import requests
import json


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
        self.root.geometry('400x400')

    def fill_in_basics(self):
        ''' fills in tkinter window with basic info'''
        city_label = tkinter.Label(self.root, text='City:')
        city_label.grid(row=2, column=0, columnspan=1, pady=20)
        current_city_label = tkinter.Label(self.root, text='Praha')
        current_city_label.grid(row=2, column=1, columnspan=1)
        openweather_label = tkinter.Label(self.root, text='Openweather')
        openweather_label.grid(row=5, column=0, columnspan=1)

    def fill_in_days(self):

        self.days_labels = []
        temperatures_openweather, dates_openweather = self.get_data_openweather()
        for i in range(len(dates_openweather)):
            self.fill_in_day(dates_openweather[i], temperatures_openweather[i])

    def fill_in_day(self, date, temperatures):
        '''
        date: str
                        date of day that hould be filled in
        temperatures: list of integers
                        list of temperatures from different sites
        '''
        self.days_labels.append(tkinter.Label(self.root, text=date))
        day_position = 1 + len(self.days_labels)
        self.days_labels[-1].grid(row=5, column=day_position, columnspan=1)

    def get_data_openweather(self):
        '''get weather data from openweather and returns tempeeratures and dates lists'''
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
            date = item['dt_txt']
            temperature = item['main']['temp']

            dates.append(date)
            temperatures.append(temperature)
            print(date, '.'*int(temperature//1), temperature)

        return temperatures, dates

        ''' saving whole dataset from openweather to json file for exploring
        with open('weather.json', 'w') as file:
        json.dump(api_request, file, indent=4)
        '''


if __name__ == "__main__":
    Weather_app()
