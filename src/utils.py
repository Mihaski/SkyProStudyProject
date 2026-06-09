def has_non_digit_except_spaces(text):
    return any(not (c.isdigit() or c.isspace()) for c in text)
