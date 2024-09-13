from keyboard.cache import Delivery, load_from_cache

from utils.cache import create_tables

create_tables()

guid = Delivery(amount=2).dump_in_cache()

delivery = load_from_cache(Delivery, guid)

print(delivery.amount)
