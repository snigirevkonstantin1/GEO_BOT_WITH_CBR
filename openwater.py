import requests

def whater(latitude, longitude):
    api_key = '1b565d8876bfa86be8202fa97324dffa'
    r = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'lon': longitude, 'lat': latitude, 'type': 'like', 'units': 'metric', 'APPID': api_key})
    mydict = r.json()
    return (mydict['main']['temp'])

