import csv

from src.log_module import setup_logger

LOG_FILE_NAME = "pandas_module"
MODULE_NAME = "pandas_module"

logger_pandas = setup_logger(MODULE_NAME, LOG_FILE_NAME)


def get_transactions_from_csv(csv_file: str) -> list[dict]:
    """ Returns a list of transactions from a csv file."""
    logger_pandas.info(f"Вызов функции get_transactions_from_csv с аргументом: {csv_file}")

    transactions = []
    try:
        with open(csv_file) as op_file:
            csv_reader = csv.reader(op_file, delimiter=';')
            for row in csv_reader:
                transactions.append(row)
    except FileNotFoundError:
        logger_pandas.error(f"Ошибка файл не найден: вызов с параметром {csv_file}")
        return transactions
    except Exception:
        logger_pandas.error(f"Общая категория исключения: вызов с параметром {csv_file}")
        return transactions

    logger_pandas.info(f"Успешное завершение функции get_transactions_from_csv")
    return transactions
