from datetime import datetime
from pathlib import Path

from src.utils import read_operations
from src.read_transactions import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state, sort_by_date
from src.widget import mask_account_card, get_date
from src.search import process_bank_search


# Папка с файлами
DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

# Папка для сохранения результатов
RESULTS_DIR = Path(__file__).resolve().parent.parent / 'results'


# вывожу отдельно функцию Ответов Да и Нет для сокращения кода основных функций
def get_yes_no(question):
    """Запрашивает ответ Да или Нет"""
    while True:
        answer = input(question).strip().lower()

        # рассматриваем ввод разных форматов ответов
        if answer in ('да', 'ага', 'yes', 'y', 'yeah', 'yep'):
            return True
        elif answer in ('нет', 'неа', 'no', 'n', 'nope'):
            return False
        else:
            print('Введите Да или Нет')


# вывожу отдельно функцию доставания кода валюты, т.к. входные файлы разные по структуре
def get_currency_code(transaction):
    """Получает код валюты из транзакции JSON или CSV/XLSX"""
    if 'operationAmount' in transaction:
        return transaction.get('operationAmount', {}).get('currency', {}).get('code')

    return transaction.get('currency_code')


def filter_transactions_by_currency(transactions, currency_code):
    """Оставляет операции только с указанной валютой"""
    result = []

    for transaction in transactions:
        if get_currency_code(transaction) == currency_code:
            result.append(transaction)

    return result


def format_transaction(transaction):
    """Форматирует банковскую операцию для вывода"""

    # Форматируем дату с помощью функции из модуля widget.py
    date = get_date(transaction.get('date', ''))

    # Получаем описание операции
    description = transaction.get('description', 'Описание отсутствует')

    # Получаем отправителя и получателя
    sender = transaction.get('from')
    recipient = transaction.get('to')

    # Маскируем номера карт и счетов
    # Проверяем, что отправитель и получатель являются строками
    if isinstance(sender, str) and sender:
        sender = mask_account_card(sender)
    else:
        sender = None

    if isinstance(recipient, str) and recipient:
        recipient = mask_account_card(recipient)
    else:
        recipient = None

    # Получаем сумму и валюту
    if 'operationAmount' in transaction:
        operation_amount = transaction.get('operationAmount', {})
        amount = operation_amount.get('amount', '0')
        currency = operation_amount.get('currency', {})
        currency_name = currency.get('name', currency.get('code', ''))
    else:
        amount = transaction.get('amount', '0')
        currency_name = transaction.get('currency_name')

        if not isinstance(currency_name, str):
            currency_name = transaction.get('currency_code', '')

        if not isinstance(currency_name, str):
            currency_name = ''

    # Собираем результат
    result = f'{date} {description}'

    if sender and recipient:
        result += f'\n{sender} -> {recipient}'
    elif recipient:
        result += f'\n{recipient}'
    elif sender:
        result += f'\n{sender}'

    result += f'\nСумма: {amount} {currency_name}'

    return result


# Сохраняем результаты в отдельную папку для информативности по запросам
def save_results(transactions, query_info):
    """Сохраняет результаты обработки в отдельный текстовый файл"""

    # Создаём папку results, если её ещё нет
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Получаем текущую дату и время для названия файла
    current_time = datetime.now()
    file_name = current_time.strftime('report_%Y%m%d_%H%M%S_%f.txt')

    # Формируем полный путь к файлу
    file_path = RESULTS_DIR / file_name

    # Формируем содержимое отчёта
    report = []

    report.append(f'Дата и время запроса: {current_time.strftime("%d.%m.%Y %H:%M:%S")}')
    report.append('')
    report.append('ПАРАМЕТРЫ ЗАПРОСА:')
    report.append('-' * 55)

    # Добавляем информацию о запросе
    for item in query_info:
        report.append(item)

    report.append('')
    report.append('РЕЗУЛЬТАТЫ:')
    report.append('-' * 55)
    report.append(f'Количество найденных операций: {len(transactions)}')
    report.append('')

    # Добавляем найденные операции
    if transactions:
        for transaction in transactions:
            report.append(format_transaction(transaction))
            report.append('')
    else:
        report.append('Не найдено ни одной транзакции, подходящей под условия фильтрации')

    # Записываем отчёт в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(report))

    return file_path



