from data import create_xlsx, save_to_file, save_to_xlsx, process_data_correctly, filter_numeric_data
from parser import parse_dual_use_goods, parse_sanctioned
from sender import send_email

from config import SEND_TIME, logger

def job():
    logger.info('Запуск приложения')
    data_site1 = parse_dual_use_goods()
    data_site2 = parse_sanctioned()
    create_xlsx(filter_numeric_data(data_site2), process_data_correctly(data_site1))
    send_email()
    logger.info('Завершение работы приложения')

if __name__ == '__main__':
    job()