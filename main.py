import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import routers

from config import BOT_TOKEN

from utils.database import Base, engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# from utils.database import engine, Base
# async def recreate_tables():
#   async with engine.begin() as conn:
#       await conn.run_sync(Base.metadata.drop_all)
#       await conn.run_sync(Base.metadata.create_all)
#   print("✅ Таблицы пересозданы с обновленной структурой!")


async def main():
    try:
        await create_tables()
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        dp = Dispatcher(storage=MemoryStorage())

        for router in routers:
            dp.include_router(router)

        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)

    except Exception as e:
        print(f'Ошибка при запуске бота: {e}')

    finally:
        await bot.session.close() if 'bot' in locals() else None

if __name__ == '__main__':
    asyncio.run(main())