import uuid
from typing import Type

from aiogram.filters.callback_data import CallbackData, T
from peewee import DoesNotExist

from utils.cache import CallbackCache


class CallbackDataStored(CallbackData, prefix=""):

    def pack(self):
        json_str = super().model_dump_json()
        guid = str(uuid.uuid4())
        CallbackCache.create(key=guid, data=json_str)
        callback_data = self.__separator__.join([self.__prefix__, guid])
        return callback_data

    @classmethod
    def unpack(cls: Type[T], value: str) -> T | None:

        prefix, guid = value.split(cls.__separator__)
        if prefix != cls.__prefix__:
            raise ValueError(f"Bad prefix ({prefix!r} != {cls.__prefix__!r})")

        try:
            callback_cache = CallbackCache.get(CallbackCache.key == guid)
        except DoesNotExist:
            return None

        return cls.parse_raw(callback_cache.data)
