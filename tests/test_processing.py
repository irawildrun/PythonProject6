import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def operations():
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 3, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 4, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]


# поскольку вывод данных по фильтрам громоздкий, будем проверять только по id
# проверка работы функции filter_by_state и проверка на несуществующий статус
@pytest.mark.parametrize('state, expected_ids', [
    ('EXECUTED', [1, 2]),
    ('CANCELED', [3, 4]),
    ('UNKNOWN', []),
])
def test_filter_by_state(operations, state, expected_ids):
    assert [operation['id'] for operation in filter_by_state(operations, state)] == expected_ids


# проверка, что при отсутствии входных данных на статус, выводятся значения по 'EXECUTED'
def test_filter_by_state_default(operations):
    assert [operation['id'] for operation in filter_by_state(operations)] == [1, 2]


# проверка на пустой входной список операций
def test_filter_by_state_empty_list():
    assert filter_by_state([], 'EXECUTED') == []


# проверка, что при отсутствии входных данных на направление времени, выводятся значения по-убыванию
def test_sort_by_date_default(operations):
    assert [operation['id'] for operation in sort_by_date(operations)] == [1, 4, 3, 2]


# проверка направления по reverse
def test_sort_by_date_reverse(operations):
    assert [operation['id'] for operation in sort_by_date(operations, reverse=False)] == [2, 3, 4, 1]


# проверка на пустой входной список операций
def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []

