from decorators import my_log

# Учебный проект написанный на Python в SkyPro

## Описание:

Учебный проект на python. Учусь кодить.

## Цель проекта:

Научиться грамоте используемой в среде python

## Установка:

1. Клонируйте репозиторий:

```
git clone https://github.com/Mihaski/SkyProStudyProject/tree/main
```

2. Проверьте подсказки...

## Использование:

1. Открывайте модуля и смотрите docstring.
2. Параметры анотированы, подбирайте аргументы соответсвенно.

## Примеры:

##### filter_by_state:

###### Выход функции со статусом по умолчанию 'EXECUTED'

[{'id': 414288290, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

###### Выход функции, если вторым аргументом передано 'CANCELED'

[{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

##### sort_by_date:

###### Выход функции (сортировка по убыванию, т. е. сначала самые последние операции)

[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

##### filter_by_currency:

Генератор, который фильтрует транзакции по валюте.

**Параметры:**

- `list_dict_transactions` - список словарей с транзакциями
- `currency` - код валюты для фильтрации (например, "USD", "EUR", "RUB")

**Возвращает:** Генератор, выдающий транзакции только с указанной валютой

**Пример использования:**

```python
from src.generators import filter_by_currency

transactions = [
    {
        "id": 939719570,
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации"
    },
    {
        "id": 873106923,
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "RUB", "code": "RUB"}
        },
        "description": "Перевод со счета на счет"
    }
]

# Получаем все USD транзакции
usd_transactions = filter_by_currency(transactions, "USD")

for transaction in usd_transactions:
    print(transaction["id"], transaction["description"])
# Вывод: 939719570 Перевод организации
```

##### transaction_descriptions:

Генератор, который извлекает описания из каждой транзакции.

Параметры:

list_dict_transactions - список словарей с транзакциями

Возвращает: Генератор, выдающий описание каждой транзакции

Пример использования:

```python
from src.generators import transaction_descriptions

transactions = [
    {"id": 1, "description": "Перевод организации"},
    {"id": 2, "description": "Оплата услуг"},
    {"id": 3, "description": "Пополнение счета"}
]

descriptions = transaction_descriptions(transactions)

for desc in descriptions:
    print(desc)
# Вывод:
# Перевод организации
# Оплата услуг
# Пополнение счета
```

##### card_number_generator:

Генератор, который создает номера банковских карт в формате XXXX XXXX XXXX XXXX.

Параметры:

start - начальное значение диапазона (включительно)

stop - конечное значение диапазона (включительно)

Возвращает: Генератор, выдающий номера карт в форматированном виде

Пример использования:

```python
from src.generators import card_number_generator

# Генерация первых пяти номеров карт
for card_number in card_number_generator(1, 5):
    print(card_number)

# Вывод:
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005

# Генерация конкретного номера
card = list(card_number_generator(1234567890123456, 1234567890123456))
print(card[0])  # 1234 5678 9012 3456
```

##### decorators

my_log

Декоратор для логирования функций

Необязательный параметр имя файла

Пример использования:

```python
@my_log()
def card_number():
    pass


@my_log("file.txt")
def card_number():
    pass
```

##### pandas_module

модуль с функциями получения транзакций из csv и xlsx

обе функции принимают один параметр путь файла
```python
def get_transactions_from_csv(csv_file: str) -> list[dict]:
    transactions: list[dict] = []
    ...
    return transactions


def get_transactions_from_xlsx(excel_file: str) -> list[dict]:
    transactions: list[dict] = []
    ...
    return transactions
```


## Тесты:

Написано 284 тестов, покрывают 92% функций в проекте на 30 июля 26 года