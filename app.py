import time

import schedule

from data import create_xlsx, process_data_correctly, filter_numeric_data
from parser import parse_dual_use_goods, parse_sanctioned
from sender import send_email

from config import URL1, URL2, logger

logger.info('Запуск приложения Docker')

def job():
    logger.info('Запуск приложения')
    data_site1 = parse_dual_use_goods(URL1)
    data_site2 = parse_dual_use_goods(URL2)
    data_site3 = parse_sanctioned()
    create_xlsx(filter_numeric_data(data_site3), process_data_correctly(data_site1), process_data_correctly(data_site2))
    send_email()
    logger.info('Завершение работы приложения')

# schedule.every(12).hours.do(job)

job()


# while True:
#     schedule.run_pending()
#     time.sleep(1)