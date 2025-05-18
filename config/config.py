from pathlib import Path
from enum import Enum
import os

class TaskStatus(str, Enum):
    """Статусы задач"""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED_BY_ADMIN = "cancelled_by_admin"
    CANCELLED_BY_CLIENT = "cancelled_by_client"

class Config:
    # Telegram Bot Settings
    BOT_TOKEN = "7807656215:AAFwoLQvLNZ1-6ZPv1XVTD33pUXRb5GbPSo"  # Токен от @BotFather
    ADMIN_GROUP_ID = -1002460971966  # ID группы для уведомлений (должен начинаться с -100)
    ADMIN_GROUP_THREAD_ID = 123  # ID темы в группе (если нужно)
    
    # Database Settings
    DB_HOST = "localhost"  # Хост базы данных
    DB_USER = "certus_bot"  # Пользователь БД
    DB_PASSWORD = "SecurePass123!"  # Пароль (заменить на свой)
    DB_NAME = "certus_telecom"  # Название базы данных
    
    # Path Configuration
    BASE_DIR = Path(__file__).parent.parent  # Корневая директория проекта
    IMAGES_DIR = BASE_DIR / "images"  # Папка для хранения изображений
    LOG_DIR = BASE_DIR / "logs"  # Папка для логов
    
    # Task Settings
    MAX_TITLE_LENGTH = 100  # Максимальная длина названия задачи
    MAX_DESCRIPTION_LENGTH = 2000  # Максимальная длина описания
    MAX_COMPANY_LENGTH = 100  # Максимальная длина названия компании
    
    # Image Settings
    MAX_IMAGE_SIZE_MB = 5  # Максимальный размер изображения (в МБ)
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png']  # Разрешенные типы изображений
    
    def __init__(self):
        """Создает необходимые директории при инициализации"""
        os.makedirs(self.IMAGES_DIR, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)
        
        # Валидация критических настроек
        assert self.BOT_TOKEN and self.BOT_TOKEN.startswith(''), "Неверный формат BOT_TOKEN"
        assert self.ADMIN_GROUP_ID and str(self.ADMIN_GROUP_ID).startswith('-100'), "ADMIN_GROUP_ID должен начинаться с -100"

# Экземпляр конфигурации
config = Config()
