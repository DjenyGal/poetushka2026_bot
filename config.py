import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")

GPTUNNEL_API_KEY = os.getenv("GPTUNNEL_API_KEY")
GPTUNNEL_BASE_URL = "https://gptunnel.ru/v1"
CLAUDE_MODEL = "claude-5-sonnet"

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

PRICES = {
    "short": 349,
    "medium": 549,
    "long": 849,
}

LENGTH_LABELS = {
    "short": "Короткое (примерно 200 слов)",
    "medium": "Среднее (присерно 400 слов)",
    "long": "Длинное (примерно 800 слов)",
}