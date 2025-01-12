from dataclasses import dataclass
from os import getenv as __getenv

from dotenv import load_dotenv

load_dotenv()


def getenv(key):
    var = __getenv(key)
    if var is None:
        raise ValueError(f"Environment variable {key} not set")
    return var


@dataclass
class _Config:
    MARKET_BOT_TOKEN = getenv("MARKET_BOT_TOKEN")
    SERVICE_BOT_TOKEN = getenv("SERVICE_BOT_TOKEN")
    PAYMENT_TOKEN = getenv("PAYMENT_TOKEN")
    MAIN_PAYMENT_METHOD = getenv("MAIN_PAYMENT_METHOD")
    ERROR_REPORTS_PATH = getenv("ERROR_REPORTS_PATH")
    REDIS_CALLBACK_DATA_URL = getenv("REDIS_CALLBACK_DATA_URL")
    REDIS_STATE_FSM_URL = getenv("REDIS_STATE_FSM_URL")
    XENON_API_URL = getenv("XENON_API_URL")
    XENON_LOGIN = getenv("XENON_LOGIN")
    XENON_PASSWORD = getenv("XENON_PASSWORD")


Config = _Config()
