from aiogram.dispatcher.filters.state import State,StatesGroup

class Add_text(StatesGroup):
    account = State()
    text = State()