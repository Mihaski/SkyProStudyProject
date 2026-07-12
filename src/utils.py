import json
import os
from json import JSONDecodeError


def has_non_digit_except_spaces(text):
    return any(not (c.isdigit() or c.isspace()) for c in text)


def write_or_print(message, filename):
    """Записывает сообщение в файл или выводит в консоль"""
    if filename != "stdout":
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message, end='')


def djecson_from_path(file_path: str) -> list[dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""

    # Проверяем существование файла
    if not os.path.exists(file_path):
        return ['check']

    # Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        return []

    # Преобразование из локального файла
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


    except JSONDecodeError:
        # Возвращаем пустой список при любой ошибке
        return []
