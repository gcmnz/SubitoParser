from src.price import price

from aiogram.types import KeyboardButton

registration_button = KeyboardButton(text='Зарегистрироваться')
authorization_button = KeyboardButton(text='Войти')

back = KeyboardButton(text='Назад')

main_start_getting_ads = KeyboardButton(text='Запустить поиск объявлений',)
main_stop_getting_ads = KeyboardButton(text='Остановить поиск объявлений')
main_check_subscribe = KeyboardButton(text='Проверить срок действия подписки')
main_check_balance = KeyboardButton(text='Проверить баланс')

subscribe_add = KeyboardButton(text='Продлить')

add_subscribe_one_day = KeyboardButton(text=f'1 день [{price[1]}$]')
add_subscribe_three_days = KeyboardButton(text=f'3 дня [{price[3]}$]')
add_subscribe_seven_days = KeyboardButton(text=f'7 дней [{price[7]}$]')
add_subscribe_fourteen_days = KeyboardButton(text=f'14 дней [{price[14]}$]')
add_subscribe_thirty_days = KeyboardButton(text=f'30 дней [{price[30]}$]')

balance_add = KeyboardButton(text='Пополнить')
