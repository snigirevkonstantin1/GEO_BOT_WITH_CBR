import requests
from bs4 import BeautifulSoup

currensi = ['AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD', 'DKK', 'USD', 'EUR', 'INR', 'KZT', 'CAD', 'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS', 'UAH', 'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY']

def check_currency_value(text):
    mydict = {}
    url1 = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    page = requests.get(url1)
    soup = BeautifulSoup(page.text, 'lxml')
    for tag in soup.find_all('valute'):
        mydict[tag.charcode.text] = tag.value.text
    for currency, value in mydict.items():
        if currency in text.upper():
            return currency, value
    return None, None

def check_currency_nominal(text):
    mydict = {}
    url1 = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    page = requests.get(url1)
    soup = BeautifulSoup(page.text, 'lxml')
    for tag in soup.find_all('valute'):
        mydict[tag.charcode.text] = tag.nominal.text
    for currency, value in mydict.items():
        if currency in text.upper():
            return value
    return None

