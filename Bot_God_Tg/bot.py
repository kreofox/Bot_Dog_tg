from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.types.web_app_info import WebAppInfo

import config
import json

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, f'Привет {message.from_user.id}, я Собока бот. Чтобы узнать мои команды, напиши /info')

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Контакт', callback_data='Contact')
    btn2 = types.InlineKeyboardButton('GitHub', callback_data='GitHub')
    btn3 = types.InlineKeyboardButton('shop', callback_data='shop')
    btn4 = types.InlineKeyboardButton('', callback_data='')
    markup.add(btn1, btn2, btn3, btn4)
    await bot.send_message(message.chat.id, 'Выберите команду', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'Contact')
async def process_callback_contact(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Мои данные:')
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Telegram', url='https://t.me/Mancionde')
    btn2 = types.InlineKeyboardButton('Discord', url='https://discord.gg/WG6fpxzjvh')
    markup.add(btn1, btn2)
    await bot.send_message(callback_query.from_user.id, 'Писать туда', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'GitHub')
async def process_callback_github(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Портфолио:')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('GitHub', url='https://github.com/kreofox')
    markup.add(btn1)
    await bot

@dp.message_handler(commands = 'shop')
async def shop(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('shop', web_app=WebAppInfo(url = 'https://')))
    await message.answer('Выберите товар', reply_markup)

@dp.message_handler(content_types = ["web_app_data"])
async def wep_app(message: types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f'Name: {res['name']}. Email{res['email']}. Phone: {res['phone']}')
    

excutor.start_polling(dp)