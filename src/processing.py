from typing import Any, Dict, List

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



# проверка работы функции фильтрации по статусу операции
executed_operations = filter_by_state(list_of_bank_operations, 'EXECUTED')
print(executed_operations)

