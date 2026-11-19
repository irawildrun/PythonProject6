from unittest.mock import patch
import pytest
from src import main

# Тесты функции get_yes_no()


def test_get_yes_no_valid_answers():
    """Проверяет допустимые ответы Да и Нет"""

    answers = ['да', 'ага', 'yes', 'y', 'yeah', 'yep', 'нет', 'неа', 'no', 'n', 'nope']

    expected_results = [True, True, True, True, True, True, False, False, False, False, False]

    # используем функцию zip для объединения ответов, т.е. для присваивания ожидаемых ответов реальным
    for answer, expected in zip(answers, expected_results):
        with patch('builtins.input', return_value=answer):
            result = main.get_yes_no('Продолжить? ')

        assert result is expected


def test_get_yes_no_invalid_answer(capsys):
    """Проверяет повторный запрос при неправильном ответе"""

    # проверим сначала неподходящий ответ, а затем подходящий
    with patch('builtins.input', side_effect=['не знаю', 'да']):
        result = main.get_yes_no('Продолжить? ')

    captured = capsys.readouterr()

    assert result is True
    assert 'Введите Да или Нет' in captured.out


# Тесты функции get_currency_code()


def test_get_currency_code_json():
    """Проверяет получение кода валюты из JSON"""

    transaction = {'operationAmount': {'currency': {'code': 'RUB'}}}

    result = main.get_currency_code(transaction)

    assert result == 'RUB'


def test_get_currency_code_csv():
    """Проверяет получение кода валюты из CSV или XLSX"""

    transaction = {'currency_code': 'USD'}

    result = main.get_currency_code(transaction)

    assert result == 'USD'


def test_get_currency_code_missing():
    """Проверяет операцию без информации о валюте"""

    transaction = {}

    result = main.get_currency_code(transaction)

    assert result is None


# Тесты функции filter_transactions_by_currency()


def test_filter_transactions_by_currency():
    """Проверяет фильтрацию операций по валюте"""

    transactions = [
        {'id': 1, 'currency_code': 'RUB'},
        {'id': 2, 'currency_code': 'USD'},
        {'id': 3, 'currency_code': 'RUB'},
        {'id': 4, 'currency_code': 'EUR'},
    ]

    result = main.filter_transactions_by_currency(transactions, 'RUB')

    assert len(result) == 2
    assert result == [{'id': 1, 'currency_code': 'RUB'}, {'id': 3, 'currency_code': 'RUB'}]


def test_filter_transactions_by_currency_empty():
    """Проверяет результат, если подходящих операций нет"""

    transactions = [{'id': 1, 'currency_code': 'USD'}, {'id': 2, 'currency_code': 'EUR'}]

    result = main.filter_transactions_by_currency(transactions, 'RUB')

    assert result == []


# Тесты функции format_transaction()


def test_format_transaction_json():
    """Проверяет форматирование операции из JSON"""

    transaction = {
        'date': '2024-01-15T10:30:00',
        'description': 'Перевод организации',
        'from': 'Visa Classic 1234567890123456',
        'to': 'Счет 12345678901234567890',
        'operationAmount': {'amount': '1500.00', 'currency': {'name': 'руб.', 'code': 'RUB'}},
    }

    with (
        patch('src.main.get_date', return_value='15.01.2024'),
        patch('src.main.mask_account_card', side_effect=['Visa Classic 1234 56** **** 3456', 'Счет **7890']),
    ):
        result = main.format_transaction(transaction)

    assert '15.01.2024' in result
    assert 'Перевод организации' in result
    assert 'Visa Classic 1234 56** **** 3456' in result
    assert 'Счет **7890' in result
    assert 'Сумма: 1500.00 руб.' in result
    assert '->' in result


def test_format_transaction_csv():
    """Проверяет форматирование операции из CSV или XLSX"""

    transaction = {
        'date': '2024-01-15T10:30:00',
        'description': 'Оплата услуг',
        'from': None,
        'to': 'Счет 12345678901234567890',
        'amount': '2500.00',
        'currency_name': 'руб.',
    }

    with (
        patch('src.main.get_date', return_value='15.01.2024'),
        patch('src.main.mask_account_card', return_value='Счет **7890'),
    ):
        result = main.format_transaction(transaction)

    assert '15.01.2024' in result
    assert 'Оплата услуг' in result
    assert 'Счет **7890' in result
    assert 'Сумма: 2500.00 руб.' in result
    assert '->' not in result


