import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError('API_KEY не найден. Проверь файл .env')

# в документации указан пример, берем оттуда сайт API. без endpoints не работает, берем курсы валют на текущую дату
URL = 'https://api.apilayer.com/exchangerates_data/latest'

def get_transaction_amount_in_rub(transaction):
    """
    Принимает транзакцию, возвращает ее сумму. Если валюта не руб, то конвертирует через API.
    """
    # Достаем сумму, переводим во float. Если ошибка, то возвращаем 0.0
    try:
        operation_amount = transaction["operationAmount"]
        amount = float(operation_amount["amount"])
        currency = operation_amount["currency"]["code"]

    except (KeyError, TypeError, ValueError):
        return 0.0

    # Если уже рубли
    if currency == "RUB":
        return amount

    # Если не рубли, то запрашиваем курс через запрос к API
    # делаем через try для обработки ошибок
    # указываем параметр timeout для ограничения времени выполнения запроса
    try:
        response = requests.get(
            URL,
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
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
        return result


    except Exception as e:
        print(f'Ошибка при конвертации: {e}')
        return 0.0



if __name__ == '__main__':
    # передаем в функцию одну транзакцию, как по заданию. но если передавать весь файл json,
    # нужно сначала адаптировать код функции - проходиться циклом по списку
    print(get_transaction_amount_in_rub(
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {
                    "amount": "123",
                    "currency": {
                        "name": "eur.",
                        "code": "EUR"
                    }
                },
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589"
            }
    ))

