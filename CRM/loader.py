import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils.config import Config
from utils.database import database


database.test()
logging.basicConfig(level=logging.INFO)

market_bot = Bot(Config.MARKET_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
service_bot = Bot(Config.SERVICE_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

user_dp = Dispatcher()
service_dp = Dispatcher()
