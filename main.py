from aiogram import Bot, Dispatcher

import asyncio

import config
import database
import handlers
import misc


async def start_bot():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    await database.create_tables()
    dp.startup.register(misc.on_start)
    dp.shutdown.register(misc.on_shutdown)
    dp.include_router(handlers.main_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
