import openpyxl
from openpyxl import Workbook
import pandas as pd

from config import logger, FILE_NAME

def filter_numeric_data(data):
    """
    Удаляет строки, где первый элемент не является числом.
    
    :param data: Список строк с данными
    :return: Отфильтрованный список
    """
    filtered_data = []
    for row in data:
        if row[0].isdigit():  # Проверяем, что первый элемент состоит только из цифр
            filtered_data.append(row)
    return filtered_data


def process_data_correctly(data):
    """
    Обрабатывает данные в соответствии с заданными условиями, включая удаление пробелов из первого элемента.
    
    :param data: Список строк с данными
    :return: Обработанный список
    """
    processed_data = []

    for row in data:
        if len(row) < 5:  # Пропуск строк с недостаточным количеством элементов
            continue

        # Убираем пробелы, буквы, слова
        first_element = row[0].replace(" ", "")  # Убираем пробелы
        if "или" in first_element:
            # Заменяем "или" на запятую и делим элементы
            first_element = first_element.replace("или", ",")
        if "," in first_element:
            # Создаем отдельные строки для каждого кода
            codes = first_element.split(",")
            for code in codes:
                code = code.strip()  # Убираем лишние пробелы
                if code.isdigit() or code.replace(" ", "").isdigit():
                    processed_data.append([
                        code,  # Новый код
                        row[1],  # Описание
                        row[-3],  # -3 элемент
                        row[-2],  # -2 элемент
                        row[-1],  # -1 элемент
                    ])
        else:
            # Проверяем, если элемент подходит под условия
            if first_element.isdigit() or first_element.replace(" ", "").isdigit():
                processed_data.append([
                    first_element.strip(),  # Убираем лишние пробелы
                    row[1],  # Описание
                    row[-3],  # -3 элемент
                    row[-2],  # -2 элемент
                    row[-1],  # -1 элемент
                ])

    return processed_data


def create_xlsx(sanctioned_data, dual_use_data, filename=FILE_NAME):
    """
    Создает Excel-файл с объединенными данными.
    :param sanctioned_data: Данные санкционных товаров
    :param dual_use_data: Данные товаров двойного назначения
    :param filename: Имя выходного файла
    """
    # Создаем новую книгу
    wb = Workbook()
    ws = wb.active
    ws.title = "Товары"

    # Заголовки столбцов
    headers = ["Код", "Наименование ENG", "Наименование RUS", "Страна", "Тип", "Вид"]
    ws.append(headers)

    # Обработка данных
    for item in sanctioned_data:
        item.append('')
        item.append('')
        item.append('')
        item.append("Товары двойного назначения")
        ws.append(item)

    for item in dual_use_data:
        item.append("Санкционный")
        ws.append(item)

    # Сохраняем файл
    wb.save(filename)
    logger.info(f"Файл '{filename}' успешно создан!")


def save_to_file(data, filename):
    """
    Сохраняет данные в файл.
    :param data: Данные для сохранения
    :param filename: Имя файла
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item}\n")



def save_to_xlsx(data):
    # Создаем DataFrame и добавляем столбцы
    columns = ["Код", "Наименование ENG", "Наименование RUS", "Страна", "Тип", "Вид"]
    df = pd.DataFrame(data, columns=columns[:len(data[0])])

    # Преобразуем DataFrame для Excel с учетом условий
    def transform_data(row):
        transformed_row = {col: None for col in columns}
        transformed_row["Код"] = row[0]
        transformed_row["Наименование ENG"] = row[1] if len(row) > 1 else None
        transformed_row["Наименование RUS"] = row[2] if len(row) > 2 else None
        transformed_row["Страна"] = row[3] if len(row) > 3 else None
        transformed_row["Тип"] = row[4] if len(row) > 4 else None
        transformed_row["Вид"] = "Товары двойного назначения" if "Экспорт в РФ" in row else None
        return transformed_row

    transformed_data = [transform_data(row) for row in data]
    df_transformed = pd.DataFrame(transformed_data)

    # Сохраняем в файл Excel
    output_path = 'processed_data.xlsx'
    df_transformed.to_excel(output_path, index=False, sheet_name="Данные")