def main():
    """Главная функция приложения"""

    print('Привет! Добро пожаловать в программу работы с банковскими операциями.')

    # Выбор формата файла, как требуется в задании
    print('\nВыберите необходимый пункт меню:')
    print('1. Получить информацию о транзакциях из JSON-файла')
    print('2. Получить информацию о транзакциях из CSV-файла')
    print('3. Получить информацию о транзакциях из XLSX-файла')

    while True:
        file_choice = input('Введите номер: ').strip()

        if file_choice == '1':
            file_path = DATA_DIR / 'operations.json'
            transactions = read_operations(file_path)
            print('Для обработки выбран JSON-файл')
            source_name = 'JSON (operations.json)'
            break

        elif file_choice == '2':
            file_path = DATA_DIR / 'transactions.csv'
            transactions = read_csv_transactions(file_path)
            print('Для обработки выбран CSV-файл')
            source_name = 'CSV (transactions.csv)'
            break

        elif file_choice == '3':
            file_path = DATA_DIR / 'transactions_excel.xlsx'
            transactions = read_excel_transactions(file_path)
            print('Для обработки выбран XLSX-файл')
            source_name = 'XLSX (transactions_excel.xlsx)'
            break

        else:
            print('Введите 1, 2 или 3')

    if not transactions:
        print('Не удалось загрузить операции, или файл пуст')
        return


    # Создаём список для сохранения параметров запроса
    query_info = []

    # Записываем источник данных
    query_info.append(f'Источник данных: {source_name}')


    # Фильтрация по статусу
    print('\nВведите статус, по которому необходимо выполнить фильтрацию: ')
    print('1. EXECUTED — выполнена')
    print('2. CANCELED — отменена')
    print('3. PENDING — ожидает обработки')

    statuses = {
        '1': 'EXECUTED',
        '2': 'CANCELED',
        '3': 'PENDING'
    }

    while True:
        status_choice = input('Введите номер статуса: ').strip()

        if status_choice in statuses:
            status = statuses[status_choice]
            break
        else:
            print('Неверный выбор. Попробуйте ещё раз')


    # Записываем выбранный статус в параметры запроса
    query_info.append(f'Статус операций: {status}')


    # Фильтруем операции по статусу
    transactions = filter_by_state(transactions, status)

    # Сортировка по дате, пользуемся функцией Ответов Да или Нет. Если Да, то дальнейшие условия
    if get_yes_no('\nОтсортировать операции по дате? '):
        reverse = get_yes_no('Сначала показывать новые операции? ')

        transactions = sort_by_date(transactions, reverse=reverse)

        if reverse:
            query_info.append('Сортировка: по убыванию даты (сначала новые)')
        else:
            query_info.append('Сортировка: по возрастанию даты (сначала старые)')

    else:
        query_info.append('Сортировка: не выполнялась')

        # Фильтрация по валюте
    if get_yes_no('Выводить только рублёвые операции? '):
        transactions = filter_transactions_by_currency(transactions, 'RUB')
        query_info.append('Фильтрация по валюте: только RUB')
    else:
        query_info.append('Фильтрация по валюте: не выполнялась')

        # Поиск по описанию
    if get_yes_no('Искать операции по описанию? '):
        search_word = input('Введите слово или фразу для поиска: ').strip()

        if search_word:
            transactions = process_bank_search(transactions, search_word)
            query_info.append(f'Поиск по описанию: "{search_word}"')
        else:
            print('Поисковая строка пустая. Поиск выполнен не будет')
            query_info.append('Поиск по описанию: не выполнялся (пустой запрос)')
    else:
        query_info.append('Поиск по описанию: не выполнялся')

        # Вывод результата
    print('\nРаспечатываю итоговый список транзакций...')

    # Сохраняем результаты обработки в отдельный файл
    result_file = save_results(transactions, query_info)

    if not transactions:
        print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации')
        print(f'Отчёт сохранён: {result_file}')
        return

    print(f'\nВсего банковских операций: {len(transactions)}\n')

    for transaction in transactions:
        print(format_transaction(transaction))
        print()

    # Выводим путь к сохранённому отчёту
    print(f'Отчёт сохранён: {result_file}')



if __name__ == '__main__':
    main()

