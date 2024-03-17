import asyncio

from config import CRYPTO_TOKEN
from src.database.database import AccountDatabase

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiocryptopay import AioCryptoPay, Networks


crypto = AioCryptoPay(token=CRYPTO_TOKEN, network=Networks.MAIN_NET)
database = AccountDatabase()


async def create_invoice(bot, user_id: int, amount: float):
    invoice = await crypto.create_invoice(asset='USDT', amount=amount)

    key_ = InlineKeyboardButton(text='Перейти к оплате', url=invoice.bot_invoice_url)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[key_]])
    await bot.send_message(user_id, "Нажмите на кнопку для оплаты:", reply_markup=keyboard)

    await __check_invoice(bot, user_id, invoice.invoice_id)


async def __check_invoice(bot, user_id: int, invoice_id: int):
    while True:
        invoices = await crypto.get_invoices()
        current_invoice = list(filter(lambda invoice: invoice.invoice_id == invoice_id, invoices))[0]

        if current_invoice.status == 'paid':
            database.add_to_balance(user_id, current_invoice.amount)
            await bot.send_message(user_id, f'Успешно оплачено: {current_invoice.amount} $')
            return

        await asyncio.sleep(5)
