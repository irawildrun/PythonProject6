import requests
import json

API_KEY = '1vsVLrm1UVMVV9utaqlTHZsFj5WCr0p8'
# в документации указан пример, берем оттуда сайт API. без endpoints не работает, берем курсы валют на текущую дату
URL = 'https://api.apilayer.com/exchangerates_data/latest'

def get_transaction_amount_in_rub(transaction):
    """
    Принимает транзакцию, возвращает ее сумму. Если валюта не руб, то конвертирует.
    """
    # Достаем сумму. Проверяем, есть ли ключ "amount" в ответе запроса, возвращаем 0.0, т.к. требуется вывод float
    if 'amount' not in transaction:
        return 0.0

    amount = transaction['amount']

    # Проверяем, что amount - число
    if not isinstance(amount, (int, float)):
        return 0.0

    # Превращаем в float
    amount = float(amount)

    # Достаем валюту. Если ключа "currency" нет, то считаем, что это рубли
    if 'currency' not in transaction:
        currency = 'RUB'
    else:
        currency = transaction['currency']

    # Если валюта - рубли, то возвращаем сумму как есть
    if currency == 'RUB':
        return amount

    # Если не рубли, то запрашиваем курс через запрос к API
    # делаем через try для обработки ошибок
    # указываем параметр timeout для ограничения времени выполнения запроса
    try:
        response = requests.get(
            URL,
            params={'base': currency, 'symbols': 'RUB'},
            headers={'apikey': API_KEY},
            timeout=10
        )

        # поднимаем исключение, если ошибка
        response.raise_for_status()

        # Превращаем ответ сервера в словарь Python
        data = response.json()
        # достаем ставку
        rate = data['rates']['RUB']
        # Умножаем сумму на курс, округляем до 2 знаков после запятой
        result = round(amount * rate, 2)
        return f'Запрошенная сумма, рассчитанная в рублях: {result}'

    except Exception as e:
        print(f'Ошибка при конвертации: {e}')
        return 0.0



print(get_transaction_amount_in_rub({'amount': 180, 'currency': 'EUR'}))