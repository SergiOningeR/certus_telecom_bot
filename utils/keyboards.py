from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def client_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать заявку")],
            [KeyboardButton(text="Мои заявки")],
            [KeyboardButton(text="Отменить заявку")]
        ],
        resize_keyboard=True
    )

def priority_keyboard():
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton("1", callback_data="priority_1"),
        InlineKeyboardButton("2", callback_data="priority_2"),
        InlineKeyboardButton("3", callback_data="priority_3"),
        InlineKeyboardButton("4", callback_data="priority_4"),
        InlineKeyboardButton("5", callback_data="priority_5")
    )

def admin_task_keyboard(task_id: int):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton("Принять", callback_data=f"accept_{task_id}"),
        InlineKeyboardButton("Отменить", callback_data=f"cancel_{task_id}"),
        InlineKeyboardButton("Завершить", callback_data=f"complete_{task_id}")
    )
