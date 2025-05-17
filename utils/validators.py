import re

def validate_phone(phone: str) -> bool:
    """Проверка формата телефона"""
    pattern = r'^\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}$'
    return re.match(pattern, phone) is not None

def validate_email(email: str) -> bool:
    """Проверка формата email (на будущее)"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
