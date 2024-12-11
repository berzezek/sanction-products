import schedule
import time

from config import logger
from data import create_xlsx
from parser import parse_dual_use_goods, parse_sanctioned
from sender import send_email

from config import SEND_TIME

def job():
    logger.info('Запуск приложения')
    data_site1 = parse_dual_use_goods()
    data_site2 = parse_sanctioned()
    create_xlsx(data_site1, data_site2)
    send_email()
    logger.info('Завершение работы приложения')

schedule.every().day.at(SEND_TIME, "Asia/Tashkent").do(job)



while True:
    schedule.run_pending()
    time.sleep(60)