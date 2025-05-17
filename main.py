import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config.config import config
from handlers import client_handlers, admin_handlers, common_handlers
from database.setup_db import init_db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def setup_bot():
dp.middleware.setup(LoggingMiddleware())
    
    # Обработка ошибок
    async def on_error(update: types.Update, exception: Exception):
    logger.error(f"Update {update} caused error {exception}")
    return True
    
    dp.register_errors_handler(on_error)

    # Инициализация бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(LoggingMiddleware())
    # Инициализация базы данных
    init_db()
    
    # Регистрация обработчиков
    common_handlers.register_handlers(dp)
    client_handlers.register_handlers(dp)
    admin_handlers.register_handlers(dp)
    
    return dp

async def main():
    dp = await setup_bot()
    
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await dp.bot.get_session()
        await session.close()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
