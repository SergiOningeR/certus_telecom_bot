import os
from pathlib import Path

class Config:
    # Telegram
    BOT_TOKEN = "7807656215:AAFwoLQvLNZ1-6ZPv1XVTD33pUXRb5GbPSo"  # Заменить у @BotFather
    ADMIN_GROUP_ID =  -1002460971966  # ID группы с минусом
    ADMIN_GROUP_THREAD_ID = 1      # ID темы
    
    # Database
    DB_HOST = "localhost"
    DB_USER = "certus_bot"
    DB_PASSWORD = "PassWord#@!!"  # Заменить
    DB_NAME = "certus_telecom"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    IMAGES_DIR = BASE_DIR / "images"
    LOG_DIR = BASE_DIR / "logs"
    
    # Create dirs
    if not IMAGES_DIR.exists():
        IMAGES_DIR.mkdir()
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()

config = Config()
