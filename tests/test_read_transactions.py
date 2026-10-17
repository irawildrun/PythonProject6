import pandas as pd
from unittest.mock import Mock, patch
from src.read_transactions import read_csv_transactions, read_excel_transactions


def test_read_csv_transactions():
    """Проверяет чтение финансовых операций из CSV-файла"""

    # в качестве mock возьмем усеченные транзакции из файла
    mock_data = pd.DataFrame([
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0
        },
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740.0
        }
    ])

    mock_read_csv = Mock(return_value=mock_data)

    with patch('src.read_transactions.pd.read_csv', mock_read_csv):
        result = read_csv_transactions('fake.csv')

    expected = [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0
        },
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740.0
        }
    ]

    assert result == expected



def test_read_csv_file_not_found():
    with patch('src.read_transactions.pd.read_csv', side_effect=FileNotFoundError):
        result = read_csv_transactions('no.csv')

    assert result == []


# тесты для excel-файла
def test_read_excel_operations():
    """Проверяет чтение финансовых операций из Excel-файла"""

    mock_data = pd.DataFrame([
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0
        },
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740.0
        }
    ])

    mock_read_excel = Mock(return_value=mock_data)

    with patch('src.read_transactions.pd.read_excel', mock_read_excel):
        result = read_excel_transactions('fake.xlsx')

    expected = [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0
        },
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740.0
        }
    ]

    assert result == expected



def test_read_excel_file_not_found():
    with patch('src.read_transactions.pd.read_excel', side_effect=FileNotFoundError):
        result = read_excel_transactions('no.xlsx')

    assert result == []
