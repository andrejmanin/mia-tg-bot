import asyncio
import logging
import sys
import json

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import database.requests as rq
from database.models import async_main
from database.requests import get_user, update_user_history
from gpt.gpt_model import create_request

dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    if message.from_user.username:
        await rq.set_user(message.from_user.id, message.from_user.username)
        await message.answer(f"Ahoj {message.from_user.username}!")
        user = await get_user(message.from_user.id)
        if user:
            print(user.tg_id)
        else:
            print("User not found")

@dp.message()
async def answer(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user:
        text = await create_request(message.text, json.loads(user.history))
        await message.answer(text[-1]["content"])
        await update_user_history(message.from_user.id, text)





async def main():
    await async_main()
    bot = Bot(token='bot-token')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is offline')
