def filter_by_state(list_dict: list[dict], state='EXECUTED') -> list[dict]:
    """ Функция возвращает список словарей, у которых ключ state соответствует указанному значению."""

    new_list = []

    for item in list_dict:
        if item['state'] == state:
            new_list.append(item)

    return new_list
