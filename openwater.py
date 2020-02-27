import requests
from secret_token import WHATER_TOKEN

def whater(latitude, longitude):
    api_key = 'WHATER_TOKEN'
    r = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'lon': longitude, 'lat': latitude, 'type': 'like', 'units': 'metric', 'APPID': api_key})
    mydict = r.json()
    return (mydict['main']['temp'])

