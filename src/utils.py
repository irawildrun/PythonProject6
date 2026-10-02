import json
from pathlib import Path


def read_operations(path):
    """Функция чтения JSON-файла с транзакциями."""
    # т.к. указываем путь, используем библиотеку pathlib
    path = Path(path)

    try:
        with open(path) as f:
            data = json.load(f)

        # если внутри json-файла не список транзакций, то выдает пустой список, как с другими ошибками
        if not isinstance(data, list):
            return []

        # если операция внутри данных - словарь (нужный формат), то оставляем в итоговом словаре для дальнейшей работы
        return [operation for operation in data if isinstance(operation, dict)]

    # если любая ошибка: декодирования/файл не найден/ошибка значения, то пустой список
    except (json.JSONDecodeError, FileNotFoundError, ValueError):
        return []


