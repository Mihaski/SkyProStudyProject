import pytest

from src.processing import filter_by_state, sort_by_date, process_bank_search


# тесты для process_bank_search

@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "amount": 100.50,
        },
        {
            "id": 2,
            "description": "Покупка в магазине",
            "amount": 250.00,
        },
        {
            "id": 3,
            "description": "Перевод на карту",
            "amount": 500.00,
        },
        {
            "id": 4,
            "description": "Оплата коммунальных услуг",
            "amount": 1500.00,
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
