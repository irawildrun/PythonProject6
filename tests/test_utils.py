import json
from unittest.mock import mock_open, patch
from utils import read_operations


def test_read_operations_success_open():
    """Проверяем успешное чтение JSON-файла"""
    operations = [
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
        },
    ]

    json_data = json.dumps(operations)
    # одменяем json-файл с помощью mock_open (импортируем его), в read_data - содержимое внутри файла
    with patch('builtins.open', mock_open(read_data=json_data)):
        result = read_operations('operations.json')

    assert result == operations


def test_read_operations_invalid_json():
    """Проверяем некорректный JSON"""
    with patch('builtins.open', mock_open(read_data='невалидный JSON')):
        result = read_operations('operations.json')

    assert result == []


def test_read_operations_file_not_found():
    """Проверяем отсутствие файла"""
    # side_effect - ошибка, которую должен выдать
    with patch('builtins.open', side_effect=FileNotFoundError):
        result = read_operations('operations.json')

    assert result == []


def test_read_operations_only_dicts():
    """Проверяем непосредственную работу функции, что из списка удаляются элементы,
    которые не являются словарями"""
    operations = [
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        "не словарь",
        123,
        None,
        ["список"],
        {
            "id": 41428829,
            "state": "EXECUTED",
        },
    ]

    json_data = json.dumps(operations)

    expected = [
        {
            "id": 441945886,
            "state": "EXECUTED",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
        },
    ]

    with patch('builtins.open', mock_open(read_data=json_data)):
        result = read_operations('operations.json')

    assert result == expected


def test_read_operations_json_is_not_list():
    """Если JSON содержит не список"""
    json_data = json.dumps(
        {
            "id": 41428829,
            "state": "EXECUTED",
        }
    )

    with patch('builtins.open', mock_open(read_data=json_data)):
        result = read_operations('operations.json')

    assert result == []
