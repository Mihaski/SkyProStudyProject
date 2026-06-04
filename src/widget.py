import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Hide account or card number with symbols at starts"""

    if not account_info or account_info.strip() == "":
        return "Ошибка: пустой ввод"

    if '\n' in account_info:
        return "Ошибка: некорректный ввод (содержит перенос строки)"

    parts = account_info.split()

    if len(parts) > 3:
        return "Ошибка: некорректный ввод (слишком много подстрок)"

    if parts[0].lower() == "счет":
        parts[-1] = get_mask_account(parts[-1])
        if "Ошибка" in parts[-1]:
            return parts[-1]

        return " ".join(parts)
    else:
        parts[-1] = get_mask_card_number(parts[-1])
        if "Ошибка" in parts[-1]:
            return parts[-1]

        return " ".join(parts)


def get_date(unformatted_date: str) -> str:
    """Get date from unformatted date"""

    year = unformatted_date[0:4]
    month = unformatted_date[5:7]
    day = unformatted_date[8:10]
    total_date = datetime.date(int(year), int(month), int(day))

    return total_date.strftime("%d.%m.%Y")
