import re

def validate_phone(phone: str) -> bool:
    """Проверка формата телефона"""
    pattern = r'^\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}$'
    return re.match(pattern, phone) is not None

def validate_email(email: str) -> bool:
    """Проверка формата email (на будущее)"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def validate_company_name(name: str) -> bool:
    """Проверка названия компании"""
    return 2 <= len(name) <= 100 and all(c.isalnum() or c in ' -_' for c in name)

def validate_task_title(title: str) -> bool:
    """Проверка заголовка задачи"""
    return 5 <= len(title) <= 100
