import smtplib
import pytz

from datetime import datetime
from dotenv import dotenv_values
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from config import APP_EMAIL_PASS, APP_SMTP_SERVER, APP_EMAIL_SENDER, APP_EMAIL_RECEIVER, FILE_NAME, logger

current_time = datetime.now(pytz.timezone('Asia/Almaty')).strftime('%Y-%m-%d %H:%M:%S')

def send_email():
    logger.info("Отправка письма...")
    # Настройки почты
    smtp_server = APP_SMTP_SERVER  # Для Яндекса: 'smtp.yandex.com' или 'smtp.yandex.ru'
    smtp_port = 465  # SSL-порт
    email_user = APP_EMAIL_SENDER
    email_password = APP_EMAIL_PASS
    recipient_email = APP_EMAIL_RECEIVER

    # Файл для отправки
    file_path = Path(FILE_NAME)

    if not file_path.exists():
        logger.error(f"Файл {file_path} не найден!")
        return

    # Создание сообщения
    subject = f'Данные по санкционным товарам от {current_time}'
    body = 'Пожалуйста, найдите во вложении Excel-файл с данными.'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    logger.info(f"Отправка письма на адрес {recipient_email}...")

    # Добавление файла во вложение
    try:
        with open(file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={file_path.name}'
        )
        msg.attach(part)

        # Отправка письма
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:  # Используем SMTP_SSL для SSL-соединения
            server.login(email_user, email_password)
            server.sendmail(email_user, recipient_email, msg.as_string())
            logger.info("Письмо успешно отправлено!")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма: {e}")
