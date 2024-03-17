from .buttons import *

from aiogram.types import ReplyKeyboardMarkup


main_state = ReplyKeyboardMarkup(keyboard=[[main_start_getting_ads,
                                            main_stop_getting_ads],
                                           [main_check_subscribe,
                                            main_check_balance
                                            ]], resize_keyboard=True)
subscribe_state = ReplyKeyboardMarkup(keyboard=[[subscribe_add, back]], resize_keyboard=True)
add_subscribe_state = ReplyKeyboardMarkup(keyboard=[[add_subscribe_one_day, add_subscribe_three_days],
                                                    [add_subscribe_seven_days, add_subscribe_fourteen_days],
                                                    [add_subscribe_thirty_days, back]], resize_keyboard=True)

balance_state = ReplyKeyboardMarkup(keyboard=[[balance_add, back]], resize_keyboard=True)
add_balance_state = ReplyKeyboardMarkup(keyboard=[[back]], resize_keyboard=True)
