import re

from src.utils import has_non_digit_except_spaces


def get_mask_card_number(card_number: str) -> str:
    """Hide card number"""

    if has_non_digit_except_spaces(card_number):
        return "Ошибка: присутствуют буквы"

    if card_number == "":
        return "Ошибка: пустая ввод"

    prep_card_number = re.sub(r"\D", "", str(card_number))

    if len(prep_card_number) != 16:
        return "Ошибка: количество символов в номере больше или меньше"

    return f"{prep_card_number[0:4]} {prep_card_number[4:6]}** **** {prep_card_number[12:16]}"


def get_mask_account(account_number: str) -> str:
    """Hide account number"""

    if has_non_digit_except_spaces(account_number):
        return "Ошибка: присутствуют буквы"

    prep_account_number = re.sub(r"\D", "", str(account_number))

    if len(prep_account_number) < 4:
        return "Ошибка: номер счёта должен содержать минимум 4 цифры"

    return f"**{prep_account_number[-4:]}"
