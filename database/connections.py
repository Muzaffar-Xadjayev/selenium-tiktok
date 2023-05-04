from playhouse.shortcuts import model_to_dict
from data.config import ADMINS
from keyboards.inline.admins import manage_account, admins_command
from loader import bot
from .models import *

async def add_user(user_id,full_name,join_date,username,message):
    if not Users.select().where(Users.telegram_id == user_id).exists():
        Users.create(
            telegram_id=user_id,
            full_name=full_name,
            username=username,
            join_date=join_date
        )
        c = Users.select()
        count = [model_to_dict(item) for item in c]
        msg = f"{message.from_user.get_mention(as_html=True)} bazaga qo'shildi. Bazada {len(count)} ta foydalanuvchi bor"
        for admin in ADMINS:
            await bot.send_message(admin,msg)

async def add_login(username,password,text,user_id):
    if not Logins.select().where(Logins.username_or_email == username).exists():
        Logins.create(
            username_or_email = username,
            password = password,
            comment_text = text
        )
        msg = "✅ Yangi kirish uchun login parol bazaga saqlandi."
        await bot.send_message(user_id,msg,reply_markup=manage_account)
    else:
        msg1 = "Bu login parol bazada bor"
        await bot.send_message(user_id, msg1,reply_markup=manage_account)
