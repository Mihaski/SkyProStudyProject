# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def psvm():
    print("Программа: Привет! Добро пожаловать в программу работы\n\
с банковскими транзакциями.\n\
Выберите необходимый пункт меню:\n\
1. Получить информацию о транзакциях из JSON-файла\n\
2. Получить информацию о транзакциях из CSV-файла\n\
3. Получить информацию о транзакциях из XLSX-файла\n")
    choose_menu = input("Пользователь: ")

    if choose_menu == "1":
        print("Программа: Для обработки выбран JSON-файл.")
    elif choose_menu == "2":
        print("Программа: Для обработки выбран CSV-файл.")
    elif choose_menu == "3":
        print("Программа: Для обработки выбран XLSX-файл.")
    else:
        print("Для продолжения запустите программу снова и выберите один из предложенных пунктов")

    while True:
        print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n\
        Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        second_choose_menu = input("Пользователь: ")
        up_second = second_choose_menu.upper()

        if up_second == "EXECUTED":
            print("Программа: Операции отфильтрованы по статусу \"EXECUTED\"")
            break
        elif up_second == "CANCELED":
            print("Программа: Операции отфильтрованы по статусу \"CANCELED\"")
            break
        elif up_second == "PENDING":
            print("Программа: Операции отфильтрованы по статусу \"PENDING\"")
            break
        else:
            print(f"Программа: Статус операции \"{second_choose_menu}\" недоступен.")

    print("Программа: Отсортировать операции по дате? Да/Нет")
    sel_sort = input("Пользователь: ")
    print("Программа: Отсортировать по возрастанию или по убыванию?")
    direct_sort = input("Пользователь: ")
    print("Программа: Выводить только рублевые транзакции? Да/Нет")
    only_rub_filter = input("Пользователь: ")
    print("Программа: Отфильтровать список транзакций по определенному слову\
в описании? Да/Нет")
    word_filter = input("Пользователь: ")





    pass


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    psvm()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
