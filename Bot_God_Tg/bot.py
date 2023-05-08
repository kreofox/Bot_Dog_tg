from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
fron aiogram import types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
import json
import random


bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)

class GuessNumber(StatesGroup):
    waiting_for_number = State()

class TicTacToe(StatesGroup):
    turn = State()  # Состояние, когда ход игрока
    waiting = State()  # Состояние, когда ожидание хода оппонента
    game_over = State()  # Состояние, когда игра окончена

# Создаем бота, диспетчер и хранилище
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Игровое поле
game_board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

# Отрисовка клавиатуры для игрового поля
def get_game_keyboard():
    keyboard = InlineKeyboardMarkup()
    for row in range(3):
        row_buttons = []
        for col in range(3):
            if game_board[row][col] is None:
                button_text = '-'
                callback_data = f'coord_{row}_{col}'
            else:
                button_text = game_board[row][col]
                callback_data = '-'
            row_buttons.append(InlineKeyboardButton(button_text, callback_data=callback_data))
        keyboard.row(*row_buttons)
    return keyboard

# Определение победителя
def get_winner():
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] and game_board[i][0] is not None:
            return game_board[i][0]
        if game_board[0][i] == game_board[1][i] == game_board[2][i] and game_board[0][i] is not None:
            return game_board[0][i]
    if game_board[0][0] == game_board[1][1] == game_board[2][2] and game_board[0][0] is not None:
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] and game_board[0][2] is not None:
        return game_board[0][2]
    if None not in game_board[0] and None not in game_board[1] and None not in game_board[2]:
        return 'tie'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, f'Привет {message.from_user.id}, я Собока бот. Чтобы узнать мои команды, напиши /info')

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('Контакт', callback_data='Contact')
    btn2 = types.InlineKeyboardButton('GitHub', callback_data='GitHub')
    btn3 = types.InlineKeyboardButton('shop', callback_data='Shop')
    btn4 = types.InlineKeyboardButton('Угадай', callback_data='Games')
    btn5 = types.InlineKeyboardButton('Крести и Нолики', callback_data = 'Zero')
    markup.add(btn1, btn2, btn3, btn4, btn5)
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
    await message.answer(f"Name: {res['name']}. Email{res['email']}. Phone: {res['phone']}")

@dp.message_handler(commands=['Games'])
async def Games(message: types.Message):
    number = random.randint(1, 100)
    await message.answer('Я хагадал число 1 до 100. Попробуйте его угадать!')
    await GuessNumber.waiting_for_number.set()

@dp.message_handler(state=GuessNumber.waiting_for_number, content_types.ContentType.TEXT)
async def check_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        number = data['number']
    try:
        user_number = int(message.text)
    except ValueError:
        await message.answer('Введите число')
        return
    if user_number > number:
        await message.answer('Прости, но число не верное!')
    elif user_number < number:
        await message.answer('Прости, но число не верное!')
    else:
        await message.answer('Проздравляю, вы угадали число!')
        await state.finish()

@dp.message_handler(command = ['Zero'])
async def  Zero_games(message: types.Message):
    await message.answer('Привет! Давай сыграем в крестики-нолики')
    await message.answer('Выбери крестики или нолики', reply.markup=ReplyKeyboardMarkup(resize_keyboard=True))

    

excutor.start_polling(dp)