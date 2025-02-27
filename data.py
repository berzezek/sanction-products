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
    
    special_codes = {"4201", "8483", "8484", "8426"}  # Коды, требующие особой обработки

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
                    if code in special_codes:
                        processed_data.append([
                            code,        # Код
                            row[1],      # Описание ENG
                            row[3],      # Страна → Наименование RUS
                            row[4],      # Тип → Страна
                            "Экспорт в РФ"  # Вид
                        ])
                    else:
                        processed_data.append([
                            code,        # Код
                            row[1],      # Описание ENG
                            row[-3],     # -3 элемент
                            row[-2],     # -2 элемент
                            row[-1],     # -1 элемент
                        ])
        else:
            if first_element.isdigit() or first_element.replace(" ", "").isdigit():
                if first_element in special_codes:
                    processed_data.append([
                        first_element.strip(),  # Код
                        row[1],                # Описание ENG
                        row[3],                # Страна → Наименование RUS
                        row[4],                # Тип → Страна
                        "Экспорт в РФ"         # Вид
                    ])
                else:
                    processed_data.append([
                        first_element.strip(),  # Код
                        row[1],                # Описание ENG
                        row[-3],               # -3 элемент
                        row[-2],               # -2 элемент
                        row[-1],               # -1 элемент
                    ])

    return processed_data



def create_xlsx(sanctioned_data, dual_use_data1, dual_use_data2, filename=FILE_NAME):
    """
    Создает Excel-файл с объединенными данными, сортируя сначала по 'Типу', затем по 'Стране'.
    """
    # Создаем новую книгу
    wb = Workbook()
    ws = wb.active
    ws.title = "Товары"

    # Заголовки столбцов
    headers = ["Код", "Наименование ENG", "Наименование RUS", "Страна", "Тип", "Вид"]
    ws.append(headers)

    # Объединяем все данные в один список с пометкой типа
    all_data = []
    
    for item in sanctioned_data:
        all_data.append(item + ['', '', '', "Товары двойного назначения"])

    for item in dual_use_data1:
        all_data.append(item + ["Санкционный"])

    for item in dual_use_data2:
        all_data.append(item + ["Санкционный"])

    # Сортируем сначала по 'Типу' (5-й индекс), затем по 'Стране' (3-й индекс)
    all_data.sort(key=lambda x: (x[4], x[3]))

    # Добавляем отсортированные данные в Excel
    for item in all_data:
        ws.append(item)

    # Устанавливаем автофильтр
    ws.auto_filter.ref = ws.dimensions

    # Сохраняем файл
    wb.save(filename)
    logger.info(f"Файл '{filename}' успешно создан и отсортирован!")




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

