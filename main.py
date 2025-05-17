import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config.config import config
from handlers import client_handlers, admin_handlers, common_handlers
from database.setup_db import init_db
from monitoring.zabbix_integration import ZabbixMonitor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def setup_bot():
    init_db()
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    
    # Мониторинг
    monitor = ZabbixMonitor()
    dp.middleware.setup(LoggingMiddleware())
    
    # Регистрация обработчиков
    client_handlers.register_handlers(dp)
    admin_handlers.register_handlers(dp)
    common_handlers.register_handlers(dp)
    
    # Обработка ошибок
    async def on_error(update: types.Update, exc: Exception):
        logger.error(f"Update {update} caused error: {exc}")
        await monitor.send_metric("bot.error", str(exc))
        return True
    
    dp.register_errors_handler(on_error)
    return dp

async def main():
    dp = await setup_bot()
    try:
        logger.info("Starting bot...")
        await dp.start_polling()
    finally:
        await dp.storage.close()
        logger.info("Bot stopped")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
