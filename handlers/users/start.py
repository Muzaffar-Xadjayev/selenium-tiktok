import datetime

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from database.connections import add_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    user_id=message.from_user.id
    username=message.from_user.username
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # ADD USER IN DB
    await add_user(
        user_id=user_id,
        full_name=name,
        username=username,
        join_date=time_now,
        message=message
    )
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!\n<b>TikTok bot</b>iga xush kelibsiz!")