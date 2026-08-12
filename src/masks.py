import re

from src.log_module import setup_logger
from src.utils import has_non_digit_except_spaces

LOG_FILE_NAME = "masks"

logger_masks = setup_logger("masks", LOG_FILE_NAME)


def get_mask_card_number(card_number: str | None) -> str:
    """Hide card number"""

    logger_masks.info(f"Начало работы функции get_mask_card_number")

    if card_number is None:
        return ""

    logger_masks.info(f"Вызов функции get_mask_card_number с аргументом: {card_number}")

    if has_non_digit_except_spaces(card_number):
        error_msg = "Ошибка: присутствуют буквы"
        logger_masks.error(f"Ошибка: {error_msg}, входные данные: {card_number}")
        return error_msg

    if card_number == "":
        error_msg = "Ошибка: пустая ввод"
        logger_masks.error(f"Ошибка: {error_msg}")
        return error_msg

    prep_card_number = re.sub(r"\D", "", str(card_number))

    if len(prep_card_number) != 16:
        error_msg = "Ошибка: количество символов в номере больше или меньше"
        logger_masks.error(f"Ошибка: {error_msg}, длина: {len(prep_card_number)}, входные данные: {card_number}")
        return error_msg

    result = f"{prep_card_number[0:4]} {prep_card_number[4:6]}** **** {prep_card_number[12:16]}"
    logger_masks.info(f"Успешное маскирование номера карты: {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """Hide account number"""

    logger_masks.info(f"Вызов функции get_mask_account с аргументом: {account_number}")

    if has_non_digit_except_spaces(account_number):
        error_msg = "Ошибка: присутствуют буквы"
        logger_masks.error(f"Ошибка: {error_msg}, входные данные: {account_number}")
        return error_msg

    prep_account_number = re.sub(r"\D", "", str(account_number))

    if len(prep_account_number) < 4:
        error_msg = "Ошибка: номер счёта должен содержать минимум 4 цифры"
        logger_masks.error(f"Ошибка: {error_msg}, длина: {len(prep_account_number)}, входные данные: {account_number}")
        return error_msg

    result = f"**{prep_account_number[-4:]}"
    logger_masks.info(f"Успешное маскирование номера счета: {result}")
    return result
