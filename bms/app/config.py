import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


class Config:
    # Flask/General
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///bms.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.mailtrap.io')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 2525))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    NOTIFICATIONS_EMAIL = os.getenv('NOTIFICATIONS_EMAIL', 'admin@bms.com')

    # Batch processing
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 'json')  # 'json' or 'text'

    # Scraper
    SCRAPING_TIMEOUT = int(os.getenv('SCRAPING_TIMEOUT', 30))
    USE_SELENIUM = os.getenv('USE_SELENIUM', 'false').lower() == 'true'
