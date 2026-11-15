import re


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Ищет банковские операции по заданной строке в описании"""

    result = []

    # создаем шаблон регулярного выражения для поиска среди транзакций, делаем регистронезависимость через re.IGNORECASE
    pattern = re.compile(search, re.IGNORECASE)

    for operation in data:
        description = operation.get('description', '')

        if isinstance(description, str) and pattern.search(description):
            result.append(operation)

    return result

