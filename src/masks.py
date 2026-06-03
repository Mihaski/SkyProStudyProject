def get_mask_card_number(card_number: str) -> str:
    """Hide card number"""
    prep_card_number = card_number
    if len(prep_card_number) != 16:
        total_mask = "Количество символов в номере больше или меньше"
    else:
        total_mask = prep_card_number[0:4] + " " + prep_card_number[4:6] + "** **** " + prep_card_number[12:]

    return total_mask


def get_mask_account(account_number: str) -> str:
    """Hide account number"""
    prep_account_number = account_number
    if len(prep_account_number) >= 4:
        total_mask = "**" + prep_account_number[-4:]
    else:
        total_mask = "Количество символов в номере меньше 4"

    return total_mask
