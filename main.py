from tkinter import *
from tkinter import messagebox  # similar to prompt if wrong
from configparser import ConfigParser
import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'  # from api

config_file = 'config.ini'  # to extract api key
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

app = Tk()
app.title("Weather App")
app.geometry('700x350')
app.config(bg="mint cream")


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()  # get the details of city
        # we need data: city,country,temp_celsius,temp_fht,icon,weather
        city = json['name']
        country = json['sys']['country']  # sys parent tag, country child tag
        temp_kelvin = json['main']['temp']  # need to convert to required degree
        temp_celsius = temp_kelvin - 273.15
        temp_fht = (temp_kelvin - 273.15) * 9 / 5 + 32
        # icon downloading is problematic, so skip it
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_fht, weather)  # tuple
        return final
    else:
        return None


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{},{}'.format(weather[0], weather[1])
        # weather[0] - city, weather[1] - country
        temp_lbl['text'] = '{:.2f}C,{:.2f}F'.format(weather[2], weather[3])
        weather_lbl['text'] = '{}'.format(weather[4])
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))


city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text='Search Weather', width=12, font=('bold', 11), command=search)
search_btn.pack()

location_lbl = Label(app, text='Location', font=('bold', 18), fg="purple")
location_lbl.pack()  # pack will display on screen

temp_lbl = Label(app, text='Temperature')
temp_lbl.pack()

weather_lbl = Label(app, text='Weather', fg="Green")
weather_lbl.pack()

app.mainloop()
