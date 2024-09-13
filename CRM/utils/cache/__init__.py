from utils.cache.callback import db, CallbackCache


def create_tables():
    with db:
        db.create_tables([CallbackCache])
