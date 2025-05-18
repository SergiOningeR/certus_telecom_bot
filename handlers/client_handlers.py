from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType, ReplyKeyboardRemove
from database.db_operations import create_task, get_client_tasks, cancel_task
from utils.keyboards import client_main_menu, priority_keyboard, cancel_keyboard
from utils.validators import validate_phone
from config.config import config, TaskStatus
import logging

logger = logging.getLogger(__name__)

class ClientStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_phone = State()
    waiting_for_priority = State()
    waiting_for_image = State()
    waiting_for_company = State()

async def start_client(message: types.Message):
    await message.answer(
        "Приветствуем в Certus Telecom!\n"
        "Для создания заявки нажмите кнопку ниже.",
        reply_markup=client_main_menu()
    )

async def show_my_tasks(message: types.Message):
    tasks = await get_client_tasks(message.from_user.id)
    if not tasks:
        await message.answer("У вас нет активных заявок.")
        return
    
    for task in tasks:
        status = {
            TaskStatus.NEW: "🆕 Новая",
            TaskStatus.IN_PROGRESS: "🛠 В работе",
            TaskStatus.COMPLETED: "✅ Завершена",
            TaskStatus.CANCELLED: "❌ Отменена"
        }[task.status]
        
        text = (
            f"🔹 Заявка #{task.id}\n"
            f"📌 {task.title}\n"
            f"📝 {task.description}\n"
            f"📞 {task.client_phone}\n"
            f"🏢 {task.company}\n"
            f"🔢 Приоритет: {task.priority}/5\n"
            f"🔄 {status}"
        )
        await message.answer(text, reply_markup=cancel_keyboard(task.id))

# ... (полные обработчики для каждого состояния FSM) ...

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_client, commands=['start'])
    dp.register_message_handler(show_my_tasks, text="Мои заявки")
    # ... (регистрация всех обработчиков) ...
