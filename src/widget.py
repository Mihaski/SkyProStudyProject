from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Hide account or card number with symbols at starts"""

    prep_mask = account_info.split()
    if prep_mask[0] == "Счет":
        prep_mask[-1] = get_mask_account(prep_mask[-1])
    else:
        prep_mask[-1] = get_mask_card_number(prep_mask[-1])
    return " ".join(prep_mask)


def get_date(unformatted_date: str) -> str:
    """Get date from unformatted date"""

    year = unformatted_date[0:4]
    month = unformatted_date[5:7]
    day = unformatted_date[8:10]

    return f'{year}.{month}.{day}'
