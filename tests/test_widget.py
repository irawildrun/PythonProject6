from typing import Any, Dict
import pytest
from src.widget import get_date, mask_account_card, parse_iso_date


@pytest.fixture
def card_and_account_data() -> Dict[str, str]:
    return {
        'card': 'Maestro 1596837868705199',
        'account': 'Счет 64686473678894779589',
    }


# проверка работы функции
@pytest.mark.parametrize(
    'data, expected',
    [
        ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
        ('Visa 9876543210987654', 'Visa 9876 54** **** 7654'),
        ('Mastercard 1111222233334444', 'Mastercard 1111 22** **** 4444'),
        ('Счет 64686473678894779589', 'Счет **9589'),
        ('Счет 1234567890', 'Счет **7890'),
    ],
)
def test_mask_account_card_correct_mask(data: str, expected: str) -> None:
    assert mask_account_card(data) == expected


# проверка на отсутствие цифр для маски
@pytest.mark.parametrize(
    'data_without_numbers',
    [
        '',
        '    ',
        'no digits',
        'Счет',
        'Card',
    ],
)
def test_mask_account_card_no_digits_returns_original(data_without_numbers: str) -> None:
    assert mask_account_card(data_without_numbers) == data_without_numbers


# проверка на игнор "неподходящих" цифр (в середине строки)
@pytest.mark.parametrize(
    'data, expected',
    [
        ('Order 12345 and 9876543210987654', 'Order 12345 and 9876 54** **** 7654'),
        ('Payment #555 for 1111222233334444', 'Payment #555 for 1111 22** **** 4444'),
        ('Transfer 9999 to Счет 72824645351234567890', 'Transfer 9999 to Счет **7890'),
        ('Maestro такая 1596837868705199', 'Maestro такая 1596 83** **** 5199'),
    ],
)
def test_mask_account_card_digits_in_middle_not_masked(data: str, expected: str) -> None:
    assert mask_account_card(data) == expected


# проверка переформата ISO в привычную дату
@pytest.mark.parametrize(
    'iso_string, expected',
    [
        ('2024-03-11T02:26:18.671407', '11.03.2024'),
        ('2019-07-03T18:35:29.512364', '03.07.2019'),
        ('2000-01-01T00:00:00', '01.01.2000'),
        ('2018-06-30T02:08:58.425572', '30.06.2018'),
    ],
)
def test_get_date_iso_to_dd_mm_yyyy(iso_string: str, expected: str) -> None:
    assert get_date(iso_string) == expected


# проверка на "неподходящие" данные для ISO
@pytest.mark.parametrize(
    'bad_iso',
    [
        '',  # пустая строка
        '    ',  # пробелы
        'not a date',  # текст
        '12.03.2024',  # не ISO формат
        'abcdefghi',  # не цифры
    ],
)
def test_get_date_invalid_data(bad_iso: str) -> None:
    with pytest.raises(ValueError):
        get_date(bad_iso)
