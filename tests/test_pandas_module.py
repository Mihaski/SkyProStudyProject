from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.pandas_module import get_transactions_from_csv, get_transactions_from_xlsx


# тесты для get_transactions_from_csv

def test_read_csv_success():
    """Тест 1: Успешное чтение CSV-файла."""
    mock_csv_data = """id;state;date;amount
1;EXECUTED;2023-01-01;100.50
2;CANCELED;2023-01-02;200.75
"""
    expected = [
        {'id': '1', 'state': 'EXECUTED', 'date': '2023-01-01', 'amount': '100.50'},
        {'id': '2', 'state': 'CANCELED', 'date': '2023-01-02', 'amount': '200.75'},
    ]

    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = get_transactions_from_csv("fake_path.csv")

    assert result == expected
    assert len(result) == 2


def test_read_csv_file_not_found(caplog):
    """Тест 2: Обработка ошибки FileNotFoundError."""
    with caplog.at_level("ERROR"):
        result = get_transactions_from_csv("non_existent_file.csv")

    assert result == []
    assert "Ошибка файл не найден" in caplog.text


def test_read_csv_empty_file(caplog):
    """Тест 3: Обработка пустого CSV-файла (содержит только заголовки)."""
    mock_csv_data = "id;state;date;amount\n"
    expected = []

    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = get_transactions_from_csv("empty.csv")

    assert result == expected
    # Функция не логирует это специально, но это можно добавить как улучшение


def test_read_csv_malformed_data(caplog):
    """Тест 4: Обработка "битого" CSV-файла (невалидные данные)."""
    # csv.DictReader сам обработает ошибки, но мы можем протестировать общее исключение
    mock_csv_data = "id;state;date;amount\n1;EXECUTED;2023-01-01;100.50\ninvalid,row,here"
    expected = [
        {'id': '1', 'state': 'EXECUTED', 'date': '2023-01-01', 'amount': '100.50'}
    ]

    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = get_transactions_from_csv("malformed.csv")

    # DictReader просто пропустит битую строку
    assert result == expected
    assert len(result) == 1


def test_read_csv_with_different_delimiter(caplog):
    """Тест 5: Проверка, что разделитель ';' работает корректно."""
    mock_csv_data = """id;state;amount\n1;EXECUTED;100\n2;CANCELED;200"""
    expected = [
        {'id': '1', 'state': 'EXECUTED', 'amount': '100'},
        {'id': '2', 'state': 'CANCELED', 'amount': '200'},
    ]

    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = get_transactions_from_csv("semicolon.csv")

    assert result == expected


# тесты для get_transactions_from_xlsx

@pytest.fixture
def sample_excel_file(tmp_path):
    """Создает временный Excel-файл для тестов."""
    data = {
        'id': [1, 2, 3],
        'state': ['EXECUTED', 'CANCELED', 'PENDING'],
        'amount': [100.50, 200.75, 300.00]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "test_data.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')
    return str(file_path)


def test_read_xlsx_success(sample_excel_file):
    """Тест 1: Успешное чтение XLSX-файла."""
    expected = [
        {'id': 1, 'state': 'EXECUTED', 'amount': 100.5},
        {'id': 2, 'state': 'CANCELED', 'amount': 200.75},
        {'id': 3, 'state': 'PENDING', 'amount': 300.0},
    ]

    result = get_transactions_from_xlsx(sample_excel_file)

    assert result == expected
    assert len(result) == 3


def test_read_xlsx_file_not_found(caplog):
    """Тест 2: Обработка FileNotFoundError."""
    with caplog.at_level("ERROR"):
        result = get_transactions_from_xlsx("non_existent_file.xlsx")

    assert result == []
    assert "Ошибка файл не найден" in caplog.text


def test_read_xlsx_empty_file(tmp_path, caplog):
    """Тест 3: Обработка пустого XLSX-файла."""
    empty_df = pd.DataFrame()
    file_path = tmp_path / "empty.xlsx"
    empty_df.to_excel(file_path, index=False, engine='openpyxl')

    with caplog.at_level("WARNING"):
        result = get_transactions_from_xlsx(str(file_path))

    assert result == []
    assert "Файл empty.xlsx пуст или не содержит данных" in caplog.text


def test_read_xlsx_with_nan_values(tmp_path):
    """Тест 4: Проверка обработки пустых ячеек (NaN)."""
    data = {
        'id': [1, 2],
        'state': ['EXECUTED', None],  # Пустая ячейка
        'amount': [100.50, None]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "with_nan.xlsx"
    df.to_excel(file_path, index=False, engine='openpyxl')

    expected = [
        {'id': 1, 'state': 'EXECUTED', 'amount': 100.5},
        {'id': 2, 'state': None, 'amount': None},  # NaN преобразован в None
    ]

    result = get_transactions_from_xlsx(str(file_path))

    # Сравниваем, игнорируя тип None
    assert result == expected


def test_read_xlsx_corrupted_file(caplog):
    """Тест 5: Обработка битого или невалидного Excel-файла."""
    with caplog.at_level("ERROR"):
        # Передаем CSV как XLSX, чтобы вызвать исключение
        with patch("builtins.open", mock_open(read_data="fake excel data")):
            # Нам нужно переопределить pd.read_excel, чтобы он выбросил исключение
            with patch("pandas.read_excel", side_effect=Exception("Corrupted file")):
                result = get_transactions_from_xlsx("corrupted.xlsx")

    assert result == []
    assert "Общая категория исключения" in caplog.text
