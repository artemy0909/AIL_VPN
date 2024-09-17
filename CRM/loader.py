import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils import database
from utils.config import Config

# from handlers.event import Scheduler
if not database.connection.is_connected():
    raise ConnectionError("1C connection refused")

logging.basicConfig(level=logging.INFO)

market_bot = Bot(Config.MARKET_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
service_bot = Bot(Config.SERVICE_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

user_dp = Dispatcher()
service_dp = Dispatcher()
# scheduler = Scheduler(bot)
