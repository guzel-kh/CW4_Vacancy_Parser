import json
import os

import requests


def get_currencies(currency: str='RUB') -> dict:
    """
    Функция для получения курсов валют к рублю
    :param currency: название валюты курс к которому нужно получить
    :return: курсы доступных валют к рублю.
    """
    API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={'apikey': API_KEY})
    currencies = json.loads(response.text)
    return currencies['rates']
