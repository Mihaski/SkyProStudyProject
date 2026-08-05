import pytest

from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations


# тесты для process_bank_operations

def test_process_bank_operations_exact_match():
    """ точное совпадение категорий"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Покупка в магазине"},
    ]
    categories = ["Перевод организации", "Открытие вклада"]

    result = process_bank_operations(data, categories)

    expected = {"Перевод организации": 2, "Открытие вклада": 1}
    assert result == expected


def test_process_bank_operations_partial_match():
    """ частичное совпадение (благодаря re.search)"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Перевод со счета на счет"},
        {"description": "Открытие вклада"},
    ]
    categories = ["Перевод", "Открытие"]

    result = process_bank_operations(data, categories)

    expected = {"Перевод": 3, "Открытие": 1}
    assert result == expected


def test_process_bank_operations_empty_data():
    """ пустой список транзакций"""
    data = []
    categories = ["Перевод", "Открытие"]

    result = process_bank_operations(data, categories)

    expected = {"Перевод": 0, "Открытие": 0}
    assert result == expected


def test_process_bank_operations_empty_categories():
    """ пустой список категорий"""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    categories = []

    result = process_bank_operations(data, categories)

    assert result == {}


def test_process_bank_operations_missing_description():
    """ транзакция без поля description"""
    data = [
        {"description": "Перевод организации"},
        {"id": 1, "amount": 100},  # Нет description
        {"description": "Открытие вклада"},
        {"id": 2, "amount": 200},  # Нет description
    ]
    categories = ["Перевод организации", "Открытие вклада"]

    result = process_bank_operations(data, categories)

    expected = {"Перевод организации": 1, "Открытие вклада": 1}
    assert result == expected


def test_process_bank_operations_empty_description():
    """ пустое поле description"""
    data = [
        {"description": "Перевод организации"},
        {"description": ""},  # Пустое описание
        {"description": "Открытие вклада"},
    ]
    categories = ["Перевод организации", "Открытие вклада"]

    result = process_bank_operations(data, categories)

    expected = {"Перевод организации": 1, "Открытие вклада": 1}
    assert result == expected


def test_process_bank_operations_no_matches():
    """ нет совпадений с категориями."""
    data = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    categories = ["Покупка", "Оплата"]

    result = process_bank_operations(data, categories)

    expected = {"Покупка": 0, "Оплата": 0}
    assert result == expected


def test_process_bank_operations_case_sensitive():
    """ учитывается регистр (re.search чувствителен к регистру)"""
    data = [
        {"description": "Перевод организации"},
        {"description": "перевод организации"},  # С маленькой буквы
        {"description": "ПЕРЕВОД ОРГАНИЗАЦИИ"},  # Все заглавные
    ]
    categories = ["Перевод организации"]

    result = process_bank_operations(data, categories)

    # Найдёт только точное совпадение с учётом регистра
    expected = {"Перевод организации": 1}
    assert result == expected


def test_process_bank_operations_special_characters():
    """ специальные символы в категориях"""
    data = [
        {"description": "Перевод (организации)"},
        {"description": "Перевод [организации]"},
        {"description": "Перевод {организации}"},
    ]
    categories = [r"Перевод \(организации\)", r"Перевод \[организации\]"]

    result = process_bank_operations(data, categories)

    expected = {r"Перевод \(организации\)": 1, r"Перевод \[организации\]": 1}
    assert result == expected


def test_process_bank_operations_multiple_categories_one_transaction():
    """ одна транзакция может попасть в несколько категорий"""
    data = [
        {"description": "Перевод организации"},  # Подходит под обе категории
    ]
    categories = ["Перевод", "Перевод организации"]

    result = process_bank_operations(data, categories)

    # Так как у вас нет break, транзакция засчитается в обе категории
    expected = {"Перевод": 1, "Перевод организации": 1}
    assert result == expected


# тесты для process_bank_search

