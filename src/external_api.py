import os

import requests
from dotenv import load_dotenv

# from utils import djecson_from_path

# Для первой загрузки в переменные среды os
load_dotenv()

# Получаем API ключ из переменных окружения
API_KEY = os.getenv('EXCHANGE_RATES_DATA_API_KEY')
BASE_URL = "https://api.apilayer.com"


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

def convert_currency(quantity: float, from_currency: str, to_currency: str = "RUB") -> float:
    """ Конвертирует сумму из валюты from_currency в to_currency через внешнее API. """

    if not API_KEY:
        print("Предупреждение: API ключ не настроен. Конвертация недоступна.")
        # Код ошибки будет todo
        return -0.1

    try:
        url = f"{BASE_URL}/exchangerates_data/convert?to={from_currency}&from={to_currency}&amount={quantity}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get('success'):
            results = data.get('results')
            # Для тестов по большей части кусок
            if results is not None:
                return float(results)
            else:
                print("Ошибка: в ответе API отсутствует поле 'results'")
                return -0.1
        else:
            error_msg = data.get('error', {}).get('info', 'Неизвестная ошибка')
            print(f"Ошибка API: {error_msg}")
            return -0.1

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        # Код ошибки будет todo
        return -0.1
    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка при обработке ответа API: {e}")
        # Код ошибки будет todo
        return -0.1

#
# list_of_dict = djecson_from_path(r"D:\PyCharmCatalog\SkyProStudyProject\data\operations.json")
#
# print(get_transaction_amount(list_of_dict[0]))
