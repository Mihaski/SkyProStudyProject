import pytest

from masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card_number, expected", [
    ("7000 7922 8960 6361", "7000 79** **** 6361"),
    ("7000792289606361", "7000 79** **** 6361"),
    ("70as7asd896063as", "Ошибка: присутсвуют буквы"),
    ("7000792289606361123123123", "Ошибка: количество символов в номере больше или меньше"),
    ("", "Ошибка: пустая ввод"),
])
def test_get_mask_card_number(card_number, expected):
    """тест для номера карты"""

    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("account_number, expected", [
    ("73654108430135874305", "**4305"),
    ("736541sss3013587430a", "Ошибка: присутсвуют буквы"),
    ("", "Ошибка: номер счёта должен содержать минимум 4 цифры"),
])
def test_get_mask_account(account_number, expected):
    """Тесты для номера счета"""
    assert get_mask_account(account_number) == expected
