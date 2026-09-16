from typing import Any, Dict, List
from widget import parse_iso_date

list_of_bank_operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
]


# Для аннотации типов импортируем Any, Dict, List из модуля typing.
def filter_by_state(list_of_bank_operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """Функция фильтрации банковских операций по статусу, по-умолчанию статус 'EXECUTED' (ВЫПОЛНЕНО)
    Используем list comprehension."""
    return [operation for operation in list_of_bank_operations if operation['state'] == state]


def sort_by_date(list_of_bank_operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Функция сортировки банковских операций по дате,
    по-умолчанию направление - по-убыванию (сначала новые).
    Импортируем функционал превращения строки с датой в ISO-формат из ДЗ по 9.2 из модуля widget.py
    """
    return sorted(list_of_bank_operations, key=lambda x: parse_iso_date(x['date']), reverse=reverse)


# проверка работы функции фильтрации по статусу операции
executed_operations = filter_by_state(list_of_bank_operations, 'EXECUTED')
print(executed_operations)

# проверка работы функции сортировки по по убыванию (по-умолчанию) и возрастанию соответственно
sorted_operations_from_new = sort_by_date(list_of_bank_operations)
sorted_operations_from_old = sort_by_date(list_of_bank_operations, reverse=False)
print(sorted_operations_from_new)
print(sorted_operations_from_old)
