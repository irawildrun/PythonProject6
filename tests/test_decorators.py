import pytest
from src.decorators import log


def summ(a, b):
    """Тестовая функция суммы чисел"""
    return a + b


def error_out(value):
    """Тестовая функция ошибки: всегда выдает ValueError"""
    raise ValueError(f'Error: {value}')


# тесты вывода в консоль
def test_log_success_console(capsys):
    """При успешном выполнении функции в консоль печатается 'ok', функция возвращает результат"""
    # вызываем функцию, применяя декоратор
    logged_test_func = log()(summ)
    result = logged_test_func(1, 2)

    assert result == 3
    captured = capsys.readouterr()
    assert 'summ ok' in captured.out
    assert 'Result: 3' in captured.out


def test_log_error_console(capsys):
    """При ошибке в консоль печатается текст ошибки"""
    # вызываем функцию, применяя декоратор
    logged_test_func = log()(error_out)

    with pytest.raises(ValueError):
        log()(logged_test_func('_error_'))

    captured = capsys.readouterr()
    assert 'error_out error' in captured.out
    assert 'Error: _error_' in captured.out


# тесты записи в лог-файл
def test_log_success_file(tmp_path):
    """При успешном выполнении функции в консоль печатается 'ok'."""
    # создаем временный путь к папке для тестирования работы (фишка из Лайва от Сергея Горохова)
    log_file = tmp_path / 'logs.txt'

    # вызываем функцию, применяя декоратор
    logged_test_func = log(filename=log_file)(summ)

    logged_test_func(3, 4)

    assert log_file.exists()
    log_text = log_file.read_text(encoding='utf-8')
    assert 'summ ok' in log_text


def test_log_error_file(tmp_path):
    """При ошибке запись в файл содержит текст исключения"""
    log_file = tmp_path / 'logs.txt'

    logged_test_func = log(filename=log_file)(error_out)

    with pytest.raises(ValueError):
        logged_test_func('_error_')

    log_text = log_file.read_text(encoding='utf-8')
    assert 'error_out error' in log_text
    assert 'Error: _error_' in log_text


def test_log_multiple_calls_append_to_file(tmp_path):
    """Несколько вызовов дописываются в один файл"""
    log_file = tmp_path / 'logs.txt'

    logged_test_func = log(filename=log_file)(summ)

    logged_test_func(3, 4)
    logged_test_func(1, 7)

    content = log_file.read_text(encoding='utf-8')
    assert content.count('summ ok') == 2


def test_log_preserves_function_name():
    """Декоратор сохраняет __name__ оригинальной функции (через @wraps)"""
    assert summ.__name__ == 'summ'
    assert error_out.__name__ == 'error_out'
