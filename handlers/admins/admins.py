from aiogram import types
from aiogram.dispatcher import FSMContext
from playhouse.shortcuts import model_to_dict

from data.config import ADMINS,ADMINS_NAME
from database.connections import add_login
from database.models import *
from keyboards.inline.admins import admins_command, manage_account,cancel_btn
from keyboards.inline.show_btn import show_btn, show_btn1
from states.add_tiktok_account import Add_TikTok
from states.add_text import Add_text
from loader import dp,bot


@dp.message_handler(commands=["admin"],user_id=ADMINS)
async def intro(msg: types.Message):
    await bot.send_message(msg.from_user.id,f"Xush Kelibsiz <b>{msg.from_user.full_name}</b> – ADMIN",reply_markup=admins_command)

@dp.callback_query_handler(text="tiktok_accounts")
async def manage_logins(call: types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.edit_text("Nima qilishni xohlaysiz ?",reply_markup=manage_account)

@dp.callback_query_handler(text=["add_tiktok_account"])
async def add_account(call: types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    text2 = await call.message.answer("TikTok ga kirish uchun <b>username</b> yoki <b>e-pochta</b> kiriting: ",reply_markup=cancel_btn)
    await state.update_data(
        {"id_1":text2.message_id}
    )
    await Add_TikTok.username_or_email.set()

@dp.message_handler(state=Add_TikTok.username_or_email,user_id=ADMINS)
async def get_username_or_email(msg: types.Message, state:FSMContext):
    text1 = await msg.answer("Yangi akkaunt uchun parolni kiriting: ",reply_markup=cancel_btn)
    await state.update_data(
        {"username": msg.text,
         "id_2":text1.message_id}
    )
    await Add_TikTok.password.set()

@dp.message_handler(state=Add_TikTok.password,user_id=ADMINS)
async def get_password(msg: types.Message, state:FSMContext):
    text2 = await msg.answer("Yangi Akkauntning kamentariya uchun text ni kiriting: ",reply_markup=cancel_btn)
    await state.update_data(
        {"password":msg.text,
         "id_3":text2.message_id}
    )
    await Add_TikTok.text.set()


@dp.message_handler(state=Add_TikTok.text)
async def get_text(msg: types.Message, state:FSMContext):
    await state.update_data(
        {"text":msg.text}
    )
    data = await state.get_data()
    await add_login(data["username"], data["password"],data["text"], msg.from_user.id)
    await bot.delete_message(msg.chat.id, data["id_1"])
    await bot.delete_message(msg.chat.id, data["id_2"])
    await bot.delete_message(msg.chat.id, data["id_3"])
    await state.finish()

@dp.callback_query_handler(text="cancel_states",state=[Add_TikTok.password,Add_TikTok.username_or_email,Add_TikTok.text])
async def cancel_state(call: types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.edit_text("🏠 Bosh Menu",reply_markup=admins_command)
    await state.finish()

@dp.callback_query_handler(text="delete_tiktok_account")
async def delete_logins(call: types.CallbackQuery):
    await call.answer()
    d = Logins.select()
    data = [model_to_dict(i) for i in d]
    btn = await show_btn(data)
    await call.message.edit_text("👇 Qaysi Akkauntni o'chirmoqchisiz ?",reply_markup=btn)

@dp.callback_query_handler(text="cancel_delete_account",state="*")
async def cancel_delete(call: types.CallbackQuery,state:FSMContext):
    await call.answer()
    await call.message.edit_text("🏠 Bosh Menu", reply_markup=admins_command)
    await state.finish()

@dp.callback_query_handler(text_contains=["logins:"])
async def delete_log(call: types.CallbackQuery):
    await call.answer()
    username = call.data.split("logins:")[1]
    Logins.delete().where(Logins.username_or_email == username).execute()
    await call.message.edit_text(f"{username} ga tegishli login va parollar o'chirildi ✅.",reply_markup=manage_account)
