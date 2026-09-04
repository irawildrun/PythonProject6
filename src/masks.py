# Реализация функций маскировки номера карты и банковского счета


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты по формату XXXX XX** **** XXXX."""
    if not (card_number.isdigit() and len(card_number) == 16):
        raise ValueError("Номер карты должен содержать 16 цифр.")

    # Поскольку на вход принимаем строку, можем использовать срезы.
    return card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета по формату **XXXX."""
    if not (account_number.isdigit() and len(account_number) >= 4):
        raise ValueError("Номер счета должен содержать минимум 4 цифры.")

    # Поскольку на вход принимаем строку, можем использовать срезы.
    return "**" + account_number[-4:]


# Ручной ввод для проверки функций.
# Сделаем проверку с ручным вводом, только если запуск функции происходит в этом файле
if __name__ == "__main__":
    card_number = input("Введите номер карты, без пробелов 16 цифр: ").strip()
    account_number = input("Введите номер банковского счета минимум 4 цифры: ").strip()

    print(get_mask_card_number(card_number))
    print(get_mask_account(account_number))
