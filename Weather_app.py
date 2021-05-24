import tkinter
import datetime
import requests
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WeatherApp:
    '''app for displaying weather forecast from multiple web sources'''

    def __init__(self):
        self.root = tkinter.Tk()

        self.root.title('Weather forecast comparison')
        self.root.geometry('820x620')

        user_input_frame = tkinter.Frame(
            self.root, height=200, width=820)
        user_input_frame.grid(row=0, column=0)
        self.fill_in_user_input_frame(user_input_frame)

        self.temperatures_table_frame = tkinter.Frame(
            self.root, height=200, width=820)
        self.temperatures_table_frame.grid(row=1, column=0)

        self.temperatures_graph_frame = tkinter.Frame(
            self.root, height=200, width=820)
        self.temperatures_graph_frame.grid(row=2, column=0)

        self.fill_in_weather_forecasts(self.place_selection.get())

        tkinter.Button(self.root, text="Close", command=self.root.destroy).grid(
            row=99, column=0, columnspan=1, padx=10, pady=10)

        self.root.mainloop()

    def fill_in_weather_forecasts(self, place):
        """
        fills weather forecast info for given place both as table and as graph  to the tkinter window, also used when button get temperatures is pressed
        :param place: str
        """
        weather_forecast = GetWeatherForecasts(place)
        weather_data = weather_forecast.weather_data

        self.fill_in_temperatures_table(
            self.temperatures_table_frame, weather_data)
        self.fill_in_graph(self.temperatures_graph_frame, weather_data)

    def fill_in_user_input_frame(self, frame):
        """
        fills in input tools for user to frame
        :param frame: tkinter frame  object
        """
        tkinter.Label(frame, text='City:').grid(
            row=0, column=0, pady=20, padx=20)

        place_options = ['Praha', 'Brno', 'Kvilda', 'Nová Paka']
        self.place_selection = tkinter.StringVar()
        self.place_selection.set(place_options[0])
        tkinter.OptionMenu(frame, self.place_selection,
                           *place_options).grid(row=0, column=1, pady=20, padx=20)

        tkinter.Label(frame, text='Units:').grid(
            row=0, column=2, pady=20, padx=20)

        degrees_options = ['Celsius', 'Fahrenheit', 'Kelvin']
        self.degrees_selection = tkinter.StringVar()
        self.degrees_selection.set(degrees_options[0])
        tkinter.OptionMenu(frame, self.degrees_selection,
                           *degrees_options).grid(row=0, column=3, pady=20, padx=20)

        tkinter.Button(frame, text="get temperatures", command=lambda: self.fill_in_weather_forecasts(self.place_selection.get())).grid(
            row=0, column=4, pady=20, padx=20)

    def fill_in_temperatures_table(self, frame, weather_data):
        '''
        creates table showing temperatures in given frame
        :param frame: tkinter frame obj
        :param weather_data: dictionary
        '''
        tkinter.Label(frame, text='Openweather').grid(row=1, column=0, padx=20)
        tkinter.Label(frame, text='In Počasí').grid(row=2, column=0)
        tkinter.Label(frame, text='Yr.no').grid(row=3, column=0)

        weather_data = self.unit_conversion(weather_data)
        print(weather_data['length'])
        self.fill_in_days(weather_data, frame)

    def fill_in_days(self, weather_data, frame):
        '''
        fill in informations for all days
        :param weather_data: dictionary of lists
        :param frame: tkinter frame obj
        '''
        self.days_labels = []
        for index in range(weather_data['length']):
            day_position = index+1

            tkinter.Label(frame, text=weather_data['dates'][index]).grid(
                row=0, column=day_position, columnspan=1, padx=10)

            open_temperature = self.add_degrees_symbol(
                str(weather_data['temperatures_openweather'][index]))
            in_temperature = self.add_degrees_symbol(
                str(weather_data['temperatures_in_pocasi'][index]))
            yr_temperature = self.add_degrees_symbol(
                str(weather_data['temperatures_yr'][index]))

            tkinter.Label(frame, text=(open_temperature), width=5).grid(
                row=1, column=day_position, columnspan=1)
            tkinter.Label(frame, text=(in_temperature), width=5).grid(
                row=2, column=day_position, columnspan=1)
            tkinter.Label(frame, text=(yr_temperature), width=5).grid(
                row=3, column=day_position, columnspan=1)

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

    def fill_in_graph(self, frame, weather_data):
        """
        display temperature forecasts graph in a given frame
        :param frame: tkinter frame obj
        :param weather_data: dict
        """

        weather_data = self.unit_conversion(weather_data)
        self.plot_temperatures(frame, weather_data)

    def plot_temperatures(self, frame, weather_data):
        '''
        plots temperature forecasts in tkinter window
        :param weather_data: dictionary of lists
        '''
        open_temperatures, in_pocasi_temperatures, date_open, date_in_pocasi, date_yr, yr_temperatures = [], [], [], [], [], []

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

        for i in range(len(weather_data['temperatures_yr'])):
            if weather_data['temperatures_yr'][i] != 'NA':
                yr_temperatures.append(
                    weather_data['temperatures_yr'][i])
                date_yr.append(weather_data['dates'][i])

        data = {'Date': date_in_pocasi,
                'In Počasí': in_pocasi_temperatures
                }
        data_open = {'Open Date': date_open,
                     'Open Počasí': open_temperatures
                     }
        data_yr = {'Yr_date': date_yr,
                   'Yr_temperature': yr_temperatures
                   }

        if self.degrees_selection.get() == 'Celsius':
            unit = '°C'
        elif self.degrees_selection.get() == 'Fahrenheit':
            unit = '°F'
        else:
            unit = 'K'
        figure = plt.Figure(figsize=(7.5, 3.9), dpi=100)

        line2 = FigureCanvasTkAgg(figure, frame)
        line2.get_tk_widget().grid(row=0, column=0, pady=10, padx=20)

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

    def unit_conversion(self, weather_data):
        '''
        converse units of temperatures in weather_data dictionary according to selected units
        :param weather_data: dict
        '''
        units = self.degrees_selection.get()
        print(weather_data)
        if units == 'Celsius':
            return weather_data

        elif units == 'Fahrenheit':
            for i in range(len(weather_data['temperatures_in_pocasi'])):
                if isinstance(weather_data['temperatures_in_pocasi'][i], str):
                    pass
                else:
                    weather_data['temperatures_in_pocasi'][i] = round(
                        (weather_data['temperatures_in_pocasi'][i]*1.8 + 32), 2)

            for i in range(len(weather_data['temperatures_openweather'])):
                if isinstance(weather_data['temperatures_openweather'][i], str):
                    pass
                else:
                    weather_data['temperatures_openweather'][i] = round(
                        (weather_data['temperatures_openweather'][i]*1.8 + 32), 2)

            for i in range(len(weather_data['temperatures_yr'])):
                if isinstance(weather_data['temperatures_yr'][i], str):
                    pass
                else:
                    weather_data['temperatures_yr'][i] = round(
                        (weather_data['temperatures_yr'][i]*1.8 + 32), 2)

        elif units == 'Kelvin':
            for i in range(len(weather_data['temperatures_in_pocasi'])):
                if isinstance(weather_data['temperatures_in_pocasi'][i], str):
                    pass
                else:
                    weather_data['temperatures_in_pocasi'][i] = round(
                        (weather_data['temperatures_in_pocasi'][i]+273.15), 2)

            for i in range(len(weather_data['temperatures_openweather'])):
                if isinstance(weather_data['temperatures_openweather'][i], str):
                    pass
                else:
                    weather_data['temperatures_openweather'][i] = round(
                        (weather_data['temperatures_openweather'][i]+273.15), 2)

            for i in range(len(weather_data['temperatures_yr'])):
                if isinstance(weather_data['temperatures_yr'][i], str):
                    pass
                else:
                    weather_data['temperatures_yr'][i] = round(
                        (weather_data['temperatures_yr'][i]+273.15), 2)

        print(weather_data)
        return weather_data