def test_format_transaction_without_sender_and_recipient():
    """Проверяет форматирование операции без отправителя и получателя"""

    transaction = {
        'date': '2024-01-15T10:30:00',
        'description': 'Пополнение счета',
        'amount': '500',
        'currency_name': 'руб.',
    }

    with patch('src.main.get_date', return_value='15.01.2024'):
        result = main.format_transaction(transaction)

    assert 'Пополнение счета' in result
    assert 'Сумма: 500 руб.' in result
    assert '->' not in result


# Тесты функции save_results()


def test_save_results_creates_report(tmp_path):
    """Проверяет создание и заполнение отчёта"""

    transactions = [{'id': 1}]

    query_info = [
        'Источник данных: JSON (operations.json)',
        'Статус операций: EXECUTED',
        'Фильтрация по валюте: только RUB',
    ]

    # Подменяем функцию форматирования операции
    with (
        patch('src.main.RESULTS_DIR', tmp_path),
        patch('src.main.format_transaction', return_value='15.01.2024 Оплата услуг'),
    ):
        result = main.save_results(transactions, query_info)

    # Проверяем, что файл создан
    assert result.exists()

    # Читаем содержимое файла
    report = result.read_text(encoding='utf-8')

    assert 'ПАРАМЕТРЫ ЗАПРОСА:' in report
    assert 'Источник данных: JSON (operations.json)' in report
    assert 'Статус операций: EXECUTED' in report
    assert 'Количество найденных операций: 1' in report
    assert '15.01.2024 Оплата услуг' in report


def test_save_results_without_transactions(tmp_path):
    """Проверяет сохранение отчёта без найденных операций"""

    transactions = []
    query_info = ['Статус операций: EXECUTED']

    with patch('src.main.RESULTS_DIR', tmp_path):
        result = main.save_results(transactions, query_info)

    report = result.read_text(encoding='utf-8')

    assert result.exists()
    assert 'Количество найденных операций: 0' in report
    assert 'Не найдено ни одной транзакции, подходящей под условия фильтрации' in report


# Тесты главной функции main()


def test_main_json_success(capsys, tmp_path):
    """Проверяет успешную работу основной функции с JSON"""

    transactions = [
        {
            'id': 1,
            'state': 'EXECUTED',
            'date': '2024-01-15T10:30:00',
            'description': 'Оплата услуг',
            'operationAmount': {'amount': '1500', 'currency': {'name': 'руб.', 'code': 'RUB'}},
        }
    ]

    # Подменяем ввод пользователя: JSON;статус EXECUTED; без сортировки; без фильтрации по валюте; без поиска
    user_answers = ['1', '1', 'нет', 'нет', 'нет']

    with (
        patch('builtins.input', side_effect=user_answers),
        patch('src.main.read_operations', return_value=transactions),
        patch('src.main.filter_by_state', return_value=transactions),
        patch('src.main.save_results', return_value=tmp_path / 'report.txt'),
        patch('src.main.format_transaction', return_value='Оплата услуг'),
    ):
        main.main()

    captured = capsys.readouterr()

    assert 'Для обработки выбран JSON-файл' in captured.out
    assert 'Всего банковских операций: 1' in captured.out
    assert 'Оплата услуг' in captured.out
    assert 'Отчёт сохранён:' in captured.out


def test_main_empty_file(capsys):
    """Проверяет завершение программы, если файл пуст"""

    with (
        patch('builtins.input', return_value='1'),
        patch('src.main.read_operations', return_value=[]),
        patch('src.main.save_results') as mock_save_results,
    ):
        main.main()

    captured = capsys.readouterr()

    assert 'Не удалось загрузить операции, или файл пуст' in captured.out

    # Если файл пуст, сохранение отчёта не запускается
    mock_save_results.assert_not_called()
