import openpyxl
from openpyxl import Workbook

from config import FILE_NAME, logger

def create_xlsx(data_site1, data_site2, filename=FILE_NAME):
    # Создаем книгу и лист
    wb = Workbook()
    ws = wb.active
    ws.title = "Санкционные товары"
    
    # Заголовки столбцов
    headers = ["Код", "Наименование ENG", "Наименование RUS", "Страна", "Тип", "Вид"]
    ws.append(headers)
    
    # Записываем данные с первого сайта
    for item in data_site1:
        try:
            row = [
                item[0],              # Код
                item[1],              # Наименование ENG
                item[2],              # Наименование RUS
                item[3],              # Страна
                item[4],              # Тип
                "Санкционный"         # Вид
            ]
            ws.append(row)
        except Exception as e:
            logger.error(f"Ошибка при записи данных: {e}")
            continue
    
    # Записываем данные со второго сайта
    for item in data_site2:
        try:
            row = [
                item[0],              # Код
                item[1],              # Наименование ENG
                None,                 # Наименование RUS
                None,                 # Страна
                None,                 # Тип
                "Товары двойного назначения"  # Вид
            ]
            ws.append(row)
        except Exception as e:
            logger.error(f"Ошибка при записи данных: {e}")
            continue
    
    # Сохраняем файл
    wb.save(filename)
    logger.info(f"Файл '{filename}' успешно создан!")


