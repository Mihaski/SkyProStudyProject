import re

from typing import Union


def get_mask_card_number(card_number: Union[str, None] = None) -> str:
    """Hide card number"""

    if card_number is None:
        return "Ошибка: пустой ввод"

    prep_card_number = re.sub(r'\D', '', str(card_number))

    if len(prep_card_number) != 16:
        return "Ошибка: количество символов в номере больше или меньше"

    return f"{prep_card_number[0:4]} {prep_card_number[4:6]}** **** {prep_card_number[12:16]}"


def get_mask_account(account_number: str) -> str:
    """Hide account number"""
    prep_account_number = re.sub(r'\D', '', str(account_number))

    if len(prep_account_number) < 4:
        return "Ошибка: номер счёта должен содержать минимум 4 цифры"

    return f"**{prep_account_number[-4:]}"
