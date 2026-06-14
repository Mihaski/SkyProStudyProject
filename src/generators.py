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

