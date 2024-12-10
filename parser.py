import pandas as pd

from requests_html import HTMLSession

from config import FILE_NAME, TIMEOUT, logger


def parse_data():
    # URL и заголовки
    url = 'https://traderadar.kz/tnved'
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
    all_data = []
    filtered_data = []

    if tables:
        for table in tables:
            rows = table.find('tr')
            for row in rows:
                cells = row.find('td')
                row_data = [cell.text.strip() for cell in cells]
                if row_data:  # Сохраняем только непустые строки
                    all_data.append(row_data)
                    # Если первый элемент содержит только цифры и запятые, добавляем в фильтрованные данные
                    if row_data[0].replace(',', '').isdigit():
                        filtered_data.append(row_data)
    else:
        logger.warning('Таблицы не найдены')

    # Создаём DataFrames
    df_all = pd.DataFrame(all_data)
    df_filtered = pd.DataFrame(filtered_data)

    # Сохраняем в файл Excel
    output_file = FILE_NAME
    with pd.ExcelWriter(output_file) as writer:
        df_all.to_excel(writer, sheet_name='Все данные', index=False, header=False)
        df_filtered.to_excel(writer, sheet_name='Фильтрованные', index=False, header=False)

    logger.info(f"Данные успешно сохранены в файл: {output_file}")
