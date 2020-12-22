from tkinter import *
from PIL import ImageTk, Image
import requests
import json

token = '3826180b6619b9e8655cd67a2fa30f52'
url = 'http://api.openweathermap.org/data/2.5/forecast'

parametry = {
    'APIKEY': token,
    'q': 'praha',
    'units': 'metric'
}

api_request = requests.get(url, params=parametry)
api_request = api_request.json()
print(json.dumps(api_request, indent=4))
with open('weather.json', 'w') as file:
    json.dump(api_request, file, indent=4)
    



class Weather_app:
    def __init__(self):
        print('Hello weather app')
        self.built_frame()

    def built_frame(self):
        '''creates basic frame for weather app'''
        root = Tk()
        root.title('Porovnání počasí')
        root.geometry('500x900')


if __name__ == "__main__":
    Weather_app()
