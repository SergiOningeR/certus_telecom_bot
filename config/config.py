from pathlib import Path
from enum import Enum

class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Config:
    # Telegram
    BOT_TOKEN = "7807656215:AAFwoLQvLNZ1-6ZPv1XVTD33pUXRb5GbPSo"
    ADMIN_GROUP_ID = -1002460971966
    
    # Database
    DB_HOST = "localhost"
    DB_USER = "certus_bot"
    DB_PASSWORD = "SecurePass123!"
    DB_NAME = "certus_telecom"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    IMAGES_DIR = BASE_DIR / "images"
    
    def __init__(self):
        self.IMAGES_DIR.mkdir(exist_ok=True)

config = Config()
