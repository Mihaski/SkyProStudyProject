import os
from typing import Optional

import requests

from utils import djecson_from_path

# url = "https://api.apilayer.com/exchangerates_data/convert?to=JPY&from=GBP&amount=1000"
# headers = {"apikey": "VISx1oa1zkcsDGvfGbhRHlJUXXGNoWuj"}
#
# response = requests.get(url, headers=headers)
#
# print(f"Status: {response.status_code}")
# print(f"Headers: {response.headers}")
# print(f"Response text: {response.text}")
#
# if response.status_code == 200:
#     data = response.json()
#     print(f"JSON: {data}")
#     print(f"Keys: {data.keys()}")
#     print(f"Result: {data.get('result')}")

# Получаем API ключ из переменных окружения
API_KEY = os.getenv('EXCHANGE_RATES_DATA_API_KEY')
BASE_URL = "https://api.apilayer.com"


def get_transaction_amount(transaction: dict) -> float:
    """ Возвращает сумму транзакции в рублях.
        Транзакция - моделька, тип python объекта словарь. """

    # Извлекаем сумму и валюту из транзакции
    amount = transaction['operationAmount']['amount']
    currency = transaction['operationAmount']['currency']['code']

    # Если валюта не указана или это рубли, возвращаем сумму без изменений
    if currency == 'RUB':
        return float(amount)

    # Для USD и EUR используем API для конвертации
    # if currency == 'USD' or currency == 'EUR':
    #     prep = convert_currency(amount, currency, 'RUB')
    #     return float(prep)

    # Код ошибки будет todo
    return -0.1


list_of_dict = djecson_from_path(r"D:\PyCharmCatalog\SkyProStudyProject\data\operations.json")

print(get_transaction_amount(list_of_dict[0]))
