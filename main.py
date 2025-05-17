import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

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
    """Инициализация бота и диспетчера"""
    # Инициализация базы данных
    init_db()
    
    # Создание экземпляров бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    
    # Настройка middleware
    dp.middleware.setup(LoggingMiddleware())
    
    # Регистрация обработчиков
    common_handlers.register_handlers(dp)
    client_handlers.register_handlers(dp)
    admin_handlers.register_handlers(dp)
    
    # Обработка ошибок
    async def on_error(update: types.Update, exception: Exception):
        logger.error(f"Update {update} caused error {exception}")
        return True
    
    dp.register_errors_handler(on_error)
    
    return dp

async def main():
    """Основная функция запуска бота"""
    dp = await setup_bot()
    
    try:
        logger.info("Starting bot...")
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        logger.info("Bot stopped")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}")