from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

admins_command = InlineKeyboardMarkup(row_width=2)
btn = InlineKeyboardButton(text="👮‍♀️ Akkaunt qo'shish",callback_data="add_tiktok_accaunt")
btn1 = InlineKeyboardButton(text="💬 Akkauntga text qo'shish",callback_data="add_tiktok_text")
admins_command.add(btn,btn1)