class GetWeatherForecasts:
    """
    class for getting weather forecast from multiple sources
    """

    def __init__(self, place):
        self.weather_data = self.get_weather_data(place)

    def get_weather_data(self, place):
        '''
        collects weather data for given place from all sources and returns them in dictionary of lists
        :param place: str
        '''
        temperatures_openweather, dates_openweather = self.get_data_openweather(
            place)
        temperatures_in_pocasi, dates_in_pocasi = self.get_in_pocasi_data(
            place)
        temperatures_yr, dates_yr = self.get_yr_data(
            place)

        weather_data = self.prepare_weather_data(
            dates_openweather, temperatures_openweather, dates_in_pocasi, temperatures_in_pocasi, temperatures_yr, dates_yr)
        print(weather_data)
        weather_data = self.fill_in_vectors(weather_data)

        return weather_data

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
            if(dates[i] >= datetime.datetime.today()):
                sorted_temperatures[dates[i].strftime(
                    '%d. %m.')].append(temperatures[i])

        for date in sorted_temperatures:
            max_day_temperatures.append((max(sorted_temperatures[date])))
            prepared_dates.append(date)

        today_date = (datetime.date.today())
        if prepared_dates[0] != today_date.strftime('%d. %m.'):
            prepared_dates.insert(0,  today_date.strftime('%d. %m.'))
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

    def fill_in_vectors(self, weather_data):
        '''
        uses fill_in_vector method to fill in lists in weather_data to length of the longest one
        :param weather_data: dict
        '''
        for key in weather_data:
            if key != 'length':
                while len(weather_data[key]) < weather_data['length']:
                    weather_data[key].append('NA')

        return weather_data


if __name__ == "__main__":
    WeatherApp()
