from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

async def show_btn(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in data:
        btn = InlineKeyboardButton(text=i["username_or_email"],callback_data=f"logins:{i['username_or_email']}")
        keyboard.add(btn)
    cancel_btn = InlineKeyboardButton(text="🔙 Bekor qilish",callback_data="cancel_delete_account")
    keyboard.add(cancel_btn)
    return keyboard

async def show_btn1(data):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in data:
        btn = InlineKeyboardButton(text=i["account"]["username_or_email"],callback_data=f"comment:{i['account']['username_or_email']}")
        keyboard.add(btn)
    cancel_btn = InlineKeyboardButton(text="🔙 Bekor qilish",callback_data="cancel_delete_account")
    keyboard.add(cancel_btn)
    return keyboard