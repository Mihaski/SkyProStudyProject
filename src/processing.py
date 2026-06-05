def filter_by_state(list_dict: list[dict], state='EXECUTED') -> list[dict]:
    """ Функция возвращает список словарей, у которых ключ state соответствует указанному значению."""

    new_list = []

    for item in list_dict:
        if item['state'] == state:
            new_list.append(item)

    return new_list


def sort_by_date(list_dict: list[dict], sort_by_decrease=True) -> list[dict]:
    """ Функция возвращает список, отсортированный по дате"""

    new_list = list_dict.copy()

    new_list.sort(key=lambda x: x.get("date", ""), reverse=sort_by_decrease)

    return new_list
