from playhouse.shortcuts import model_to_dict

from data.config import ADMINS
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