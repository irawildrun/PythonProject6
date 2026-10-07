from unittest.mock import Mock, patch
from src.external_api import get_transaction_amount_in_rub


def test_get_transaction_amount_in_rub_api_error():
    """Проверяем ошибку при запросе к API"""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": "EUR"
            }
        }
    }

    with patch('external_api.requests.get', side_effect=Exception('Ошибка')):
        result = get_transaction_amount_in_rub(transaction)

    assert result == 0.0


def test_get_transaction_amount_in_rub__eur_convert():
    """Проверяем конвертацию евро в рубли"""
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": "EUR"
            }
        }
    }
    # создаем поддельный ответ от API
    response = Mock()
    # говорим, что получить ответ нужно RUB
    response.json.return_value = {
        "rates": {
            "RUB": 100
        }
    }

    with patch('external_api.requests.get', return_value=response):
        result = get_transaction_amount_in_rub(transaction)
    # проверяем выполнение функции - пересчет в руб по формуле
    assert result == 10000.0


def test_get_transaction_amount_in_rub__missing_operation_amount():
    """Проверяем отсутствие operationAmount"""
    transaction = {}
    result = get_transaction_amount_in_rub(transaction)
    assert result == 0.0


def test_get_transaction_amount_in_rub_invalid_amount():
    """Проверяем некорректную сумму"""
    transaction = {
        "operationAmount": {
            "amount": "не число",
            "currency": {
                "code": "RUB"
            }
        }
    }

    result = get_transaction_amount_in_rub(transaction)
    assert result == 0.0


def test_get_transaction_amount_in_rub_http_error():
    """Проверяем ошибку HTTP от API"""
    # здесь отдельно проверяем response.raise_for_status()
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": "EUR"
            }
        }
    }
    response = Mock()
    # side_effect - в данном случае как метод
    response.raise_for_status.side_effect = Exception('Ошибка')

    with patch('external_api.requests.get', return_value=response):
        result = get_transaction_amount_in_rub(transaction)
    assert result == 0.0
