import csv

import pandas as pd

from src.log_module import setup_logger

LOG_FILE_NAME = "pandas_module"
MODULE_NAME = "pandas_module"

logger_pandas = setup_logger(MODULE_NAME, LOG_FILE_NAME)


def get_transactions_from_csv(csv_file: str) -> list[dict]:
    """ Returns a list of transactions from a csv file."""
    logger_pandas.info(f"Вызов функции get_transactions_from_csv с аргументом: {csv_file}")

    transactions = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as op_file:
            csv_reader = csv.DictReader(op_file, delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                transactions.append(row)
    except FileNotFoundError:
        logger_pandas.error(f"Ошибка файл не найден: вызов с параметром {csv_file}")
        return transactions
    except Exception as e:
        logger_pandas.error(f"Общая категория исключения {e}: вызов с параметром {csv_file}")
        return transactions

    logger_pandas.info(f"Успешно загружено {len(transactions)} транзакций из {csv_file}")
    return transactions


def get_transactions_from_xlsx(excel_file: str) -> list[dict]:
    """ Returns a list of transactions from an xlsx file."""
    logger_pandas.info(f"Вызов функции get_transactions_from_exls с аргументом: {excel_file}")

    # внимание s
    transactions = []
    try:
        # only xlsx
        excel_data = pd.read_excel(excel_file, engine='openpyxl')

        # Проверка на пустой DataFrame
        if excel_data.empty:
            logger_pandas.warning(f"Файл {excel_file} пуст или не содержит данных")
            return transactions

        for index, row in excel_data.iterrows():
            # Внимание нет s
            transaction = {}
            for column in excel_data.columns:
                value = row[column]
                # Проверяем, не является ли значение NaN (пустым)
                if pd.isna(value):
                    transaction[column] = None
                else:
                    transaction[column] = value
            transactions.append(transaction)

    except FileNotFoundError:
        logger_pandas.error(f"Ошибка файл не найден: вызов с параметром {excel_file}")
        return transactions
    except Exception as e:
        logger_pandas.error(f"Общая категория исключения {e}: вызов с параметром {excel_file}")
        return transactions
    logger_pandas.info(f"Успешно загружено {len(transactions)} транзакций из {excel_file}")

    return transactions
