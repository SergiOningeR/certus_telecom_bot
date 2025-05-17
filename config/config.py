import os
from pathlib import Path

# Базовые настройки
class Config:
    # Настройки бота
    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    ADMIN_GROUP_ID = -1001234567890  # ID группы администраторов
    ADMIN_GROUP_THREAD_ID = 123      # ID темы в группе для заявок
    
    # Настройки базы данных
    DB_HOST = "localhost"
    DB_USER = "certus_bot"
    DB_PASSWORD = "secure_password"
    DB_NAME = "certus_telecom"
    
    # Пути к файлам
    BASE_DIR = Path(__file__).parent.parent
    IMAGES_DIR = BASE_DIR / "images"
    
    # Создаем папку для изображений, если ее нет
    if not IMAGES_DIR.exists():
        IMAGES_DIR.mkdir()

# Настройки для разработки
class DevelopmentConfig(Config):
    DEBUG = True

# Настройки для производства
class ProductionConfig(Config):
    DEBUG = False

# Выбираем конфигурацию в зависимости от окружения
if os.getenv('ENVIRONMENT') == 'production':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

# Логирование
    LOG_DIR = BASE_DIR / "logs"
    LOG_FILE = LOG_DIR / "bot.log"
    
    # Создаем папку для логов, если ее нет
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()
