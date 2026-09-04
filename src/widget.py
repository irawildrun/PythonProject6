import re
from datetime import datetime
from masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """Маскировка номера карты или счета"""
    # Проверяем на наличие цифр в конце строки, если они есть, выполнится функция маскировки
    # Иначе вернет данные обратно
    match = re.search(r"\d+$", data)

    if not match:
        return data

    # достаем номер для маскировки
    number = match.group()

    if data.startswith("Счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    # в выводе отдаются все данные из ввода до начала цифр, а далее - маска
    return data[: match.start()] + masked_number


# def get_date(date: str) -> str:
#     """Форматирование даты из ГГГГ-ММ-ДД в ДД.ММ.ГГГГ"""
#
#     # проверяем строку на соответствие шаблону регулярного выражения
#     match = re.search(r'(\d{4})-(\d{2})-(\d{2})', date)
#
#     # что не соответствует шаблону - удаляем
#     if not match:
#         return ''
#
#     # форматируем дату, используя ранее зафиксированные группы рег. выражений
#     return f'{match.group(3)}.{match.group(2)}.{match.group(1)}'


# решение переформата даты с помощью datetime
def parse_iso_date(date_str: str) -> datetime:
    """Преобразует ISO-строку в datetime (для сортировки и расчётов)."""

    # т.к. в задании явно указано, используем встроенный метод .fromisoformat(),
    # для этого импортируем datetime в начале модуля
    return datetime.fromisoformat(date_str)


def get_date(date: str) -> str:
    """Форматирует дату в ДД.ММ.ГГГГ (для отображения)."""
    date_obj = parse_iso_date(date)
    # возвращаем в нужном формате с помощью метода .strftime()
    return date_obj.strftime("%d.%m.%Y")


print(mask_account_card('Maestro 1596837868705199'))
print(mask_account_card('Счет 64686473678894779589'))
print(mask_account_card(''))

print(get_date("2024-03-11T02:26:18.671407"))
