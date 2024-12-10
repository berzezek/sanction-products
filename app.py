from config import logger
from parser import parse_data
from sender import send_email


if __name__ == '__main__':
    logger.info('Запуск приложения')
    parse_data()
    send_email()
    logger.info('Завершение работы приложения')