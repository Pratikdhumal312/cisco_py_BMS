import os
from dotenv import load_dotenv

# Load variables from .env file if present
load_dotenv()

class Config:
    # 🔐 Flask / General
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-this")

    # 🗄️ Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///bms.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 📧 Email Configuration (Gmail)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "pratikdhumal312@gmail.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "ocvmmsnpmelojlxz")
    NOTIFICATIONS_EMAIL = os.getenv("NOTIFICATIONS_EMAIL", "jahnavichopparapu@gmail.com")

    # ⚙️ Batch Processing
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))

    # Email test mode (when True, emails are not actually sent; useful for local/dev/testing)
    EMAIL_TEST_MODE = os.getenv("EMAIL_TEST_MODE", "false").lower() == "true"

    # 🧾 Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "json")  # or "text"

    # 🌐 Scraper
    SCRAPING_TIMEOUT = int(os.getenv("SCRAPING_TIMEOUT", 30))
    USE_SELENIUM = os.getenv("USE_SELENIUM", "false").lower() == "true"
