# This is a sample Python script.
from generators import filter_by_currency, transaction_descriptions
from pandas_module import get_transactions_from_csv, get_transactions_from_xlsx
from processing import filter_by_state, sort_by_date, process_bank_search
from src.utils import djecson_from_path


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    """ главная функция - консольный интерфейс"""

    print("Программа: Привет! Добро пожаловать в программу работы\n\
с банковскими транзакциями.\n\
Выберите необходимый пункт меню:\n\
1. Получить информацию о транзакциях из JSON-файла\n\
2. Получить информацию о транзакциях из CSV-файла\n\
3. Получить информацию о транзакциях из XLSX-файла\n")
    method = input("Пользователь: ")

    # ломается если не выдать, основа поведения параметр
    while True:
        if method == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            transactions = djecson_from_path("data/operations.json")
            # print(transactions)
            break

        elif method == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            transactions = get_transactions_from_csv("data/transactions.csv")
            break

        elif method == "3":
            print("Программа: Для обработки выбран XLSX-файл.")
            transactions = get_transactions_from_xlsx("data/transactions.xlsx")
            break
        else:
            print("Для продолжения запустите программу снова и выберите один из предложенных пунктов")

    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n\
        Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status_filter = input("Пользователь: ")
        upper_second = status_filter.upper()

        if upper_second in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        else:
            print(f"Программа: Статус операции \"{status_filter}\" недоступен.")

    transactions = filter_by_state(transactions, upper_second)

    if input("Отсортировать операции по дате? Да/Нет\n").lower() == "да":
        direction = input(
            "Отсортировать по возрастанию или по убыванию?\n"
        ).lower()

        transactions = sort_by_date(
            transactions,
            sort_by_decrease=(direction == "по убыванию")
        )

    if input("Выводить только рублевые транзакции? Да/Нет\n").lower() == "да":
        # transactions = [
        #     t for t in transactions
        #     if t.get("operationAmount", {})
        #        .get("currency", {})
        #        .get("code") == "RUB"
        # ]
        # RUB обязательный хотя хотел или было заявлено что по умолчанию
        transactions = list(filter_by_currency(transactions, "RUB"))
        # print(transactions)

    if input("Отфильтровать список транзакций по слову в описании? Да/Нет\n").lower() == "да":
        word = input("Введите слово: ")
        transactions = process_bank_search(
            transactions,
            word
        )

    if not transactions:
        print(
            "Не найдено ни одной транзакции, "
            "подходящей под ваши условия фильтрации"
        )
        # выход из функции если ничего не подошло
        return

    print(f"Программа:\nВсего банковских операций в выборке: {len(transactions)}")

    transaction_descriptions_gena = transaction_descriptions(transactions)
    for transaction in transactions:
        prep_data = {}
        prep_description = next(transaction_descriptions_gena)
        prep_amount = transaction.get("amount")
        print(transaction)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
