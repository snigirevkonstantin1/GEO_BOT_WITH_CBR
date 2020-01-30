from openwater import whater
import requests
from bs4 import BeautifulSoup

def closest_metro(location):
    token1 = "21c338c5-4077-4dbc-a9a7-5d48b72a1e3e"
    lat = location.latitude
    lon = location.longitude
    temp = whater(lat, lon)
    url = requests.get("https://geocode-maps.yandex.ru/1.x/?apikey={}&format=xml&geocode={},{}&kind=metro&results=1"
                       .format(token1, lon, lat))
    try:
        soup1 = BeautifulSoup(url.text, 'lxml')
        metro_adres = soup1.premisename.text
        a = []
        b = []
        for i in (soup1.find_all("pos")):
            a.append(i.text.split(' '))
        for i in a[1]:
            b.append(i)
        metro_lat, metro_lon = b[0], b[1]
        return metro_adres, metro_lat, metro_lon, temp
    except Exception as e:
        metro_adres = "Кажется в вашем городе нет метро"
        metro_lat = lat
        metro_lon = lon
        return metro_adres, metro_lon, metro_lat, temp