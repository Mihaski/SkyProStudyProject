import json
import os
from json import JSONDecodeError

from src.external_api import convert_currency


def has_non_digit_except_spaces(text):
    return any(not (c.isdigit() or c.isspace()) for c in text)


def write_or_print(message, filename):
    """Записывает сообщение в файл или выводит в консоль"""
    if filename != "stdout":
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message)
    else:
        print(message, end="")


def djecson_from_path(file_path: str) -> list[dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""

    # Проверяем существование файла
    if not os.path.exists(file_path):
        return []

    # Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        return []

    # Преобразование из локального файла
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Гарантируем, что возвращаем список
            return data if isinstance(data, list) else []
    except JSONDecodeError, FileNotFoundError:
        # Возвращаем пустой список при любой ошибке
        return []


def get_transaction_amount(transaction: dict) -> float:
    """Возвращает сумму из транзакции в рублях.
    Транзакция - моделька, тип python объекта словарь."""

    # Извлекаем сумму и валюту из транзакции
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]

    # Если валюта не указана или это рубли, возвращаем сумму без изменений
    if currency == "RUB":
        return float(amount)

    # Для USD и EUR используем API для конвертации
    if currency == "USD" or currency == "EUR":
        prep = convert_currency(amount, currency, "RUB")
        return float(prep)

    # Код ошибки будет todo
    return -0.1
