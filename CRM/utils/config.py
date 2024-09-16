from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    MARKET_BOT_TOKEN = getenv("MARKET_BOT_TOKEN")
    SERVICE_BOT_TOKEN = getenv("SERVICE_BOT_TOKEN")
    PAYMENT_TOKEN = getenv("PAYMENT_TOKEN")
    BROM_API_URL = getenv("BROM_API_URL")
    BROM_LOGIN = getenv("BROM_LOGIN")
    BROM_PASSWORD = getenv("BROM_PASSWORD")
    # DB_CACHE_PATH = getenv("DB_CACHE_PATH")
    ERROR_REPORTS_PATH = getenv("ERROR_REPORTS_PATH")
    REDIS_CALLBACK_DATA_URL = getenv("REDIS_CALLBACK_DATA_URL")
    REDIS_STATE_FSM_URL = getenv("REDIS_STATE_FSM_URL")
