transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


def filter_by_currency(transactions, currency_code):
    """
    Функция-генератор по транзакциям, возвращает итератор по транзакциям, где валюта соответствует заданной.
    """
    for transaction in transactions:
        operation_amount = transaction.get('operationAmount', {})
        currency = operation_amount.get('currency', {})
        code = currency.get('code')

        if code == currency_code:
            yield transaction


usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(transactions):
    """
    Функция-генератор, последовательно возвращает описания операций из списка транзакций.
    """
    for transaction in transactions:
        description = transaction.get('description', '')
        yield description


descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))


def card_number_generator(start, end):
    """
    Функция-генератор номеров банковских карт.
    Принимает диапазон целых чисел (от 1 до 9999999999999999) и возвращает
    строки с номерами карт в формате XXXX XXXX XXXX XXXX.
    """
    # Если входные данные не валидны, возвращаем сообщения об ошибке
    if start < 1:
        raise ValueError("начало диапазона номеров карт должно быть >= 1")
    if end < start:
        raise ValueError("окончание диапазона номеров карт должно быть выше его начала")

    for num in range(start, end + 1):
        # Преобразуем число в строку 16 символов с ведущими нулями, используем спецификатор формата f-строки:
        # d - целое число, с шириной строки 16 символов, недостающее заполнить нулями
        full_num = f'{num:016d}'

        # Разбиваем на группы по 4 символа через пробел
        card_number = f'{full_num[0:4]} {full_num[4:8]} {full_num[8:12]} {full_num[12:16]}'
        yield card_number


for card_number in card_number_generator(1, 5):
    print(card_number)
