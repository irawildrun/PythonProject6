import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
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


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по категориям"""

    result = {}

    for category in categories:
        count = 0

        for operation in data:
            description = operation.get('description')

            # делаем возможность поиска по части строки, а не по точному совпадению.
            # Приводим строки поиска к единому формату через нижний регистр
            # Проверяем, что описание является строкой
            if isinstance(description, str):
                # Ищем категорию без учёта регистра
                if category.lower() in description.lower():
                    count += 1

        result[category] = count

    return result
