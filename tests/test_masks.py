from typing import Any, List
import pytest
from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def card_number_input() -> List[str]:
    return [
        '1596837868705199',
        '1777222281033999',
        '2000535918816002',
        '1612139840056277',
    ]


# проверка работы функции get_mask_card_number
@pytest.mark.parametrize(
    'card_number_input, expected',
    [
        ('1596837868705199', '1596 83** **** 5199'),
        ('1777222281033999', '1777 22** **** 3999'),
        ('2000535918816002', '2000 53** **** 6002'),
        ('1612139840056277', '1612 13** **** 6277'),
    ],
)
def test_get_mask_card_number(card_number_input: str, expected: str) -> None:
    assert get_mask_card_number(card_number_input) == expected


# проверка на "неподходящие" входные данные
@pytest.mark.parametrize(
    'bad_input',
    [
        '',  # пустая строка
        '    ',  # строка только из пробелов
        '123',  # слишком короткий номер
        '123456789012345',  # меньше 16 цифр
        '12345678901234567',  # больше 16 цифр
        '1234abcd56789012',  # есть буквы
        '12-34-56-78-90-12',  # есть спецсимволы
        ' 1234567890123456 ',  # есть пробелы
    ],
)
def test_get_mask_card_number_invalid_card_input(bad_input: str) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number(bad_input)


# если на ввод не строка (тут была ошибка в тесте: передавали строку, а не не-строку)
def test_get_mask_card_number_non_string_input() -> None:
    with pytest.raises(TypeError):
        get_mask_card_number(1234567890123456)


# если на вход None
def test_get_mask_card_number_none_input() -> None:
    with pytest.raises(TypeError):
        get_mask_card_number(None)


# проверка работы функции get_mask_account
@pytest.mark.parametrize(
    'account_number_input, expected',
    [
        ('6837868705199', '**5199'),
        ('33999', '**3999'),
        ('918816002', '**6002'),
        ('200720071612139840056277', '**6277'),
    ],
)
def test_get_mask_account(account_number_input: str, expected: str) -> None:
    assert get_mask_account(account_number_input) == expected


# проверка на "неподходящие" входные данные
@pytest.mark.parametrize(
    'bad_input',
    [
        '',  # пустая строка
        '    ',  # строка только из пробелов
        '123',  # меньше 4 цифр
        'abc',  # нет цифр
        '1a2b3c',  # буквы среди цифр
    ],
)
def test_get_mask_account_invalid_input(bad_input: str) -> None:
    with pytest.raises(ValueError):
        get_mask_account(bad_input)


def test_get_mask_account_exactly_4_digits() -> None:
    assert get_mask_account("1234") == "**1234"


# если на вход None
def test_get_mask_account_none_input() -> None:
    with pytest.raises(TypeError):
        get_mask_account(None)
