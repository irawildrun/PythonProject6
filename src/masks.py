# Реализация функций маскировки номера карты и банковского счета
import logging
from pathlib import Path
from src.decorators import log

# перестал видеть файлы с логами, хотя по директориям не перемещалась. тогда сделаем абсолютный путь, в корне проекта
logs_dir = Path(__file__).resolve().parent.parent / 'logs'
logs_dir.mkdir(exist_ok=True)

# создаю логгер модуля, задаю уровень
logger = logging.getLogger('masks.py')
logger.setLevel(logging.DEBUG)
# делаю хендлер на запись в файл в режиме перезаписи
file_handler = logging.FileHandler(logs_dir / 'masks.log', mode='w', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


@log(filename='../masks_logs.txt')
def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты по формату XXXX XX** **** XXXX."""
    logger.info('Начинаем маскировку номера карты...')

    # После написания теста добавила фильтр на тип входных данных внутрь функции.
    if not isinstance(card_number, str):
        logger.error('Ошибка передачи номера карты: ожидалась строка.')
        raise TypeError('Номер карты должен быть строкой.')

    if not (card_number.isdigit() and len(card_number) == 16):
        logger.error('Ошибка передачи номера карты: ожидалось 16 цифр.')
        raise ValueError('Номер карты должен содержать 16 цифр.')

    logger.info('Маскировка номера карты выполнена успешно.')
    # Поскольку на вход принимаем строку, можем использовать срезы.
    return card_number[:4] + ' ' + card_number[4:6] + '** **** ' + card_number[-4:]


@log(filename='../masks_logs.txt')
def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета по формату **XXXX."""
    logger.info('Начинаем маскировку номера счёта...')

    # После написания теста добавила фильтр на тип входных данных внутрь функции.
    if not isinstance(account_number, str):
        logger.error('Ошибка передачи номера счета: ожидалась строка.')
        raise TypeError('Номер счета должен быть строкой.')

    if not (account_number.isdigit() and len(account_number) >= 4):
        logger.error('Ошибка передачи номера счета: ожидалось минимум 4 цифры.')
        raise ValueError('Номер счета должен содержать минимум 4 цифры.')

    logger.info('Маскировка номера счета выполнена успешно.')
    # Поскольку на вход принимаем строку, можем использовать срезы.
    return '**' + account_number[-4:]


# Ручной ввод для проверки функций.
# Сделаем проверку с ручным вводом, только если запуск функции происходит в этом файле
if __name__ == '__main__':
    card_number = input('Введите номер карты, без пробелов 16 цифр: ').strip()
    account_number = input('Введите номер банковского счета минимум 4 цифры: ').strip()

    try:
        print(get_mask_card_number(card_number))
    except Exception as e:
        print(f"Ошибка: {e}")

    try:
        print(get_mask_account(account_number))
    except Exception as e:
        print(f"Ошибка: {e}")
