import asyncio
import re
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from parser_subito import SubitoParser
from tg_bot import markups as nav
from tg_bot.database import AccountDatabase
from tg_bot.price import price_txt


# TOKEN = '321'
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

    if database.account_exists(user_id):  # Если аккаунт существует
        await bot.send_message(user_id, 'Вы уже зарегистрированы', reply_markup=nav.main_state)
        database.set_state(user_id, 'main')
    else:
        await bot.send_message(user_id, 'Привет, твоего аккаунта ещё не существует, предлагаю исправить', reply_markup=nav.start_state)


@dp.message()
async def bot_message(message: types.Message):
    user_id = message.from_user.id
    if message.chat.type == 'private':

        if message.text == 'Зарегистрироваться' and not database.account_exists(user_id):
            database.set_state(user_id, 'registration')
            await bot.send_message(user_id, 'Введите логин и пароль через пробел', reply_markup=nav.registration_state)

        else:
            if database.get_state(user_id) == 'registration':
                msg_data = message.text.split(' ')
                if len(msg_data) != 2:
                    await bot.send_message(user_id, 'Введено неверное количество слов', reply_markup=nav.registration_state)
                else:
                    login, password = msg_data
                    if len(login) < 5 or len(login) > 15:
                        await bot.send_message(user_id, 'Длина логина должна быть от 5 до 15 символов', reply_markup=nav.registration_state)
                    elif not is_alpha_only(login):
                        await bot.send_message(user_id, 'Логин должен состоять только из строчных или заглавных букв английского алфавита', reply_markup=nav.registration_state)
                    elif len(password) < 5 or len(password) > 25:
                        await bot.send_message(user_id, 'Длина пароля должна быть от 5 до 25 символов', reply_markup=nav.registration_state)
                    else:
                        database.set_state(user_id, 'main')
                        database.create_account(user_id, login, password)
                        await bot.send_message(user_id, 'Регистрация прошла успешно', reply_markup=nav.main_state)

            if database.get_state(user_id) == 'main':

                if message.text == 'Проверить срок действия подписки':
                    subscribe_time = database.get_subscribe(user_id)
                    is_subscribe_valid = subscribe_time >= datetime.now()
                    if is_subscribe_valid:
                        text = f'Подписка действительна до: {subscribe_time.strftime("%d.%m.%Y %H:%M:%S")}'
                    else:
                        text = 'Подписка недействительна'
                    await bot.send_message(user_id, text, reply_markup=nav.subscribe_state)
                    database.set_state(user_id, 'subscribe')

                elif message.text == 'Проверить баланс':
                    await bot.send_message(user_id, f'Текущий баланс: {database.get_balance(user_id)} $', reply_markup=nav.balance_state)
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
                    await bot.send_message(user_id, 'Поиск завершен', reply_markup=nav.main_state)

            elif database.get_state(user_id) == 'subscribe':
                if message.text == 'Назад':

                    await bot.send_message(user_id, '...', reply_markup=nav.main_state)
                    database.set_state(user_id, 'main')

                elif message.text == 'Продлить':
                    current_balance = database.get_balance(user_id)
                    await bot.send_message(user_id, f'Выбери желаемую подписку, баланс: {current_balance}$', reply_markup=nav.add_subscribe_state)
                    database.set_state(user_id, 'add_subscribe')

            elif database.get_state(user_id) == 'add_subscribe':
                if message.text == 'Назад':

                    await bot.send_message(user_id, '...', reply_markup=nav.main_state)
                    database.set_state(user_id, 'main')

                elif message.text in price_txt:
                    days, _, price = message.text.split(' ')
                    price = int(price[1:-2])
                    balance = database.get_balance(user_id)
                    if balance < price:
                        await bot.send_message(user_id, 'Для покупки этой подписки недостаточно средств', reply_markup=nav.add_subscribe_state)
                    else:
                        database.set_balance(user_id, balance-price)
                        new_subscribe_time = database.add_subscribe(user_id, int(days))

                        await bot.send_message(user_id, f'Подписка успешно продлена до {new_subscribe_time}, текущий баланс: {balance-price} $', reply_markup=nav.main_state)
                        database.set_state(user_id, 'main')

            elif database.get_state(user_id) == 'balance':
                if message.text == 'Назад':
                    await bot.send_message(user_id, '...', reply_markup=nav.main_state)
                    database.set_state(user_id, 'main')

                elif message.text == 'Пополнить':
                    await bot.send_message(user_id, 'Пока не умею, обратись к славику', reply_markup=nav.main_state)
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
