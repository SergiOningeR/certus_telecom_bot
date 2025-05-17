from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from database.db_operations import create_task, get_client_tasks, cancel_task
from utils.keyboards import client_main_menu, priority_keyboard
from utils.validators import validate_phone
from config.config import config, TaskStatus
import logging
from datetime import datetime

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
        "Приветствуем в компании Certus Telecom!\n"
        "Для создания заявки нажмите кнопку ниже.",
        reply_markup=client_main_menu()
    )

async def create_new_task(message: types.Message):
    await ClientStates.waiting_for_title.set()
    await message.answer("Введите название задачи:", reply_markup=types.ReplyKeyboardRemove())

async def process_task_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await ClientStates.next()
    await message.answer("Опишите проблему подробно:")

# ... (все остальные шаги FSM) ...

async def process_task_company(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company'] = message.text
        data['telegram_user_id'] = message.from_user.id
        data['telegram_username'] = message.from_user.username
        
        try:
            task_id = await create_task(data)
            await message.answer(
                f"✅ Задача #{task_id} создана!\n"
                "Скоро с вами свяжутся.",
                reply_markup=client_main_menu()
            )
            
            # Отправка уведомления в группу
            await notify_admins(message.bot, data, task_id)
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            await message.answer("Ошибка при создании заявки!")
    
    await state.finish()

async def notify_admins(bot: Bot, task_data: dict, task_id: int):
    text = (
        f"🆕 Новая заявка #{task_id}\n"
        f"🔹 Клиент: @{task_data['telegram_username']}\n"
        f"📞 Телефон: {task_data['client_phone']}\n"
        f"🏢 Компания: {task_data['company']}\n"
        f"❗ Приоритет: {task_data['priority']}/5"
    )
    
    try:
        if task_data.get('image_path'):
            with open(task_data['image_path'], 'rb') as photo:
                msg = await bot.send_photo(
                    chat_id=config.ADMIN_GROUP_ID,
                    photo=photo,
                    caption=text,
                    message_thread_id=config.ADMIN_GROUP_THREAD_ID
                )
        else:
            msg = await bot.send_message(
                chat_id=config.ADMIN_GROUP_ID,
                text=text,
                message_thread_id=config.ADMIN_GROUP_THREAD_ID
            )
        
        # Сохраняем ID сообщения в БД
        async with get_db() as db:
            db.query(Task).filter(Task.id == task_id).update({'admin_message_id': msg.message_id})
            db.commit()
            
    except Exception as e:
        logger.error(f"Error notifying admins: {e}")
