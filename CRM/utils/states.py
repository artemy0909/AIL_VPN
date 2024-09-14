from aiogram.fsm.state import StatesGroup, State


class Start(StatesGroup):
    start = State()


class MenuCommands(StatesGroup):
    article = State()
