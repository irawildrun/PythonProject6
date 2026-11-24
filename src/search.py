import re
from collections import Counter


def process_bank_search(data, search):
    """Ищет банковские операции по заданной строке в описании"""

    result = []

    # создаем шаблон рег. выражения для поиска среди транзакций, делаем регистронезависимость через re.IGNORECASE
    pattern = re.compile(search, re.IGNORECASE)

    for operation in data:
        # Получаем описание без значения по умолчанию
        description = operation.get('description')

        # Проверяем, что описание является строкой
        if isinstance(description, str) and pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(data, categories):
    """Подсчитывает количество операций по категориям"""

    # Собираем все описания операций в список
    descriptions = [
        # делаем возможность поиска по части строки, а не по точному совпадению.
        # Приводим строки поиска к единому формату через нижний регистр
        # Проверяем, что описание является строкой
        operation.get('description', '').lower()
        for operation in data
        if isinstance(operation.get('description'), str)
    ]

    # Создаем счетчик описаний
    counter = Counter(descriptions)

    result = {}

    for category in categories:
        # Считаем количество описаний, содержащих категорию
        count = sum(value for description, value in counter.items() if category.lower() in description)

        result[category] = count

    return result


