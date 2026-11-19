import pytest

from src.search import process_bank_search, process_bank_operations


@pytest.fixture
def operations():
    """Тестовый список банковских операций"""
    return [
        {
            'id': 1,
            'description': 'Оплата мобильной связи',
        },
        {
            'id': 2,
            'description': 'Перевод организации',
        },
        {
            'id': 3,
            'description': 'Оплата услуг ЖКХ',
        },
        {
            'id': 4,
            'description': 'Перевод между счетами',
        },
        {
            'id': 5,
            'description': None,
        },
        {
            'id': 6,
        },
    ]


# Тесты для process_bank_search()

def test_process_bank_search_finds_matches(operations):
    """Проверяем поиск операций по заданному слову"""
    result = process_bank_search(operations, 'оплата')

    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[1]['id'] == 3


def test_process_bank_search_ignores_case(operations):
    """Проверяем, что поиск не зависит от регистра"""
    result = process_bank_search(operations, 'ОПЛАТА')

    assert len(result) == 2


def test_process_bank_search_finds_partial_match(operations):
    """Проверяем поиск по части слова"""
    result = process_bank_search(operations, 'орган')

    assert len(result) == 1
    assert result[0]['id'] == 2


def test_process_bank_search_returns_empty_list(operations):
    """Проверяем результат, если совпадений нет"""
    result = process_bank_search(operations, 'покупка')

    assert result == []


def test_process_bank_search_ignores_missing_description(operations):
    """Проверяем обработку операций без описания или с None"""
    result = process_bank_search(operations, 'перевод')

    assert len(result) == 2


def test_process_bank_search_empty_string(operations):
    """Проверяем поиск по пустой строке"""
    result = process_bank_search(operations, '')

    assert len(result) == 4


# Тесты для process_bank_operations()

def test_process_bank_operations_counts_categories(operations):
    """Проверяем подсчёт операций по категориям"""
    categories = ['Оплата', 'Перевод']

    result = process_bank_operations(operations, categories)

    assert result == {
        'Оплата': 2,
        'Перевод': 2,
    }


def test_process_bank_operations_ignores_case(operations):
    """Проверяем, что подсчёт не зависит от регистра"""
    categories = ['оплата', 'ПЕРЕВОД']

    result = process_bank_operations(operations, categories)

    assert result == {
        'оплата': 2,
        'ПЕРЕВОД': 2,
    }


def test_process_bank_operations_partial_match(operations):
    """Проверяем поиск категории по части слова"""
    categories = ['мобиль']

    result = process_bank_operations(operations, categories)

    assert result == {'мобиль': 1}


def test_process_bank_operations_category_not_found(operations):
    """Проверяем категорию, для которой нет операций"""
    categories = ['Покупки']

    result = process_bank_operations(operations, categories)

    assert result == {'Покупки': 0}


def test_process_bank_operations_empty_categories(operations):
    """Проверяем передачу пустого списка категорий"""
    result = process_bank_operations(operations, [])

    assert result == {}

