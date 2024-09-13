from datetime import datetime

from peewee import *

from utils.config import Config

db = SqliteDatabase(Config.DB_CACHE_PATH)


class CallbackCache(Model):
    key = CharField(primary_key=True)
    data = CharField(max_length=2 ** 14 - 1)
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db
