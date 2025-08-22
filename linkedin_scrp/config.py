# config.py
from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    # Authentication
    USER_AGENT = os.getenv("USER_AGENT")
    CSRF_TOKEN = os.getenv("CSRF_TOKEN")
    COOKIE = os.getenv("COOKIE")

    # API Configuration
    BASE_URL = os.getenv("BASE_URL")
    QUERY_ID = os.getenv("QUERY_ID")

    # Company Configuration
    COMPANY_ID = os.getenv("COMPANY_ID")
    COMPANY_SLUG = os.getenv("COMPANY_SLUG")

    # Pagination
    START = int(os.getenv("START", "0"))
    END = int(os.getenv("END", "100"))
    STEP = int(os.getenv("STEP", "20"))