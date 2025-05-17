from config.config import config
from pathlib import Path
from typing import Optional
import re

def validate_phone(phone: str) -> bool:
    """Валидация номера телефона"""
    pattern = r'^\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}$'
    return re.match(pattern, phone) is not None

def format_phone(phone: str) -> str:
    """Форматирование телефона в единый формат"""
    digits = re.sub(r'\D', '', phone)
    return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

def save_image(file_id: str, bot) -> Optional[str]:
    """Сохранение изображения на диск"""
    try:
        file = await bot.get_file(file_id)
        file_path = file.file_path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = config.IMAGES_DIR / f"task_{timestamp}_{file_id}.jpg"
        await bot.download_file(file_path, str(save_path))
        return str(save_path.relative_to(config.BASE_DIR))
    except Exception as e:
        print(f"Error saving image: {e}")
        return None
