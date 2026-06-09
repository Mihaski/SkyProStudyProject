import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def test_output_fixture():
    return "Ошибка"


@pytest.mark.parametrize("card_number, expected", [
    ("7000 7922 8960 6361", "7000 79** **** 6361"),
    ("7000792289606361", "7000 79** **** 6361"),
    ("70as7asd896063as", "Ошибка: присутствуют буквы"),
    ("7000792289606361123123123", "Ошибка: количество символов в номере больше или меньше"),
    ("", "Ошибка: пустая ввод"),
])
def test_get_mask_card_number(card_number, expected):
    """тест для номера карты"""

    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_invalid(test_output_fixture):
    assert test_output_fixture in get_mask_card_number("7000792223")


@pytest.mark.parametrize("account_number, expected", [
    ("73654108430135874305", "**4305"),
    ("736541sss3013587430a", "Ошибка: присутствуют буквы"),
    ("", "Ошибка: номер счёта должен содержать минимум 4 цифры"),
])
def test_get_mask_account(account_number, expected):
    """Тесты для номера счета"""
    assert get_mask_account(account_number) == expected


def test_get_mask_account_invalid(test_output_fixture):
    """Тесты для номера счета"""
    assert test_output_fixture in get_mask_account("asdasdas")
