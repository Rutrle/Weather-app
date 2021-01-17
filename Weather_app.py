import tkinter
import datetime
import requests
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Weather_app:
    '''app for getting weather forecast from multiple websites and displaying those data'''

    def __init__(self):
        self.root = tkinter.Tk()

        self.customize_frame()
        self.fill_in_basics()

        self.show_temperatures()

        self.root.mainloop()

    def customize_frame(self):
        '''customizes basic frame for weather app'''
        self.root.title('Weather forecast comparison')
        self.root.geometry('820x600')

    def fill_in_basics(self):
        ''' fills in tkinter window with basic info'''
        city_label = tkinter.Label(self.root, text='City:')
        city_label.grid(row=2, column=0, columnspan=1, pady=20)

        place_options = ['Praha', 'Brno', 'Kvilda', 'Nová Paka']

        self.place_selection = tkinter.StringVar()
        self.place_selection.set(place_options[0])
        self.place_dropmenu = tkinter.OptionMenu(
            self.root, self.place_selection, *place_options)
        self.place_dropmenu.grid(
            row=2, column=1, columnspan=2)

        units_label = tkinter.Label(self.root, text='Units:')
        units_label.grid(row=2, column=3, columnspan=1, pady=20)

        degrees_options = ['Celsius', 'Fahrenheit', 'Kelvin']
        self.degrees_selection = tkinter.StringVar()
        self.degrees_selection.set(degrees_options[0])
        self.degrees_dropmenu = tkinter.OptionMenu(
            self.root, self.degrees_selection, *degrees_options)
        self.degrees_dropmenu.grid(
            row=2, column=4, columnspan=2)

        button_get_temperatures = tkinter.Button(self.root, text="get temperatures",
                                                 command=lambda: self.show_temperatures())
        button_get_temperatures.grid(
            row=2, column=6, columnspan=2, padx=10, pady=10)

        openweather_label = tkinter.Label(self.root, text='Openweather')
        openweather_label.grid(row=6, column=0, columnspan=1, padx=20)
        in_pocasi_label = tkinter.Label(self.root, text='In Počasí')
        in_pocasi_label.grid(row=7, column=0, columnspan=1)

        Yr_label = tkinter.Label(self.root, text='Yr.no')
        Yr_label.grid(row=8, column=0, columnspan=1)

        button_exit = tkinter.Button(
            self.root, text="Zavřít", command=self.root.destroy)
        button_exit.grid(row=99, column=8, columnspan=1, padx=10, pady=10)

    def show_temperatures(self):
        '''show temperatures in tkinter window and graph'''

        weather_data = self.get_weather_data()

        weather_data = self.unit_conversion(weather_data)

        self.plot_temperatures(weather_data)
        print(weather_data['length'])
        weather_data = self.fill_in_vectors(weather_data)

        self.fill_in_days(weather_data)

    def get_weather_data(self):
        '''collects weather data from all sources and returns them in dictionary of lists'''
        temperatures_openweather, dates_openweather = self.get_data_openweather(
            self.place_selection.get())
        temperatures_in_pocasi, dates_in_pocasi = self.get_in_pocasi_data(
            self.place_selection.get())
        temperatures_yr, dates_yr = self.get_yr_data(
            self.place_selection.get())

        weather_data = self.prepare_weather_data(
            dates_openweather, temperatures_openweather, dates_in_pocasi, temperatures_in_pocasi, temperatures_yr, dates_yr)
        print(weather_data)

        return weather_data

    def fill_in_days(self, weather_data):
        '''
        fill in informations for all days
        :param weather_data: dictionary of lists
        '''
        self.days_labels = []
        self.open_temperatures = {}
        self.in_temperatures = {}
        self.yr_temperatures = {}
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

        self.days_labels[-1].grid(row=5,
                                  column=day_position, columnspan=1, padx=10)

        date = weather_data['dates'][index]

        open_temperature = self.add_degrees_symbol(
            str(weather_data['temperatures_openweather'][index]))
        in_temperature = self.add_degrees_symbol(
            str(weather_data['temperatures_in_pocasi'][index]))
        yr_temperature = self.add_degrees_symbol(
            str(weather_data['temperatures_yr'][index]))

        self.open_temperatures[date] = tkinter.Label(
            self.root, text=(open_temperature), width=5)
        self.open_temperatures[date].grid(
            row=6, column=day_position, columnspan=1)

        self.in_temperatures[date] = tkinter.Label(
            self.root, text=(in_temperature), width=5)
        self.in_temperatures[date].grid(
            row=7, column=day_position, columnspan=1)

        self.yr_temperatures[date] = tkinter.Label(
            self.root, text=(yr_temperature), width=5)
        self.yr_temperatures[date].grid(
            row=8, column=day_position, columnspan=1)

    def add_degrees_symbol(self, temperature):
        '''
        adds degrees symbol, depending on selected units, to temperature in case the temperature is a valid number
        :param temperature: string
                                temperature to which units should be added
        '''
        if temperature != 'NA':
            if self.degrees_selection.get() == 'Celsius':
                temperature = temperature + ' °C'
            elif self.degrees_selection.get() == 'Fahrenheit':
                temperature = temperature + ' °F'
            elif self.degrees_selection.get() == 'Kelvin':
                temperature = temperature + ' K'
        return temperature

    def prepare_weather_data(self, dates_openweather, temperatures_openweather, dates_in_pocasi, temperatures_in_pocasi, temperatures_yr, dates_yr):
        '''
        prepares weather data from different sources into one dictionary weather_data, which it returns
        :param dates_openweather: list
        :param temperatures_openweather: list
        :param dates_in_pocasi: list
        :param temperatures_in_pocasi: list
        :param temperatures_yr: list
        :param dates_yr: list
        '''
        weather_data = {}

        max_length = max(len(dates_in_pocasi), len(
            dates_openweather), len(dates_yr))
        print(max_length)

        if max_length == len(dates_yr):
            weather_data['dates'] = dates_yr
        elif max_length == len(dates_in_pocasi):
            weather_data['dates'] = dates_in_pocasi
        else:
            weather_data['dates'] = dates_in_pocasi

        weather_data['temperatures_openweather'] = temperatures_openweather
        weather_data['temperatures_in_pocasi'] = temperatures_in_pocasi
        weather_data['temperatures_yr'] = temperatures_yr
        weather_data['length'] = max_length

        weather_data['dates_openweather'] = dates_openweather
        weather_data['dates_in_pocasi'] = dates_in_pocasi
        weather_data['dates_yr'] = dates_yr

        return weather_data

    def fill_in_vectors(self, weather_data):
        '''
        uses fill_in_vector method to fill in lists in weather_data to length of the longest one
        :param weather_data: dict
        '''

        weather_data['temperatures_openweather'] = self.fill_in_vector(
            weather_data['temperatures_openweather'], weather_data['length'])

        weather_data['dates_openweather'] = self.fill_in_vector(
            weather_data['dates_openweather'], weather_data['length'])

        weather_data['temperatures_in_pocasi'] = self.fill_in_vector(
            weather_data['temperatures_in_pocasi'], weather_data['length'])
        weather_data['dates_in_pocasi'] = self.fill_in_vector(
            weather_data['dates_in_pocasi'], weather_data['length'])

        weather_data['temperatures_yr'] = self.fill_in_vector(
            weather_data['temperatures_yr'], weather_data['length'])
        weather_data['dates_yr'] = self.fill_in_vector(
            weather_data['dates_yr'], weather_data['length'])

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

    def plot_temperatures(self, weather_data):
        '''
        plots temperature forecasts in tkinter window
        :param weather_data: dictionary of lists
        '''
        num_temperatures, open_temperatures, in_pocasi_temperatures, date_open, date_in_pocasi = [], [], [], [], []

        num_temperatures = weather_data['temperatures_in_pocasi']

        for i in range(len(weather_data['temperatures_openweather'])):

            if weather_data['temperatures_openweather'][i] != 'NA':
                open_temperatures.append(
                    weather_data['temperatures_openweather'][i])
                date_open.append(weather_data['dates'][i])

        for i in range(len(weather_data['temperatures_in_pocasi'])):

            if weather_data['temperatures_in_pocasi'][i] != 'NA':
                in_pocasi_temperatures.append(
                    weather_data['temperatures_in_pocasi'][i])
                date_in_pocasi.append(weather_data['dates'][i])

        data = {'Date': date_in_pocasi,
                'In Počasí': in_pocasi_temperatures
                }
        data_open = {'Open Date': date_open,
                     'Open Počasí': open_temperatures
                     }
        data_yr = {'Yr_date': weather_data['dates'],
                   'Yr_temperature': weather_data['temperatures_yr']
                   }

        if self.degrees_selection.get() == 'Celsius':
            unit = '°C'
        elif self.degrees_selection.get() == 'Fahrenheit':
            unit = '°F'
        else:
            unit = 'K'
        figure = plt.Figure(figsize=(7.5, 3.9), dpi=100)

        line2 = FigureCanvasTkAgg(figure, self.root)
        line2.get_tk_widget().grid(row=9, column=0, columnspan=14, pady=10)

        plt.style.use('ggplot')

        ax2 = figure.add_subplot(111)

        ax2.set_xlabel('Date')
        ax2.set_ylabel(f'Temperature / {unit}')
        ax2.set_title('Temperature forecast')

        ax2.plot(data['Date'], data['In Počasí'],
                 color='r', marker="o", label='In Počasí')
        ax2.plot(data_open['Open Date'], data_open['Open Počasí'],
                 color='g', marker="o", label='Open weather')

        ax2.plot(data_yr['Yr_date'], data_yr['Yr_temperature'],
                 color='b', marker="o", label='Yr.no')

        ax2.legend()

    def get_data_openweather(self, place):
        '''
        get weather forecast data from openweather api and returns temperatures and dates lists
        :param place: str
        '''

        token = '3826180b6619b9e8655cd67a2fa30f52'
        url = 'http://api.openweathermap.org/data/2.5/forecast'

        parameters = {
            'APIKEY': token,
            'q': place,
            'units': 'metric'
        }

        api_request = requests.get(url, params=parameters)
        api_request = api_request.json()

        dates, temperatures = [], []
        for item in api_request['list']:
            date = item['dt']
            temperature = item['main']['temp']

            date = datetime.datetime.fromtimestamp(date)

            dates.append(date)
            temperatures.append(temperature)
            # used for exploring data
            '''
            print(date, '.'*int(temperature//1), temperature)
            print(date.strftime('%H'))
            '''

        ''' saving whole dataset from openweather to json file for exploring
        with open('weather.json', 'w') as file:
        json.dump(api_request, file, indent=4)
        '''

        temperatures, dates = self.prepare_api_data(
            temperatures, dates)

        return temperatures, dates

    def prepare_api_data(self, temperatures, dates):
        '''
        clears and prepares data from  api which has multiple temperatures per single day
        :param temperatures: list
        :param dates: list
        '''
        max_day_temperatures, prepared_dates = [], []

        sorted_temperatures = defaultdict(list)

        for i in range(len(dates)):
            sorted_temperatures[dates[i].strftime(
                '%d. %m.')].append(temperatures[i])

        for date in sorted_temperatures:
            max_day_temperatures.append((max(sorted_temperatures[date])))
            prepared_dates.append(date)

        today_date = (datetime.date.today())
        if prepared_dates[0] != today_date.strftime('%d. %m.'):
            prepared_dates.insert(0, 'NA')
            max_day_temperatures.insert(0, 'NA')

        return max_day_temperatures, prepared_dates

    def get_yr_data(self, place):
        '''
        get weather forecast data from yr weather api from selected place and returns temperatures and dates lists
        :param place: str
        '''
        ['Praha', 'Brno', 'Kvilda', 'Nová Paka']
        latslongs = {
            'Praha': {'lat': 50.5, 'long': 14.25},
            'Brno': {'lat': 49.20, 'long': 16.60},
            'Kvilda': {'lat': 49.02, 'long': 13.58},
            'Nová Paka': {'lat': 50.49, 'long': 15.52}
        }

        url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latslongs[place]['lat']}&lon={latslongs[place]['long']}"
        header = {
            "Accept": 'application/json',
            'User-Agent': 'weather app tryout https://github.com/Rutrle/Weather-app'
        }

        api_request = requests.get(url, headers=header)
        api_request = api_request.json()
        relevant_data = api_request['properties']['timeseries']

        temperatures, dates = [], []

        for weather_log in relevant_data:
            date = datetime.datetime.strptime(
                weather_log['time'], '%Y-%m-%dT%H:%M:%SZ')
            dates.append(date)
            temperatures.append(
                weather_log['data']['instant']['details']['air_temperature'])

        temperatures, dates = self.prepare_api_data(temperatures, dates)

        return temperatures, dates

    def get_in_pocasi_data(self, place):
        '''
        get weather forecast data for given place from in Počasí website and returns temperatures and dates lists
        :param place: str
        '''
        urls = {'Praha': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/praha/praha-324',
                'Kvilda': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/kvilda-4588/',
                'Brno': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/jihomoravsky/brno-25/',
                'Nová Paka': 'https://www.in-pocasi.cz/predpoved-pocasi/cz/kralovehradecky/nova-paka-271/'}

        url = urls[place]
        api_request = requests.get(url)
        soup = BeautifulSoup(api_request.content, 'html.parser')

        temperatures, dates = [], []

        actual_temp = soup.find(class_='alfa mb-1')
        actual_temp = actual_temp.text
        actual_temp = re.findall("-* *\d*\d\.*\d*", actual_temp)
        temperatures.append(float(actual_temp[0]))
        dates.append(datetime.date.today().strftime('%d. %m.'))

        indexes = ['day'+str(i) for i in range(1, 8)]
        for i in range(len(indexes)):
            try:
                results = soup.find(id=indexes[i])
                results = results.find(class_="mt-1 strong")
                results = float(
                    (re.findall("-* *\d*\d\.*\d*", results.text))[0])
                temperatures.append(results)
                date = datetime.date.today() + datetime.timedelta(days=(i+1))
                dates.append(date.strftime('%d. %m.'))

            except AttributeError:
                print(f"{indexes[i]} index was not found")

        return temperatures, dates

    def unit_conversion(self, weather_data):
        '''
        converse units of temperatures in weather_data dictionary according to selected units
        :param weather_data: dict
        '''
        units = self.degrees_selection.get()

        if units == 'Celsius':
            return weather_data

        elif units == 'Fahrenheit':
            weather_data['temperatures_in_pocasi'] = [
                round((T*1.8 + 32), 2) for T in weather_data['temperatures_in_pocasi']]
            weather_data['temperatures_openweather'] = [
                round((T*1.8 + 32), 2) for T in weather_data['temperatures_openweather']]
            weather_data['temperatures_yr'] = [
                round((T*1.8 + 32), 2) for T in weather_data['temperatures_yr']]

        elif units == 'Kelvin':
            weather_data['temperatures_in_pocasi'] = [
                round((T+273.15), 2) for T in weather_data['temperatures_in_pocasi']]
            weather_data['temperatures_openweather'] = [
                round((T+273.15), 2) for T in weather_data['temperatures_openweather']]
            weather_data['temperatures_yr'] = [
                round((T+273.15), 2) for T in weather_data['temperatures_yr']]

        return weather_data


if __name__ == "__main__":
    Weather_app()
