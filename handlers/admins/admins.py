from aiogram import types
from data.config import ADMINS,ADMINS_NAME
from keyboards.inline.admins import admins_command
from loader import dp,bot


@dp.message_handler(commands=["admin"],user_id=ADMINS)
async def intro(msg: types.Message):
    await bot.send_message(msg.from_user.id,f"Xush Kelibsiz <b>{msg.from_user.full_name}</b> – ADMIN",reply_markup=admins_command)

@dp.callback_query_handler(text_contains=["add_tiktok_accaunt"])
async def add_account(call: types.CallbackQuery):
    pass