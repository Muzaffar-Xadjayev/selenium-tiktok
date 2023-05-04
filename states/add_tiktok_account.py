from aiogram.dispatcher.filters.state import StatesGroup,State

class Add_TikTok(StatesGroup):
    username_or_email = State()
    password = State()
    text = State()