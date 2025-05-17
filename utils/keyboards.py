from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def client_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню для клиентов"""
    buttons = [
        [KeyboardButton(text="Создать заявку")],
        [KeyboardButton(text="Мои заявки"), KeyboardButton(text="Отменить заявку")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def priority_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора приоритета"""
    buttons = [
        [InlineKeyboardButton(text="1 - Низкий", callback_data="priority_1")],
        [InlineKeyboardButton(text="2 - Средний низкий", callback_data="priority_2")],
        [InlineKeyboardButton(text="3 - Средний", callback_data="priority_3")],
        [InlineKeyboardButton(text="4 - Средний высокий", callback_data="priority_4")],
        [InlineKeyboardButton(text="5 - Высокий", callback_data="priority_5")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_task_keyboard(task_id: int, status: str) -> InlineKeyboardMarkup:
    """Клавиатура действий администратора для задачи"""
    buttons = []
    
    if status == 'new':
        buttons.append([InlineKeyboardButton(
            text="Взять в работу", 
            callback_data=f"take_{task_id}"
        )])
    elif status == 'in_progress':
        buttons.append([InlineKeyboardButton(
            text="Завершить задачу", 
            callback_data=f"complete_{task_id}"
        )])
    
    buttons.append([InlineKeyboardButton(
        text="Отменить задачу", 
        callback_data=f"cancel_{task_id}"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def admin_search_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура поиска для администраторов"""
    buttons = [
        [InlineKeyboardButton(
            text="Поиск по номеру телефона", 
            callback_data="search_phone"
        )],
        [InlineKeyboardButton(
            text="Поиск по компании", 
            callback_data="search_company"
        )],
        [InlineKeyboardButton(
            text="Все активные заявки", 
            callback_data="search_active"
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
