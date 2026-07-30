from unittest.mock import patch

import pytest

from src.utils import get_transaction_amount


@pytest.fixture
def rub_transaction():
    """Фикстура транзакции в рублях"""
    return {
        "id": 1,
        "operationAmount": {"amount": "1500.50", "currency": {"code": "RUB", "name": "Рубль"}},
        "description": "Покупка продуктов",
    }


@pytest.fixture
def usd_transaction():
    """Фикстура транзакции в долларах"""
    return {
        "id": 2,
        "operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "Доллар США"}},
        "description": "Покупка в США",
    }


@pytest.fixture
def eur_transaction():
    """Фикстура транзакции в евро"""
    return {
        "id": 3,
        "operationAmount": {"amount": "75.50", "currency": {"code": "EUR", "name": "Евро"}},
        "description": "Покупка в Европе",
    }


@pytest.fixture
def unknown_currency_transaction():
    """Фикстура транзакции с неизвестной валютой"""
    return {
        "id": 4,
        "operationAmount": {"amount": "1000.00", "currency": {"code": "GBP", "name": "Фунт стерлингов"}},
        "description": "Покупка в Великобритании",
    }


@patch("src.utils.convert_currency")  # Мокаем функцию конвертации
def test_get_transaction_amount_rub(mock_convert, rub_transaction):
    """Тест рублевых транзакций - convert_currency НЕ должен вызываться"""
    result = get_transaction_amount(rub_transaction)

    assert result == 1500.50
    assert isinstance(result, float)
    # Проверяем, что convert_currency НЕ вызывалась для RUB
    mock_convert.assert_not_called()


@patch("src.utils.convert_currency")
def test_get_transaction_amount_usd(mock_convert, usd_transaction):
    """Тест долларовых транзакций с моком convert_currency"""
    # Настраиваем мок
    mock_convert.return_value = "7500.00"  # 100 USD = 7500 RUB

    result = get_transaction_amount(usd_transaction)

    # Проверяем вызов с правильными параметрами
    mock_convert.assert_called_once_with("100.00", "USD", "RUB")
    assert result == 7500.00
    assert isinstance(result, float)


@patch("src.utils.convert_currency")
def test_get_transaction_amount_eur(mock_convert, eur_transaction):
    """Тест евро транзакций с моком convert_currency"""
    mock_convert.return_value = "7550.00"

    result = get_transaction_amount(eur_transaction)

    mock_convert.assert_called_once_with("75.50", "EUR", "RUB")
    assert result == 7550.00


@patch("src.utils.convert_currency")
def test_get_transaction_amount_unknown_currency(mock_convert, unknown_currency_transaction):
    """Тест с неизвестной валютой - convert_currency НЕ должен вызываться"""
    result = get_transaction_amount(unknown_currency_transaction)

    assert result == -0.1
    # Для неизвестной валюты convert_currency не вызывается
    mock_convert.assert_not_called()


@patch("src.utils.convert_currency")
def test_get_transaction_amount_usd_with_mock_side_effect(mock_convert, usd_transaction):
    """Тест с использованием side_effect для имитации разных курсов"""
    # Используем side_effect для последовательных вызовов
    mock_convert.side_effect = ["7500.00", "8000.00", "7200.00"]

    # Первый вызов
    result1 = get_transaction_amount(usd_transaction)
    assert result1 == 7500.00

    # Второй вызов с другой суммой
    usd_transaction["operationAmount"]["amount"] = "100.00"
    result2 = get_transaction_amount(usd_transaction)
    assert result2 == 8000.00

    # Третий вызов
    result3 = get_transaction_amount(usd_transaction)
    assert result3 == 7200.00

    assert mock_convert.call_count == 3


@patch("src.utils.convert_currency")
def test_get_transaction_amount_convert_returns_string(mock_convert, usd_transaction):
    """Тест, когда convert_currency возвращает строку"""
    mock_convert.return_value = "7500.50"

    result = get_transaction_amount(usd_transaction)
    assert result == 7500.50
    assert isinstance(result, float)


@patch("src.utils.convert_currency")
def test_get_transaction_amount_convert_returns_float(mock_convert, usd_transaction):
    """Тест, когда convert_currency возвращает float"""
    mock_convert.return_value = 7500.50

    result = get_transaction_amount(usd_transaction)
    assert result == 7500.50
    assert isinstance(result, float)


@patch("src.utils.convert_currency")
def test_get_transaction_amount_convert_returns_int(mock_convert, usd_transaction):
    """Тест, когда convert_currency возвращает int"""
    mock_convert.return_value = 7500

    result = get_transaction_amount(usd_transaction)
    assert result == 7500.0
    assert isinstance(result, float)


@patch("src.utils.convert_currency")
def test_get_transaction_amount_api_error(mock_convert, usd_transaction):
    """Тест обработки ошибки API - функция возвращает -0.1 при ошибке."""
    mock_convert.side_effect = Exception("API Error")

    result = get_transaction_amount(usd_transaction)

    # ожидаем -0.1, так реализована функция
    assert result == -0.1

    # проверяем вызов с правильными аргументами
    # внимание: amount передаётся как строка '100.00', а не число 100.0
    mock_convert.assert_called_once_with('100.00', 'USD', 'RUB')


