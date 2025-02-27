import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from config import FILE_NAME, TIMEOUT, logger


def parse_dual_use_goods(url):
    """
    Парсит таблицы с сайта и форматирует данные.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    # Создание сессии
    session = HTMLSession()
    response = session.get(url, headers=headers)

    # Рендеринг JavaScript
    response.html.render(timeout=TIMEOUT)

    # Поиск всех таблиц
    tables = response.html.find('table')

    # Собираем данные
    data = []

    if tables:
        for table in tables:
            rows = table.find('tr')
            for row in rows:
                cells = row.find('td')
                # Очищаем данные от пустых строк и пробелов
                row_data = [cell.text.strip() for cell in cells if cell.text.strip()]
                
                if row_data:  # Проверяем, что строка не пустая
                    if row_data[0].replace(',', '').isdigit():
                        # Если первый элемент содержит запятые, разделяем
                        codes = row_data[0].split(',')
                        for code in codes:
                            formatted_row = [code.strip()] + row_data[1:]  # Форматируем строку
                            data.append(formatted_row)  # Добавляем в список
                    else:
                        # Если кодов нет, просто добавляем строку
                        data.append(row_data)
    else:
        logger.warning('Таблицы не найдены')
    
    return data


def parse_sanctioned():

    # URL страницы
    url = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02014R0833-20240625'

    # Заголовки запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    # Создание сессии
    session = HTMLSession()
    response = session.get(url, headers=headers)

    # Рендеринг JavaScript
    response.html.render(timeout=TIMEOUT)

    # Поиск <p> с нужным текстом
    target_paragraph = response.html.find("p.title-gr-seq-level-1", first=False)

    table = None  # Объект для хранения таблицы

    for paragraph in target_paragraph:
        if "List of goods and technology as referred to in Article 12g" in paragraph.text:
            # Используем BeautifulSoup для работы с деревом элементов
            soup = BeautifulSoup(response.html.html, "html.parser")
            parent_div = soup.find("p", string="List of goods and technology as referred to in Article 12g").find_parent("div")
            table = parent_div.find("table", class_="borderOj") if parent_div else None
            if table:
                break

    # Сохраняем данные из строк
    data = []
    if table:
        rows = table.find_all("tr")  # Ищем все строки в таблице
        for row in rows:
            cells = row.find_all("td")  # Ищем ячейки в строке
            row_data = [cell.get_text(strip=True).replace('\xa0', '') for cell in cells]
            if row_data:  # Если строка не пустая
                data.append(row_data)

    return data