@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "date": "2019-08-26T10:50:58.294041",
        },
        {
            "id": 2,
            "description": "Покупка в магазине",
            "date": "2019-08-26T10:50:58.294041",
        },
        {
            "id": 3,
            "description": "Перевод на карту",
            "date": "2019-08-26T10:50:58.294041",
        },
        {
            "id": 4,
            "description": "Оплата коммунальных услуг",
            "date": "2019-08-26T10:50:58.294041",
        },
        {
            "id": 5,
            "description": "Перевод между счетами",
            "amount": 10000.00,
        }
    ]


def test_process_bank_search_found(sample_transactions):
    """Тест успешного поиска транзакций."""
    result = process_bank_search(sample_transactions, "Перевод")

    assert len(result) == 3
    assert all("Перевод" in t["description"] for t in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3
    assert result[2]["id"] == 5


def test_process_bank_search_not_found(sample_transactions):
    """Тест, когда ничего не найдено."""
    result = process_bank_search(sample_transactions, "несуществующая строка")

    assert result == []
    assert isinstance(result, list)


def test_process_bank_search_empty_data():
    """Тест с пустым списком транзакций."""
    result = process_bank_search([], "перевод")

    assert result == []
    assert isinstance(result, list)


def test_process_bank_search_empty_query(sample_transactions):
    """Тест с пустым поисковым запросом."""
    result = process_bank_search(sample_transactions, "")

    assert result == []

    result = process_bank_search(sample_transactions, "   ")
    assert result == []


def test_process_bank_search_description_missing():
    """Тест с транзакцией без описания."""
    transactions = [
        {"id": 1, "description": "Перевод", "amount": 100},
        {"id": 2, "amount": 200},  # Нет description
        {"id": 3, "description": "Ещё перевод", "amount": 300},
    ]

    result = process_bank_search(transactions, "Перевод")

    assert len(result) == 1
    assert result[0]["id"] == 1


def test_process_bank_search_special_characters():
    """Тест поиска со спецсимволами - функция НЕ экранирует их."""
    transactions = [
        {"description": "Перевод (организация)", "id": 1},
        {"description": "Перевод [важно]", "id": 2},
        {"description": "Перевод + налог", "id": 3},
    ]

    result = process_bank_search(transactions, "Перевод")
    assert len(result) == 3

    # Ищем часть слова
    result = process_bank_search(transactions, "важно")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_process_bank_search_partial_match(sample_transactions):
    """Тест частичного совпадения."""
    result = process_bank_search(sample_transactions, "плат")

    assert len(result) == 1
    assert result[0]["id"] == 4  # "Оплата коммунальных услуг"


def test_process_bank_search_no_description_field():
    """Тест с транзакциями без поля description."""
    transactions = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]

    result = process_bank_search(transactions, "перевод")

    assert result == []


# тесты для processing

@pytest.fixture
def test_sample():
    return [
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state_fix(test_sample):
    assert filter_by_state(test_sample) == [
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.mark.parametrize(
    "state,expected",
    [
        (
                "EXECUTED",
                [
                    {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                ],
        ),
        (
                "CANCELED",
                [
                    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                ],
        ),
        ("INVALID", []),
    ],
)
def test_filter_by_state(test_sample, state, expected):
    assert filter_by_state(test_sample, state) == expected


def test_sort_by_date_up_to_down(test_sample):
    assert sort_by_date(test_sample) == [
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_sort_by_date_down_to_up(test_sample):
    assert sort_by_date(test_sample, False) == [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_sort_by_date_same_date():
    assert sort_by_date(
        [
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 939719512, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        ]
    ) == [
               {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
               {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
               {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
               {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
               {"id": 939719512, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
           ]


def test_sort_by_date_invalid_unstandard_date():
    # Первый тест
    assert sort_by_date(
        [
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719512, "state": "EXECUTED", "date": "20200630T020858425572"},
        ]
    ) == [
               {"id": 939719512, "state": "EXECUTED", "date": "20200630T020858425572"},
               {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
               {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
               {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
               {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
           ]

    # Второй тест
    assert sort_by_date(
        [
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719512, "state": "EXECUTED", "date": "22f0t6sT02s858425572"},
        ]
    ) == [
               {"id": 939719512, "state": "EXECUTED", "date": "22f0t6sT02s858425572"},
               {"id": 414288290, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
               {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
               {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
               {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
           ]
