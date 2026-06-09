from masks import get_mask_card_number


def test_get_mask_card_number():
    """тест для номера карты"""

    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"

    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"

    assert get_mask_card_number("") == "Ошибка: количество символов в номере больше или меньше"

    assert get_mask_card_number() == "Ошибка: пустой ввод"


def test_get_mask_account():
    pass
