import json
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import API_KEY, BASE_URL, convert_currency

# ==================== ФИКСТУРЫ ====================


@pytest.fixture
def mock_api_key():
    """Фикстура для установки API ключа"""
    with patch("src.external_api.API_KEY", "test_api_key_123"):
        yield


# ==================== ТЕСТЫ ====================


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_success_usd_to_rub(mock_get, mock_api_key):
    """Тест успешной конвертации USD в RUB"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "result": 7500.50,  # ✅
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD", "RUB")

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to=RUB&from=USD&amount=100.0"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == 7500.50
    assert isinstance(result, float)


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_success_eur_to_usd(mock_get, mock_api_key):
    """Тест успешной конвертации EUR в USD"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 108.50}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "EUR", "USD")

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to=USD&from=EUR&amount=100.0"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == 108.50
    assert isinstance(result, float)


@patch("src.external_api.API_KEY", None)
@patch("src.external_api.requests.get")
def test_convert_currency_no_api_key(mock_get):
    """Тест при отсутствии API ключа"""
    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_not_called()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_api_error_response(mock_get, mock_api_key):
    """Тест при ошибке в ответе API (success=False)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_called_once()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_http_error(mock_get, mock_api_key):
    """Тест при HTTP ошибке (404, 500 и т.д.)"""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_called_once()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_connection_error(mock_get, mock_api_key):
    """Тест при ошибке соединения"""
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")

    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_called_once()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_timeout_error(mock_get, mock_api_key):
    """Тест при таймауте"""
    mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_called_once()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_json_decode_error(mock_get, mock_api_key):
    """Тест при ошибке парсинга JSON"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_called_once()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_key_error(mock_get, mock_api_key):
    """Тест при отсутствии ключа 'result' в ответе"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True
        # Нет ключа 'result'
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_called_once()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_value_error(mock_get, mock_api_key):
    """Тест при ошибке преобразования в float"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": "not_a_number"}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD", "RUB")

    mock_get.assert_called_once()
    assert result == -0.1


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_default_to_currency(mock_get, mock_api_key):
    """Тест с to_currency по умолчанию (RUB)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 7500.50}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD")  # to_currency не указан

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to=RUB&from=USD&amount=100.0"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == 7500.50


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_zero_amount(mock_get, mock_api_key):
    """Тест с нулевой суммой"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 0.0}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(0.00, "USD", "RUB")

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to=RUB&from=USD&amount=0.0"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == 0.0


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_negative_amount(mock_get, mock_api_key):
    """Тест с отрицательной суммой"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": -7500.50}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(-100.00, "USD", "RUB")

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to=RUB&from=USD&amount=-100.0"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == -7500.50


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_large_amount(mock_get, mock_api_key):
    """Тест с большим числом"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 7500000.00}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100000.00, "USD", "RUB")

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to=RUB&from=USD&amount=100000.0"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == 7500000.00


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_float_amount(mock_get, mock_api_key):
    """Тест с дробной суммой"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 7550.75}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.50, "EUR", "RUB")

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to=RUB&from=EUR&amount=100.5"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == 7550.75


# ==================== ИНТЕГРАЦИОННЫЙ ТЕСТ ====================


@pytest.mark.integration
def test_convert_currency_integration():
    """Интеграционный тест с реальным API (требует API ключ)"""
    if not API_KEY or API_KEY == "":
        pytest.skip("API_KEY не настроен или пустой")

    result = convert_currency(100.00, "USD", "RUB")

    assert isinstance(result, float)
    if result == -0.1:
        pytest.skip("API вернул ошибку (возможно, невалидный ключ)")
    assert result > 0
    assert 6000 < result < 12000


# ==================== ТЕСТЫ НА КОРРЕКТНОСТЬ URL ====================


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_url_formatting(mock_get, mock_api_key):
    """Тест правильности форматирования URL"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 100}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    test_cases = [
        (100.00, "USD", "RUB", f"{BASE_URL}/exchangerates_data/convert?to=RUB&from=USD&amount=100.0"),
        (50.50, "EUR", "USD", f"{BASE_URL}/exchangerates_data/convert?to=USD&from=EUR&amount=50.5"),
        (75.25, "GBP", "EUR", f"{BASE_URL}/exchangerates_data/convert?to=EUR&from=GBP&amount=75.25"),
    ]

    for amount, from_currency, to_currency, expected_url in test_cases:
        convert_currency(amount, from_currency, to_currency)
        mock_get.assert_called_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)


