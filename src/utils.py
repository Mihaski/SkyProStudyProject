import json
import os
from json import JSONDecodeError

from src.external_api import convert_currency
from src.log_module import setup_logger

LOG_FILE_NAME = "utils"

logger_utils = setup_logger("utils", LOG_FILE_NAME)


def has_non_digit_except_spaces(text):
    logger_utils.debug(f"Проверка текста на наличие не цифровых символов: {text}")
    result = any(not (c.isdigit() or c.isspace()) for c in text)
    logger_utils.debug(f"Результат проверки: {result}")
    return result


def write_or_print(message, filename):
    """Записывает сообщение в файл или выводит в консоль"""
    logger_utils.info(f"Вызов функции write_or_print с filename: {filename}")

    if filename != "stdout":
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(message)
            logger_utils.info(f"Успешная запись в файл: {filename}")
        except Exception as e:
            logger_utils.error(f"Ошибка при записи в файл {filename}: {str(e)}")
    else:
        print(message, end="")
        logger_utils.info(
            f"Вывод в консоль: {message[:100]}..." if len(message) > 100 else f"Вывод в консоль: {message}")


def djecson_from_path(file_path: str) -> list[dict]:
    """Загружает данные о финансовых транзакциях из JSON-файла."""
    logger_utils.info(f"Вызов функции djecson_from_path с file_path: {file_path}")

    # Проверяем существование файла
    if not os.path.exists(file_path):
        logger_utils.warning(f"Файл не найден: {file_path}")
        return []

    # Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        logger_utils.warning(f"Файл пустой: {file_path}")
        return []

    # Преобразование из локального файла
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Гарантируем, что возвращаем список
            if isinstance(data, list):
                logger_utils.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
                return data
            else:
                logger_utils.warning(f"Данные в файле {file_path} не являются списком, тип: {type(data)}")
                return []
    except JSONDecodeError as e:
        logger_utils.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except Exception as e:
        logger_utils.error(f"Неизвестная ошибка при чтении файла {file_path}: {str(e)}")
        return []


def get_transaction_amount(transaction: dict) -> float:
    """Возвращает сумму из транзакции в рублях.
    Транзакция - моделька, тип python объекта словарь."""

    logger_utils.info(f"Вызов функции get_transaction_amount для транзакции: {transaction.get('id', 'unknown')}")

    try:
        # Извлекаем сумму и валюту из транзакции
        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["code"]

        logger_utils.debug(f"Сумма: {amount}, Валюта: {currency}")

        # Если валюта не указана или это рубли, возвращаем сумму без изменений
        if currency == "RUB":
            result = float(amount)
            logger_utils.info(f"Сумма в рублях: {result}")
            return result

        # Для USD и EUR используем API для конвертации
        if currency == "USD" or currency == "EUR":
            try:
                prep = convert_currency(amount, currency, "RUB")
                result = float(prep)
                logger_utils.info(f"Конвертировано из {currency} в RUB: {amount} -> {result}")
                return result
            except Exception as e:
                logger_utils.error(f"Ошибка конвертации валюты {currency}: {str(e)}")
                return -0.1

        logger_utils.warning(f"Неподдерживаемая валюта: {currency}")
        return -0.1

    except KeyError as e:
        logger_utils.error(f"Отсутствует ключ в транзакции: {str(e)}, транзакция: {transaction}")
        return -0.1
    except Exception as e:
        logger_utils.error(f"Неизвестная ошибка при обработке транзакции: {str(e)}")
        return -0.1
