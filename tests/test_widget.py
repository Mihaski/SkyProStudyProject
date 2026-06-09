import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("account_info, expected", [
    # Тесты для карт
    ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),

    # Тесты для счетов
    ("Счет 73654108430135874305", "Счет **4305"),
    ("счет 12345678901234567890", "счет **7890"),

    # Тесты с ошибками
    ("", "Ошибка: пустой ввод"),
    ("   ", "Ошибка: пустой ввод"),
    ("Visa\n7000792289606361", "Ошибка: некорректный ввод (содержит перенос строки)"),
    ("Visa Platinum Gold 1234567890123456", "Ошибка: некорректный ввод (слишком много подстрок)"),
    ("Visa 7000A792289606361", "Ошибка: присутствуют буквы"),
    ("Счет 7365410843A5874305", "Ошибка: присутствуют буквы"),
    ("Visa 123", "Ошибка: количество символов в номере больше или меньше"),
    ("Счет 123", "Ошибка: номер счёта должен содержать минимум 4 цифры"),
])
def test_mask_account_card(account_info, expected):
    """Тест для маскировки счета или карты"""
    assert mask_account_card(account_info) == expected


@pytest.mark.parametrize("unformatted_date, expected", [
    # Корректные даты
    ("2024-12-25T12:34:56", "25.12.2024"),
    ("2023-01-01T00:00:00", "01.01.2023"),

    # Дополнительные форматы, которые функция успешно обрабатывает
    ("2024/12/25T12:34:56", "25.12.2024"),

    # Неверные даты (вызывают ValueError)
    ("2024-13-25T12:34:56", ValueError),
    ("2024-12-32T12:34:56", ValueError),
    ("2023-02-29T12:34:56", ValueError),

    # Неверный формат (вызывают ValueError)
    ("25-12-2024T12:34:56", ValueError),
    ("20241225T123456", ValueError),

    #Отсутсвует дата
    ("", ValueError),
    ("фывфывфывфыв", ValueError),
    ("232323232323", ValueError),
])
def test_get_date(unformatted_date, expected):
    """Тест для форматирования даты"""

    if expected is ValueError:
        with pytest.raises(ValueError):
            get_date(unformatted_date)
    else:
        assert get_date(unformatted_date) == expected
