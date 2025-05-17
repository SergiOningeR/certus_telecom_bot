from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db_operations import create_task, get_client_tasks, cancel_task
from utils.keyboards import client_main_menu, priority_keyboard
from utils.validators import validate_phone
from config.config import config
import os
from datetime import datetime

class ClientStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_phone = State()
    waiting_for_priority = State()
    waiting_for_image = State()
    waiting_for_company = State()

async def start_client(message: types.Message):
    """Обработчик команды /start для клиентов"""
    await message.answer(
        "Приветствуем в компании Certus Telecom!\n"
        "Для создания технических заявок нажмите кнопку 'Создать заявку'.",
        reply_markup=client_main_menu()
    )

async def create_new_task(message: types.Message):
    """Начало создания новой заявки"""
    await ClientStates.waiting_for_title.set()
    await message.answer("Введите название задачи:")

async def process_task_title(message: types.Message, state: FSMContext):
    """Обработка названия задачи"""
    async with state.proxy() as data:
        data['title'] = message.text
    
    await ClientStates.next()
    await message.answer("Введите подробное описание задачи:")

async def process_task_description(message: types.Message, state: FSMContext):
    """Обработка описания задачи"""
    async with state.proxy() as data:
        data['description'] = message.text
    
    await ClientStates.next()
    await message.answer("Введите ваш контактный телефон в формате +7 (XXX) XXX-XX-XX:")

async def process_task_phone(message: types.Message, state: FSMContext):
    """Обработка телефона клиента"""
    phone = message.text
    
    if not validate_phone(phone):
        await message.answer("Некорректный формат телефона. Пожалуйста, введите телефон в формате +7 (XXX) XXX-XX-XX:")
        return
    
    async with state.proxy() as data:
        data['phone'] = phone
    
    await ClientStates.next()
    await message.answer("Выберите важность задачи:", reply_markup=priority_keyboard())

async def process_task_priority(callback: types.CallbackQuery, state: FSMContext):
    """Обработка важности задачи"""
    priority = int(callback.data.split('_')[1])
    
    async with state.proxy() as data:
        data['priority'] = priority
    
    await ClientStates.next()
    await callback.message.answer("Прикрепите изображение (если необходимо) или нажмите 'Пропустить':")
    await callback.answer()

async def skip_image(message: types.Message, state: FSMContext):
    """Пропуск прикрепления изображения"""
    async with state.proxy() as data:
        data['image_path'] = None
    
    await ClientStates.next()
    await message.answer("Введите название вашей компании:")

async def process_task_image(message: types.Message, state: FSMContext):
    """Обработка прикрепленного изображения"""
    if not message.photo:
        await message.answer("Пожалуйста, прикрепите изображение или нажмите 'Пропустить'")
        return
    
    photo = message.photo[-1]
    file_id = photo.file_id
    
    # Сохраняем изображение
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = config.IMAGES_DIR / f"task_{timestamp}_{file_id}.jpg"
    
    await message.bot.download_file(file_path, str(save_path))
    
    async with state.proxy() as data:
        data['image_path'] = str(save_path.relative_to(config.BASE_DIR))
    
    await ClientStates.next()
    await message.answer("Введите название вашей компании:")

async def process_task_company(message: types.Message, state: FSMContext):
    """Обработка названия компании"""
    async with state.proxy() as data:
        data['company'] = message.text
        data['telegram_user_id'] = message.from_user.id
        data['telegram_username'] = message.from_user.username
        
        # Сохраняем задачу в базу данных
        task_id = await create_task(data)
        
        # Отправляем уведомление клиенту
        await message.answer(
            f"Задача №{task_id} успешно создана и передана сотрудникам компании. Ожидайте обратную связь.",
            reply_markup=client_main_menu()
        )
        
        # TODO: Отправить уведомление в группу администраторов
    
    await state.finish()

async def show_client_tasks(message: types.Message):
    """Показать все задачи клиента"""
    tasks = await get_client_tasks(message.from_user.id)
    
    if not tasks:
        await message.answer("У вас нет активных заявок.")
        return
    
    for task in tasks:
        status_map = {
            'new': 'Новая',
            'in_progress': 'В работе',
            'completed': 'Завершена',
            'cancelled_by_admin': 'Отменена администратором',
            'cancelled_by_client': 'Отменена вами'
        }
        
        message_text = (
            f"Задача №{task.id}\n"
            f"Название: {task.title}\n"
            f"Описание: {task.description}\n"
            f"Компания: {task.company}\n"
            f"Статус: {status_map[task.status]}\n"
            f"Приоритет: {task.priority}/5\n"
            f"Дата создания: {task.created_at.strftime('%d.%m.%Y %H:%M')}"
        )
        
        if task.status == 'cancelled_by_admin' and task.admin_comment:
            message_text += f"\nКомментарий администратора: {task.admin_comment}"
        elif task.status == 'completed' and task.completion_report:
            message_text += f"\nОтчет о выполнении: {task.completion_report}"
        
        await message.answer(message_text)

async def cancel_client_task(message: types.Message):
    """Отмена задачи клиентом"""
    # TODO: Реализовать выбор задачи для отмены
    pass

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков для клиентов"""
    dp.register_message_handler(start_client, commands=['start'], state="*")
    dp.register_message_handler(create_new_task, text="Создать заявку", state="*")
    dp.register_message_handler(show_client_tasks, text="Мои заявки", state="*")
    dp.register_message_handler(cancel_client_task, text="Отменить заявку", state="*")
    
    # Обработчики состояний
    dp.register_message_handler(process_task_title, state=ClientStates.waiting_for_title)
    dp.register_message_handler(process_task_description, state=ClientStates.waiting_for_description)
    dp.register_message_handler(process_task_phone, state=ClientStates.waiting_for_phone)
    dp.register_callback_query_handler(process_task_priority, lambda c: c.data.startswith('priority_'), state=ClientStates.waiting_for_priority)
    dp.register_message_handler(skip_image, text="Пропустить", state=ClientStates.waiting_for_image)
    dp.register_message_handler(process_task_image, content_types=types.ContentType.PHOTO, state=ClientStates.waiting_for_image)
    dp.register_message_handler(process_task_company, state=ClientStates.waiting_for_company)