@patch("src.utils.convert_currency")
def test_get_transaction_amount_convert_returns_none(mock_convert, usd_transaction):
    """Тест, когда convert_currency возвращает None - функция возвращает -0.1."""
    mock_convert.return_value = None

    result = get_transaction_amount(usd_transaction)

    # ожидаем -0.1, так как функция перехватывает все исключения
    assert result == -0.1
    mock_convert.assert_called_once_with('100.00', 'USD', 'RUB')


@patch("src.utils.convert_currency")
@pytest.mark.parametrize(
    "currency, amount, mock_rate, expected",
    [
        ("USD", "100.00", "7500.00", 7500.00),
        ("EUR", "100.00", "11000.00", 11000.00),
        ("USD", "50.50", "3787.50", 3787.50),
        ("EUR", "25.25", "2777.50", 2777.50),
    ],
)
def test_get_transaction_amount_parametrized_with_mock(mock_convert, currency, amount, mock_rate, expected):
    """Параметризованный тест с моком для разных валют и сумм"""
    mock_convert.return_value = mock_rate

    transaction = {"operationAmount": {"amount": amount, "currency": {"code": currency}}}

    result = get_transaction_amount(transaction)

    mock_convert.assert_called_once_with(amount, currency, "RUB")
    assert result == expected
    assert isinstance(result, float)


@patch("src.utils.convert_currency")
def test_get_transaction_amount_usd_with_specific_rate(mock_convert, usd_transaction):
    """Тест с конкретным курсом конвертации"""
    # Мокаем функцию так, чтобы она возвращала конкретное значение
    mock_convert.return_value = "7500.00"

    result = get_transaction_amount(usd_transaction)

    mock_convert.assert_called_once()
    call_args = mock_convert.call_args[0]  # Получаем аргументы вызова
    assert call_args[0] == "100.00"  # Сумма
    assert call_args[1] == "USD"  # Из валюты
    assert call_args[2] == "RUB"  # В валюту
    assert result == 7500.00


@patch("src.utils.convert_currency")
@pytest.mark.parametrize(
    "currency, expected_call, expected_result",
    [
        ("RUB", False, 100.00),
        ("USD", True, 7500.00),
        ("EUR", True, 7500.00),
        ("GBP", False, -0.1),
        ("JPY", False, -0.1),
    ],
)
def test_get_transaction_amount_check_currency_code_parametrized(
    mock_convert, currency, expected_call, expected_result
):
    """Параметризованный тест проверки кода валюты"""
    mock_convert.return_value = 7500.00

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": currency}}}

    result = get_transaction_amount(transaction)

    assert result == expected_result

    if expected_call:
        # amount передается как строка, так как берется из словаря
        mock_convert.assert_called_once_with("100.00", currency, "RUB")
    else:
        mock_convert.assert_not_called()


@patch("src.utils.convert_currency")
def test_get_transaction_amount_multiple_calls(mock_convert, usd_transaction, eur_transaction):
    """Тест нескольких вызовов с разными транзакциями"""
    mock_convert.side_effect = ["7500.00", "8300.00"]

    result1 = get_transaction_amount(usd_transaction)
    result2 = get_transaction_amount(eur_transaction)

    assert result1 == 7500.00
    assert result2 == 8300.00
    assert mock_convert.call_count == 2

    # Проверяем аргументы каждого вызова
    calls = mock_convert.call_args_list
    assert calls[0][0] == ("100.00", "USD", "RUB")
    assert calls[1][0] == ("75.50", "EUR", "RUB")


@patch("src.utils.convert_currency")
def test_get_transaction_amount_convert_not_called_for_unknown(mock_convert):
    """Тест, что convert_currency не вызывается для неподдерживаемых валют"""
    currencies = ["GBP", "JPY", "CNY", "CHF", "CAD"]

    for currency in currencies:
        transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": currency}}}

        mock_convert.reset_mock()
        result = get_transaction_amount(transaction)

        assert result == -0.1
        mock_convert.assert_not_called()


@patch("src.utils.convert_currency")
def test_get_transaction_amount_returns_float_for_all_cases(mock_convert, usd_transaction):
    """Тест, что функция всегда возвращает float"""
    # Случай с RUB
    rub_tx = {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB"}}}
    result = get_transaction_amount(rub_tx)
    assert isinstance(result, float)

    # Случай с USD
    mock_convert.return_value = "7500.00"
    result = get_transaction_amount(usd_transaction)
    assert isinstance(result, float)

    # Случай с неизвестной валютой
    unknown_tx = {"operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}}}
    result = get_transaction_amount(unknown_tx)
    assert isinstance(result, float)
    assert result == -0.1


@patch("src.utils.convert_currency")
def test_get_transaction_amount_with_mock_properties(mock_convert, usd_transaction):
    """Тест с использованием свойств мока"""
    mock_convert.return_value = "7500.00"

    result = get_transaction_amount(usd_transaction)

    # Проверяем свойства мока
    assert mock_convert.called
    assert mock_convert.call_count == 1
    assert mock_convert.call_args is not None

    # Проверяем, что мок был вызван с правильными параметрами
    mock_convert.assert_called_with("100.00", "USD", "RUB")

    # Проверяем возвращаемое значение
    assert result == 7500.00


# Если функция импортирует convert_currency из другого модуля
@patch("src.utils.convert_currency")
def test_get_transaction_amount_imported_convert(mock_convert, usd_transaction):
    """Тест с моком импортированной функции"""
    mock_convert.return_value = "7500.00"

    result = get_transaction_amount(usd_transaction)

    assert result == 7500.00
    mock_convert.assert_called_once()
