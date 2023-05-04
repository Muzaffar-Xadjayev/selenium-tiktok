from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

admins_command = InlineKeyboardMarkup(row_width=2)
btn = InlineKeyboardButton(text="👮‍♀️ Akkauntlar",callback_data="tiktok_accounts")
admins_command.add(btn)

manage_account = InlineKeyboardMarkup(row_width=1)
add_btn = InlineKeyboardButton(text="👮‍♀️ Akkaunt qo'shish",callback_data="add_tiktok_account")
remove_btn = InlineKeyboardButton(text="❌️ Akkaunt o'chirish",callback_data="delete_tiktok_account")
manage_account.add(add_btn,remove_btn)

cancel_btn = InlineKeyboardMarkup(row_width=1)
cancel = InlineKeyboardButton(text="🔙 Bekor qilish", callback_data="cancel_states")
cancel_btn.add(cancel)