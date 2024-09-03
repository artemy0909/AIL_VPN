from dataclasses import dataclass

from dotenv import load_dotenv
from os import getenv

load_dotenv()


@dataclass
class Config:
    MARKET_BOT_TOKEN = getenv("MARKET_BOT_TOKEN")
    SERVICE_BOT_TOKEN = getenv("SERVICE_BOT_TOKEN")
    BROM_API_URL = getenv("BROM_API_URL")
    BROM_LOGIN = getenv("BROM_LOGIN")
    BROM_PASSWORD = getenv("BROM_PASSWORD")
