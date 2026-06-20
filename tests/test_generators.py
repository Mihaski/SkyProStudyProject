from typing import Generator

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904416",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
    ]


def test_filter_by_currency_pass(sample_transactions):
    """Тест фильтрации USD транзакций"""
    usd_transactions = filter_by_currency(sample_transactions, "USD")

    # Проверяем тип возвращаемого значения
    assert isinstance(usd_transactions, Generator)

    # Получаем список транзакций
    transactions_list = list(usd_transactions)

    # Должно быть 2 USD транзакции
    assert len(transactions_list) == 2

    # Проверяем первую транзакцию
    assert transactions_list[0]["id"] == 939719570
    assert transactions_list[0]["operationAmount"]["currency"]["name"] == "USD"

    # Проверяем вторую транзакцию
    assert transactions_list[1]["id"] == 142264268
    assert transactions_list[1]["operationAmount"]["currency"]["name"] == "USD"


def test_filter_by_currency_fail(sample_transactions):
    """Тест фильтрации несуществующей валюты"""
    gbp_transactions = filter_by_currency(sample_transactions, "GBP")

    gbp_list = list(gbp_transactions)

    # Должно быть 0 транзакций
    assert len(gbp_list) == 0


def test_empty_transactions_list():
    """Тест с пустым списком транзакций"""
    empty_transactions = filter_by_currency([], "USD")

    assert list(empty_transactions) == []


def test_get_descriptions(sample_transactions):
    """Тест получения описаний транзакций"""
    descriptions = transaction_descriptions(sample_transactions)

    assert isinstance(descriptions, Generator)

    descriptions_list = list(descriptions)

    # Проверяем количество описаний
    assert len(descriptions_list) == 4

    # Проверяем содержимое
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
    ]

    assert descriptions_list == expected_descriptions


def test_get_descriptions_empty():
    """Тест с пустым списком транзакций"""
    descriptions = transaction_descriptions([])

    assert list(descriptions) == []


def test_descriptions_lazy_evaluation(sample_transactions):
    """Тест ленивых вычислений генератора описаний"""
    descriptions = transaction_descriptions(sample_transactions)

    # Пошаговое получение значений
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"

    # Проверяем исчерпание генератора
    with pytest.raises(StopIteration):
        next(descriptions)


def test_generate_single_card():
    """Тест генерации одной карты"""
    generator = card_number_generator(1, 1)

    card = next(generator)

    assert card == "0000 0000 0000 0001"

    with pytest.raises(StopIteration):
        next(generator)


def test_generate_range_from_1_to_5():
    """Тест генерации карт с 1 по 5"""
    generator = card_number_generator(1, 5)

    expected_cards = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]

    for expected in expected_cards:
        assert next(generator) == expected

    with pytest.raises(StopIteration):
        next(generator)


def test_generate_cards_with_leading_zeros():
    """Тест генерации карт с ведущими нулями"""
    generator = card_number_generator(10, 12)

    assert next(generator) == "0000 0000 0000 0010"
    assert next(generator) == "0000 0000 0000 0011"
    assert next(generator) == "0000 0000 0000 0012"


def test_generate_large_numbers():
    """Тест генерации больших номеров"""
    generator = card_number_generator(9999999999999990, 9999999999999995)

    expected = [
        "9999 9999 9999 9990",
        "9999 9999 9999 9991",
        "9999 9999 9999 9992",
        "9999 9999 9999 9993",
        "9999 9999 9999 9994",
        "9999 9999 9999 9995",
    ]

    for expected_card in expected:
        assert next(generator) == expected_card


def test_card_number_format():
    """Тест правильного формата номера карты"""
    generator = card_number_generator(1234567890123456, 1234567890123456)

    card = next(generator)

    # Проверяем формат: 4 группы по 4 цифры
    parts = card.split()
    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)
    assert all(part.isdigit() for part in parts)
    assert card == "1234 5678 9012 3456"


def test_card_number_max_value():
    """Тест генерации максимального номера карты"""
    generator = card_number_generator(9999999999999999, 9999999999999999)

    card = next(generator)

    assert card == "9999 9999 9999 9999"


def test_card_number_min_value():
    """Тест генерации минимального номера карты"""
    generator = card_number_generator(1, 1)

    card = next(generator)

    assert card == "0000 0000 0000 0001"


def test_card_number_lazy_evaluation():
    """Тест ленивых вычислений генератора"""
    generator = card_number_generator(1, 1000000)

    # Генератор не должен создавать все числа сразу
    first = next(generator)
    assert first == "0000 0000 0000 0001"

    second = next(generator)
    assert second == "0000 0000 0000 0002"


def test_card_number_same_start_end():
    """Тест когда start == end"""
    generator = card_number_generator(42, 42)

    cards = list(generator)

    assert len(cards) == 1
    assert cards[0] == "0000 0000 0000 0042"


# Параметризованный тест для разных диапазонов
@pytest.mark.parametrize(
    "start,end,expected",
    [
        (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (100, 102, ["0000 0000 0000 0100", "0000 0000 0000 0101", "0000 0000 0000 0102"]),
        (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"]),
    ],
)
def test_generator_various_ranges(start, end, expected):
    """Параметризованный тест для разных диапазонов"""
    generator = card_number_generator(start, end)
    results = list(generator)
    assert results == expected


def test_filter_by_currency_with_missing_key():
    """Тест обработки транзакций без ключа 'currency'"""
    # Создаем транзакцию с неправильной структурой
    bad_transactions = [
        {
            "id": 999999,
            "description": "Bad transaction",
            # Нет поля operationAmount или currency
        },
        {
            "id": 888888,
            "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Good transaction",
        },
    ]

    # Функция должна пропустить плохую транзакцию и вернуть только хорошую
    result = filter_by_currency(bad_transactions, "USD")
    result_list = list(result)

    assert len(result_list) == 1
    assert result_list[0]["id"] == 888888


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
