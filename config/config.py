import os
from pathlib import Path
from enum import Enum

class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED_BY_ADMIN = "cancelled_by_admin"
    CANCELLED_BY_CLIENT = "cancelled_by_client"

class Config:
    # Telegram
    BOT_TOKEN = "ВАШ_ТОКЕН"  # Обязательно заменить!
    ADMIN_GROUP_ID = -1001234567890  # ID группы с минусом
    ADMIN_GROUP_THREAD_ID = 123  # ID темы
    
    # Database
    DB_HOST = "localhost"
    DB_USER = "certus_bot"
    DB_PASSWORD = "SecurePass123!"  # Заменить
    DB_NAME = "certus_telecom"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    IMAGES_DIR = BASE_DIR / "images"
    LOG_DIR = BASE_DIR / "logs"
    
    # Zabbix
    ZABBIX_HOST = "192.168.1.100"
    ZABBIX_PORT = 10051
    
    # Admin
    ADMIN_API_KEY = "your-secret-key"  # Заменить
    
    def __init__(self):
        self.IMAGE_STORAGE = "/var/www/certus/images"
        os.makedirs(self.IMAGE_STORAGE, exist_ok=True)
        os.makedirs(self.LOG_DIR, exist_ok=True)

config = Config()
