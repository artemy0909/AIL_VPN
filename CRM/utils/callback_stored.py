import json
import uuid
from datetime import datetime
from typing import Type, TypeVar

from aiogram.filters.callback_data import CallbackData
from redis import Redis

from utils.config import Config

callback_redis = Redis.from_url(Config.REDIS_CALLBACK_DATA_URL)


def set_callback(key: str, data: str):
    data_item = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": data
    }
    callback_redis.set(key, json.dumps(data_item))


def get_callback(key: str) -> str | None:
    redis_data = callback_redis.get(key).decode()
    if not redis_data:
        return None
    else:
        data_item = json.loads(redis_data)
        return data_item["data"]


T = TypeVar("T", bound="CallbackDataStored")


class CallbackDataStored(CallbackData, prefix=""):

    def pack(self):
        model_dict = super().model_dump_json()
        guid = str(uuid.uuid4())
        set_callback(key=guid, data=model_dict)
        callback_data = self.__separator__.join([self.__prefix__, guid])
        return callback_data

    @classmethod
    def unpack(cls: Type[T], value: str) -> T | None:

        try:
            prefix, guid = value.split(cls.__separator__)
            if prefix != cls.__prefix__:
                raise ValueError(f"Bad prefix ({prefix!r} != {cls.__prefix__!r})")

            model_dict = get_callback(guid)

            if not model_dict:
                return None
            else:
                return cls.parse_raw(model_dict)
        except BaseException as e:
            pass
