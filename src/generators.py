from typing import Generator


def filter_by_currency(list_dict_transactions: list[dict], currency: str) -> Generator[dict]:
    """Выдает lazy транзакции по имени (тут нет конкретики по ходу разбирёмся но :todo)"""
    for transaction in list_dict_transactions:
        try:
            currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name")
            if currency_name == currency:
                yield transaction
        except (KeyError, TypeError, AttributeError):
            continue


def transaction_descriptions(list_dict_transactions: list[dict]) -> Generator[dict]:
    """Выдает lazy описание транзакций"""
    for transaction in list_dict_transactions:
        yield transaction["description"]


def card_number_generator(start, stop) -> Generator[str]:
    """выдает номера банковских карт в формате XXXX XXXX XXXX XXXX"""
    for number in range(start, stop + 1):
        num_str = f"{number:016d}"
        yield f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
