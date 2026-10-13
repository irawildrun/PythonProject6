import json
import logging
from pathlib import Path

# создаю логгер модуля, задаю уровень
logger = logging.getLogger('utils.py')
logger.setLevel(logging.DEBUG)
# делаю хендлер на запись в файл в режиме перезаписи
file_handler = logging.FileHandler('../logs/utils.log', mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_operations(path):
    """Функция чтения JSON-файла с транзакциями."""
    logger.info('Открываем файл с транзакциями...')
    # т.к. указываем путь, используем библиотеку pathlib
    path = Path(path)

    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        # если внутри json-файла не список транзакций, то выдает пустой список, как с другими ошибками
        if not isinstance(data, list):
            print('Это НЕ список')
            logger.error('Ошибка данных. Ожидался список ранзакций.')
            return []

        logger.info('Транзакции получены.')
        logger.info('Функция read_operations завершила работу.')
        # если операция внутри данных - словарь (нужный формат), то оставляем в итоговом словаре для дальнейшей работы
        return [operation for operation in data if isinstance(operation, dict)]

    # если любая ошибка: декодирования/файл не найден/ошибка значения, то пустой список
    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        print('ОШИБКА: ', e)
        logger.error('Ошибка чтения транзакций: %s', e)
        return []


if __name__ == '__main__':
    operations = read_operations('../data/operations.json')
    print('Результат:', operations)
    print('Количество:', len(operations))
