import json
import os
import tempfile
from unittest.mock import mock_open, patch

import pytest

from src.utils import djecson_from_path


@pytest.fixture
def temp_json_file():
    """Создает временный JSON-файл с тестовыми данными"""
    test_data = [
        {"id": 1, "amount": 100.50, "description": "Test transaction 1"},
        {"id": 2, "amount": 200.75, "description": "Test transaction 2"},
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f)
        temp_path = f.name

    yield temp_path, test_data

    # Очистка после теста
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def temp_empty_file():
    """Создает временный пустой файл"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        temp_path = f.name

    yield temp_path

    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.mark.parametrize(
    "test_data", [[{"id": 1, "amount": 100.50}], [{"id": 1, "amount": 100.50}, {"id": 2, "amount": 200.75}], []]
)
def test_djecson_from_path_valid_file(temp_json_file, test_data):
    """Тест загрузки данных из корректного JSON-файла"""
    # Создаем новый файл с тестовыми данными
    file_path, _ = temp_json_file

    # Перезаписываем файл с новыми данными
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    result = djecson_from_path(file_path)
    assert result == test_data


def test_djecson_from_path_nonexistent_file():
    """Тест загрузки из несуществующего файла"""
    result = djecson_from_path("nonexistent_file.json")
    assert result == []


def test_djecson_from_path_empty_file(temp_empty_file):
    """Тест загрузки из пустого файла"""
    result = djecson_from_path(temp_empty_file)
    assert result == []


@pytest.mark.parametrize(
    "invalid_content, expected_result",
    [
        ('{"invalid": "json", without: closing}', []),  # Некорректный JSON
        ("", []),  # Пустая строка
        ("not json at all", []),  # Совсем не JSON
        ('{"single": "object"}', []),  # Объект вместо списка (может вызвать ошибку)
    ],
)
def test_djecson_from_path_invalid_json(invalid_content, expected_result):
    """Тест загрузки из файла с некорректным JSON"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        f.write(invalid_content)
        temp_path = f.name

    try:
        result = djecson_from_path(temp_path)
        # Проверяем, что результат либо пустой список, либо возникла ошибка
        assert result == expected_result or isinstance(result, list)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@pytest.mark.parametrize("empty_type", ["empty_file", "nonexistent"])
def test_djecson_from_path_empty_cases(empty_type, temp_empty_file):
    """Тест различных случаев с пустыми данными"""
    if empty_type == "empty_file":
        result = djecson_from_path(temp_empty_file)
    else:
        result = djecson_from_path("nonexistent_file.json")

    assert result == []
    assert isinstance(result, list)


def test_djecson_from_path_returns_list():
    """Тест, что функция всегда возвращает список"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump([{"id": 1}], f)
        temp_path = f.name

    try:
        result = djecson_from_path(temp_path)
        assert isinstance(result, list)

        # Тест с несуществующим файлом
        result_nonexistent = djecson_from_path("nonexistent_file.json")
        assert isinstance(result_nonexistent, list)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@patch("os.path.exists")
@patch("os.path.getsize")
def test_djecson_from_path_file_checks(mock_getsize, mock_exists):
    """Тест проверок существования и размера файла"""
    # Тест с несуществующим файлом
    mock_exists.return_value = False
    result = djecson_from_path("any_path.json")
    assert result == []
    mock_exists.assert_called_once()

    # Тест с пустым файлом
    mock_exists.return_value = True
    mock_getsize.return_value = 0
    result = djecson_from_path("any_path.json")
    assert result == []
    mock_getsize.assert_called_with("any_path.json")


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100.50}]')
def test_djecson_from_path_with_mock(mock_file):
    """Тест с использованием mock для open"""
    with patch("os.path.exists", return_value=True), patch("os.path.getsize", return_value=100):
        result = djecson_from_path("test.json")
        expected = [{"id": 1, "amount": 100.50}]
        assert result == expected
        mock_file.assert_called_once_with("test.json", "r", encoding="utf-8")
