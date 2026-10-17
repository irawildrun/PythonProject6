import csv
import json
import openpyxl
import pandas as pd


def read_csv_transactions(path):
    """Читает финансовые операции из CSV-файла"""
    try:
        #  в файле данные разделены ;, поэтому нужно указать разделитель
        data = pd.read_csv(path, sep=';')
        # датафрейм переводим в формат словаря со словарями как отдельными записями
        result = data.to_dict(orient='records')
        return result
    except Exception as e:
        print(f'Ошибка при чтении файла: {e}')
        return []


def read_excel_transactions(path):
    """Читает финансовые операции из excel-файла"""
    try:
        data = pd.read_excel(path)
        # датафрейм переводим в формат словаря со словарями как отдельными записями
        result = data.to_dict(orient='records')
        return result
    except Exception as e:
        print(f'Ошибка при чтении файла: {e}')
        return []


if __name__ == '__main__':
    csv_operations = read_csv_transactions('../data/transactions.csv')
    # сделаем "красивый" вывод с отступами для большей информативности
    print(json.dumps(csv_operations[:3], indent=4, ensure_ascii=False))
    # print(json.dumps(csv_operations, indent=4, ensure_ascii=False))
    print('csv', len(csv_operations))

    excel_operations = read_excel_transactions('../data/transactions_excel.xlsx')
    # сделаем "красивый" вывод с отступами для большей информативности
    print(json.dumps(excel_operations[:3], indent=4, ensure_ascii=False))
    # print(json.dumps(csv_operations, indent=4, ensure_ascii=False))
    print('excel', len(excel_operations))
