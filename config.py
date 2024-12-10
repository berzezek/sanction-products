import logging

from dotenv import dotenv_values

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config = dotenv_values(".env")

APP_EMAIL_PASS = config["APP_EMAIL_PASS"]
APP_SMTP_SERVER = config["APP_SMTP_SERVER"]
APP_EMAIL_SENDER = config["APP_EMAIL_SENDER"]
APP_EMAIL_RECEIVER = config["APP_EMAIL_RECEIVER"]
TIMEOUT = int(config["TIMEOUT"])

FILE_NAME='parsed_data_with_filtered.xlsx'