# ==================== ТЕСТЫ НА ВОЗВРАЩАЕМЫЕ ТИПЫ ====================


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_always_returns_float(mock_get, mock_api_key):
    """Тест, что функция всегда возвращает float"""
    # Успешный случай
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 7500.00}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(100.00, "USD", "RUB")
    assert isinstance(result, float)

    # Ошибка API
    mock_response.json.return_value = {"success": False, "error": {"info": "Error"}}
    result = convert_currency(100.00, "USD", "RUB")
    assert isinstance(result, float)
    assert result == -0.1

    # Ошибка запроса
    mock_get.side_effect = requests.exceptions.RequestException("Error")
    result = convert_currency(100.00, "USD", "RUB")
    assert isinstance(result, float)
    assert result == -0.1


# ==================== ТЕСТЫ НА ГРАНИЧНЫЕ ЗНАЧЕНИЯ ====================


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
def test_convert_currency_edge_cases(mock_get, mock_api_key):
    """Тест граничных значений"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 1.0}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # Очень маленькое число
    result = convert_currency(0.0001, "USD", "RUB")
    assert isinstance(result, float)

    # Очень большое число
    result = convert_currency(1e10, "USD", "RUB")
    assert isinstance(result, float)


# ==================== ТЕСТЫ С ИСПОЛЬЗОВАНИЕМ PATCH.OBJECT ====================


def test_convert_currency_with_patch_object():
    """Тест с использованием patch для мока requests.get"""
    with patch("src.external_api.API_KEY", "test_key"):
        with patch("src.external_api.requests.get") as mock_get:  # ✅ Вместо patch.object
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"success": True, "result": 7500.50}
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            result = convert_currency(100.00, "USD", "RUB")

            assert result == 7500.50
            mock_get.assert_called_once()


# ==================== ТЕСТЫ НА ОБРАБОТКУ РАЗНЫХ ВАЛЮТ ====================


@patch("src.external_api.API_KEY", "test_api_key_123")
@patch("src.external_api.requests.get")
@pytest.mark.parametrize(
    "from_currency, to_currency, amount, expected_result",
    [
        ("USD", "RUB", 100.00, 7500.00),
        ("EUR", "RUB", 100.00, 11000.00),
        ("GBP", "RUB", 100.00, 12000.00),
        ("USD", "EUR", 100.00, 92.00),
        ("RUB", "USD", 10000.00, 133.33),
    ],
)
def test_convert_currency_different_currencies(
    mock_get, mock_api_key, from_currency, to_currency, amount, expected_result
):
    """Параметризованный тест с разными валютами"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": expected_result}  # ✅
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = convert_currency(amount, from_currency, to_currency)

    expected_url = f"{BASE_URL}/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
    mock_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key_123"}, timeout=10)
    assert result == expected_result


# ==================== ТЕСТ НА РЕАЛЬНЫЙ API ====================


def test_convert_currency_real_api():
    """Тест с реальным API ключом (только если ключ настроен)"""
    if not API_KEY or API_KEY == "":
        pytest.skip("API_KEY не настроен")

    result = convert_currency(100.00, "USD", "RUB")

    if result == -0.1:
        pytest.skip("API вернул ошибку (возможно, невалидный ключ или лимиты)")

    assert isinstance(result, float)
    assert result > 0
