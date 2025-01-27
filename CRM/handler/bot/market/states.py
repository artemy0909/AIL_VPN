from aiogram.fsm.state import StatesGroup, State


class Start(StatesGroup):
    wait_to_promo_code = State()
