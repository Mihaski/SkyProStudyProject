import re


def filter_by_state(list_dict: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция возвращает список словарей, у которых ключ state соответствует указанному значению."""

    new_list = []

    for item in list_dict:
        if item["state"] == state:
            new_list.append(item)

    return new_list


def sort_by_date(list_dict: list[dict], sort_by_decrease: bool = True) -> list[dict]:
    """Функция возвращает список, отсортированный по дате"""

    new_list = list_dict.copy()

    new_list.sort(key=lambda x: x.get("date", ""), reverse=sort_by_decrease)

    return new_list


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """ возвращает список словарей с банковскими операциями найденных по строке search"""
    result = []

    # Если список пустой или запрос пустой - возвращаем пустой список
    if not data or not search:
        return result

    for item in data:
        # Получаем описание транзакции (если ключа нет, то пустая строка)
        description = item.get("description", "")

        # Если описание пустое - пропускаем
        if not description:
            continue

        # Ищем в описании
        if re.search(search, description):
            result.append(item)

    return result
