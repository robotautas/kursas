import csv
import requests
from os import environ

ip_api_url = 'https://freegeoip.app/json/'
weather_url = 'http://api.openweathermap.org/data/2.5/weather/'
API_key = environ.get('OpenWeather')

ip_list = ['122.35.203.161', '174.217.10.111', '187.121.176.91', '176.114.85.116', '174.59.204.133', '54.209.112.174', '109.185.143.49', '176.114.253.216', '210.171.87.76', '24.169.250.142']

def get_city_country(ip_address):
    res = requests.get(f'{ip_api_url}{ip_address}').json()
    return res['ip'], res['country_name'], res['city'], res['latitude'], res['longitude']

def get_weather(lat, lon):
    payload = {'lat': lat, 'lon': lon, 'units': 'metric', 'appid': API_key}
    r = requests.get(f'{weather_url}', params=payload)
    res = r.json()
    return res['main']['temp'], res['weather'][0]['main']

def get_all(ip_address):
    geo = get_city_country(ip_address)
    meteo = get_weather(geo[3], geo[4])
    return geo[:3] + meteo

def make_csv(list_of_ips):
    with open('ip_data.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['IP', 'Country', 'City', 'Temp', 'Weather'])
        for ip in list_of_ips:
            writer.writerow(get_all(ip))

make_csv(ip_list)


