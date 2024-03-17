import asyncio
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from src.parser_subito import SubitoParser
from .markups import *
from src.database import AccountDatabase
from src.price import price_txt

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


TOKEN = '123'

bot = Bot(token=TOKEN)
dp = Dispatcher()
database = AccountDatabase()
subito_parser = SubitoParser(bot)


@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    if not database.user_exists(user_id):  # Создаем пользователя
        database.add_user(user_id)
        await bot.send_message(user_id, 'Приветствую', reply_markup=main_state)


@dp.message()
async def bot_message(message: types.Message):
    user_id = message.from_user.id
    if message.chat.type == 'private':
        if database.get_state(user_id) == 'main':
            if message.text == 'Проверить срок действия подписки':
                subscribe_time = database.get_subscribe(user_id)
                is_subscribe_valid = subscribe_time >= datetime.now()
                if is_subscribe_valid:
                    text = f'Подписка действительна до: {subscribe_time.strftime("%d.%m.%Y %H:%M:%S")}'
                else:
                    text = 'Подписка недействительна'
                await bot.send_message(user_id, text, reply_markup=subscribe_state)
                database.set_state(user_id, 'subscribe')

            elif message.text == 'Проверить баланс':
                await bot.send_message(user_id, f'Текущий баланс: {database.get_balance(user_id)} $', reply_markup=balance_state)
                database.set_state(user_id, 'balance')

            elif message.text == 'Запустить поиск объявлений':

                if subito_parser.is_running():
                    await bot.send_message(user_id, 'Поиск уже запущен')
                else:
                    subscribe_time = database.get_subscribe(user_id)
                    is_subscribe_valid = subscribe_time >= datetime.now()
                    if is_subscribe_valid:
                        await bot.send_message(user_id, 'Поиск успешно запущен')
                        await subito_parser.start(user_id)
                    else:
                        await bot.send_message(user_id, 'Подписка недействительна')

            elif message.text == 'Остановить поиск объявлений':
                if subito_parser.is_running():
                    subito_parser.stop()
                await bot.send_message(user_id, 'Поиск завершен', reply_markup=main_state)

        elif database.get_state(user_id) == 'subscribe':
            if message.text == 'Назад':

                await bot.send_message(user_id, '...', reply_markup=main_state)
                database.set_state(user_id, 'main')

            elif message.text == 'Продлить':
                current_balance = database.get_balance(user_id)
                await bot.send_message(user_id, f'Выбери желаемую подписку, баланс: {current_balance}$', reply_markup=add_subscribe_state)
                database.set_state(user_id, 'add_subscribe')

        elif database.get_state(user_id) == 'add_subscribe':
            if message.text == 'Назад':

                await bot.send_message(user_id, '...', reply_markup=main_state)
                database.set_state(user_id, 'main')

            elif message.text in price_txt:
                days, _, price_ = message.text.split(' ')
                price_ = int(price_[1:-2])
                balance = database.get_balance(user_id)
                if balance < price_:
                    await bot.send_message(user_id, 'Для покупки этой подписки недостаточно средств', reply_markup=add_subscribe_state)
                else:
                    database.set_balance(user_id, balance-price_)
                    new_subscribe_time = database.add_subscribe(user_id, int(days))

                    await bot.send_message(user_id, f'Подписка успешно продлена до {new_subscribe_time}, текущий баланс: {balance-price_} $', reply_markup=main_state)
                    database.set_state(user_id, 'main')

        elif database.get_state(user_id) == 'balance':
            if message.text == 'Назад':
                await bot.send_message(user_id, '...', reply_markup=main_state)
                database.set_state(user_id, 'main')

            elif message.text == 'Пополнить':
                await bot.send_message(user_id, 'Пока не умею, обратись к славику', reply_markup=main_state)
                database.set_state(user_id, 'main')

    # if user_id != 1580689542:
    #     await bot.send_message(1580689542, f'user: {user_id}, message: {message.text}')


async def main():
    await dp.start_polling(bot)


def is_alpha_only(s):
    # Регулярное выражение для проверки наличия только букв английского алфавита верхнего и нижнего регистров
    pattern = re.compile(r'^[a-zA-Z]+$')
    return bool(pattern.match(s))


if __name__ == '__main__':
    asyncio.run(main())
