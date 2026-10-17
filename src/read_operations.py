import csv
import json
import pandas as pd


def read_csv_operations(path):
    """Читает финансовые операции из CSV-файла"""
    try:
        #  в файле данные разделены ;, поэтому нужно указать разделитель
        data = pd.read_csv(path, sep=";")
        # датафрейм переводим в формат словаря
        result = data.to_dict(orient="records")
        return result
    except Exception as e:
        print(f'Ошибка при чтении файла: {e}')
        return []



if __name__ == '__main__':
    csv_operations = read_csv_operations('../data/transactions.csv')
    # сделаем "красивый" вывод с отступами для большей информативности
    print(json.dumps(csv_operations[:3], indent=4, ensure_ascii=False))
    # print(json.dumps(csv_operations, indent=4, ensure_ascii=False))
    print(len(csv_operations))

