import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

bot = Bot(token="7058891972:AAEJaO1pu6S3oekH8wqZPFwVnXk2AWSqsUA")
dp = Dispatcher()
router = Router()

class Anketa(StatesGroup):
    """Class representing a person"""
    name = State()
    age = State()
    gender = State()

@router.message(Command("anketa"))
async def anketa_handler(msg: Message, state: FSMContext):
    """Function printing python version."""
    await state.set_state(Anketa.name)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
    await msg.answer('Введите ваше имя', reply_markup=markup)

@router.callback_query(F.data== 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    """Function printing python version."""
    await state.clear()
    await callback_query.message.answer('Регистрация отменена')

@router.message(Anketa.name)
async def set_name_by_anketa_handler(msg: Message, state: FSMContext):
    """Function printing python version."""
    await state.update_data(name=msg.text)
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='set_name_anketa'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
    await msg.answer('Введите ваш возраст', reply_markup=markup)


@router.callback_query(F.data== 'set_name_anketa')
async def set_name_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    """Function printing python version."""
    await anketa_handler(callback_query.message, state)

@router.message(Anketa.age)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
    """Function printing python version."""
    try:
        await state.update_data(age=int(msg.text))
    except ValueError:
        await msg.answer('Вы неверно ввели возраст!')
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Назад', callback_data='set_name_anketa'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
        await msg.answer('Введите ваш возраст', reply_markup=markup)
        return

    await state.set_state(Anketa.gender)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='set_name_anketa'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
    await msg.answer('Введите ваш пол', reply_markup=markup)

@router.callback_query(F.data== 'set_age_anketa')
async def set_age_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    """Function printing python version."""
    await state.set_state(Anketa.age)
    markup = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Назад', callback_data='set_name_anketa'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_anketa')]])
    await callback_query.message.answer('Введите ваш возраст', reply_markup=markup)


@router.message(Anketa.gender)
async def set_age_by_anket_handler(msg: Message, state: FSMContext):
    """Function printing python version."""
    await state.update_data(gender=msg.text)
    await msg.answer(str(await state.ger_data()))
    await state.clear()

@router.message(Command("start"))
async def start_handler(msg: Message):
    """Function printing python version.""" 
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='delete', description='Отчислиться'),
    ])


    inline_markup = InlineKey[InlineKeyboardButton(text='Вперёд', callback_data='next')]
    ])
    await msg.answer(text="Страница 1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
    """Function printing python version.""" 
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]

    ])

    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 2',
        reply_markup=inline_markup)

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    """Function printing python version.""" 
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вперёд', callback_data='next')]
    ])

    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 1',
        reply_markup=inline_markup)

async def main():
    """Function printing python version.""" 
    await dp.start_polling(bot)



dp.include_routers(router)

if __name__ == '__main__':
    asyncio.run(main())