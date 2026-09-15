import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN
from database.models import init_db
from handlers import subscription, survey, generation, payment


async def main():
    logging.basicConfig(level=logging.INFO)
    await init_db()
    session = AiohttpSession(timeout=60)
    bot = Bot(token=BOT_TOKEN, session=session)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(subscription.router)
    dp.include_router(survey.router)
    dp.include_router(generation.router)
    dp.include_router(payment.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())