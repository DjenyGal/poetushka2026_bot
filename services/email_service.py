import smtplib
from email.mime.text import MIMEText
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS


async def send_greeting_email(email: str, text: str):
    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = "Ваше уникальное поздравление"
    msg["From"] = SMTP_USER
    msg["To"] = email

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)