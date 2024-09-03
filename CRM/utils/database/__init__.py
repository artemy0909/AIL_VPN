from .brom import *
from ..config import Config

brom_client = БромКлиент(Config.BROM_API_URL, Config.BROM_LOGIN, Config.BROM_PASSWORD)
brom_client.ЗагрузитьМетаданные("*")
