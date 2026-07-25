import os

import requests
from dotenv import load_dotenv

# Для первой загрузки в переменные среды os
load_dotenv()

# Получаем API ключ из переменных окружения
API_KEY = os.getenv("EXCHANGE_RATES_DATA_API_KEY")
BASE_URL = "https://api.apilayer.com"


def convert_currency(quantity: float, from_currency: str, to_currency: str = "RUB") -> float:
    """Конвертирует сумму из валюты from_currency в to_currency через внешнее API."""

    if not API_KEY:
        print("Предупреждение: API ключ не настроен. Конвертация недоступна.")
        # Код ошибки будет todo
        return -0.1

    try:
        url = f"{BASE_URL}/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={quantity}"
        headers = {"apikey": API_KEY}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("success"):
            result = data.get("result")
            # Для тестов по большей части кусок
            if result is not None:
                return float(result)
            else:
                print("Ошибка: в ответе API отсутствует поле 'results'")
                return -0.1
        else:
            error_msg = data.get("error", {}).get("info", "Неизвестная ошибка")
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
