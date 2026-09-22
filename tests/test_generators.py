import pytest
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# фикстуры для filter_by_currency
@pytest.fixture
def test_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
        },
    ]


# параметризация для filter_by_currency
@pytest.mark.parametrize(
    "currency_code, expected_count",
    [
        ("USD", 2),
        ("RUB", 2),
        ("EUR", 0),
    ],
)
def test_filter_by_currency_counts(test_transactions, currency_code, expected_count):
    """Количество отфильтрованных транзакций соответствует ожиданиям."""
    generator = filter_by_currency(test_transactions, currency_code)
    result = list(generator)
    assert len(result) == expected_count


def test_filter_by_currency_empty_list():
    """При пустом списке генератор выполняется."""
    generator = filter_by_currency([], "USD")
    result = list(generator)
    assert result == []


def test_filter_by_currency_no_match(test_transactions):
    """Генератор завершается, если нет совпадений."""
    generator = filter_by_currency(test_transactions, "xxx")
    with pytest.raises(StopIteration):
        next(generator)


def test_filter_by_currency_returns_dicts(test_transactions):
    """Генератор возвращает словари."""
    generator = filter_by_currency(test_transactions, "USD")
    first = next(generator)
    assert isinstance(first, dict)


# параметризация для transaction_descriptions
@pytest.mark.parametrize(
    "input_data, expected",
    [
        ([{"description": "A"}, {"description": "B"}, {"description": "C"}], ["A", "B", "C"]),
        ([], []),
        ([{"description": "Only one"}], ["Only one"]),
        ([{}, {"description": "with description"}, {"description": ""}], ["", "with description", ""]),
    ],
)
def test_transaction_descriptions_content(input_data, expected):
    """Проверка работы функции."""
    generator = transaction_descriptions(input_data)
    result = list(generator)
    assert result == expected


def test_transaction_descriptions_order(test_transactions):
    """Порядов описаний транзакций при выводе сохранен."""
    expected = [t["description"] for t in test_transactions]
    generator = transaction_descriptions(test_transactions)
    result = list(generator)
    assert result == expected


def test_transaction_descriptions_empty():
    """Генератор не падает при пустом списке."""
    generator = transaction_descriptions([])
    result = list(generator)
    assert result == []


# параметризация для card_number_generator
@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (5, 6, ["0000 0000 0000 0005", "0000 0000 0000 0006"]),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator_range(start, end, expected):
    """Генератор выдаёт правильные номера в заданном диапазоне."""
    generator = card_number_generator(start, end)
    result = list(generator)
    assert result == expected


def test_card_number_generator_format():
    """Каждый номер карты выдает по формату XXXX XXXX XXXX XXXX, 4 части по 4 символа."""
    generator = card_number_generator(100, 102)
    for card in generator:
        parts = card.split()
        assert len(parts) == 4
        for part in parts:
            assert len(part) == 4
            assert part.isdigit()


def test_card_number_generator_invalid_start():
    """Значение start < 1 вызывает ValueError."""
    with pytest.raises(ValueError):
        list(card_number_generator(0, 5))


def test_card_number_generator_end_less_than_start():
    """Значение end < start вызывает ValueError."""
    with pytest.raises(ValueError):
        list(card_number_generator(10, 5))


def test_card_number_generator_exhaustion():
    """Генератор корректно завершается после выдачи всех значений."""
    generator = card_number_generator(1, 3)
    next(generator)
    next(generator)
    next(generator)
    with pytest.raises(StopIteration):
        next(generator)
