from typing import Generator


def filter_by_currency(list_dict_transactions: list[dict], currency: str) -> Generator[dict]:
    """Выдает lazy транзакции по имени (тут нет конкретики по ходу разбирёмся но :todo)"""
    for transaction in list_dict_transactions:
        if currency == transaction["currency"]["name"]:
            yield transaction


def transaction_descriptions(list_dict_transactions: list[dict]) -> Generator[dict]:
    """Выдает lazy описание транзакций"""
    for transaction in list_dict_transactions:
        yield transaction["description"]


def card_number_generator(start_number, end_number) -> Generator[str]:
    """выдает номера банковских карт в формате XXXX XXXX XXXX XXXX"""
    for number in range(start_number, end_number + 1):
        num_str = f"{number:016d}"
        yield f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
