def has_non_digit_except_spaces(text):
    return any(not (c.isdigit() or c.isspace()) for c in text)


def write_or_print(message, filename):
    """Записывает сообщение в файл или выводит в консоль"""
    if filename != "stdout":
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message)
    else:
        print(message, end='')
