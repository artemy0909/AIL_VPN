from aiogram.fsm.state import StatesGroup, State


class Start(StatesGroup):
    waiting_for_token = State()
