from datetime import time
from functools import wraps


def log(filename=None):
    """
    Декоратор с параметром filename - файла для записи логов выполнения функций.
    Если filename указан, пишет в этот файл.
    Если не указан, печатает в консоль.
    Логирует время, результат или ошибку.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Замеряем время начала выполнения функции
            start_time = time.time()

            try:
                # Пытаемся выполнить функцию
                result = func(*args, **kwargs)
                # Замеряем время окончания выполнения функции
                end_time = time.time()

                # Формируем сообщение о выполнении функции, если результат БЕЗ ошибки
                message = (
                    f'{func.__name__} ok\n'
                    f'Args: {args}, Kwargs: {kwargs}\n'
                    f'Time taken: {end_time - start_time:.06f} seconds\n'
                    f'Result: {result}\n'
                )
            except Exception as exc:
                end_time = time.time()
                # Формируем сообщение об ошибке
                message = (
                    f'{func.__name__} error: {exc}\n'
                    f'Args: {args}, Kwargs: {kwargs}\n'
                    f'Time taken: {end_time - start_time:.06f} seconds\n'
                )
                # возбуждаем ошибку, если в результате выполнения функции есть ошибка
                raise

            # запись/вывод лога в файл или консоль
            if filename:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(message)
            else:
                print(message)
            return result
        return wrapper
    return decorator

