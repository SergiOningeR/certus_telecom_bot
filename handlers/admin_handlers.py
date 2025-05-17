from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db_operations import (
    get_task_by_id,
    update_task_status,
    get_all_active_tasks,
    get_tasks_by_client,
    get_tasks_by_company
)
from utils.keyboards import admin_task_keyboard, admin_search_keyboard
from config.config import config

class AdminStates(StatesGroup):
    waiting_for_cancel_reason = State()
    waiting_for_completion_report = State()
    waiting_for_search_query = State()

async def send_task_to_admin_group(bot: Bot, task):
    """Отправка задачи в группу администраторов"""
    message_text = (
        f"Новая заявка №{task.id}\n"
        f"Клиент: @{task.telegram_username} ({task.client_phone})\n"
        f"Компания: {task.company}\n"
        f"Название: {task.title}\n"
        f"Описание: {task.description}\n"
        f"Приоритет: {task.priority}/5\n"
        f"Статус: {'Новая' if task.status == 'new' else 'В работе'}"
    )
    
    keyboard = admin_task_keyboard(task.id, task.status)
    
    if task.image_path:
        image_path = config.BASE_DIR / task.image_path
        with open(image_path, 'rb') as photo:
            await bot.send_photo(
                chat_id=config.ADMIN_GROUP_ID,
                photo=photo,
                caption=message_text,
                reply_markup=keyboard,
                message_thread_id=config.ADMIN_GROUP_THREAD_ID
            )
    else:
        await bot.send_message(
            chat_id=config.ADMIN_GROUP_ID,
            text=message_text,
            reply_markup=keyboard,
            message_thread_id=config.ADMIN_GROUP_THREAD_ID
        )

async def process_task_take(callback: types.CallbackQuery):
    """Обработка взятия задачи в работу"""
    task_id = int(callback.data.split('_')[1])
    task = await get_task_by_id(task_id)
    
    if not task:
        await callback.answer("Задача не найдена!")
        return
    
    if task.status != 'new':
        await callback.answer("Эта задача уже в работе!")
        return
    
    await update_task_status(task_id, 'in_progress')
    
    # Обновляем сообщение в группе
    await callback.message.edit_reply_markup(admin_task_keyboard(task_id, 'in_progress'))
    
    # Уведомляем клиента
    await callback.bot.send_message(
        chat_id=task.telegram_user_id,
        text=f"Задача №{task_id} взята в работу. Ожидайте завершения задачи."
    )
    
    await callback.answer("Задача взята в работу!")

async def process_task_cancel(callback: types.CallbackQuery, state: FSMContext):
    """Обработка отмены задачи"""
    task_id = int(callback.data.split('_')[1])
    
    async with state.proxy() as data:
        data['task_id'] = task_id
    
    await AdminStates.waiting_for_cancel_reason.set()
    await callback.message.answer("Укажите причину отмены задачи:")
    await callback.answer()

async def process_cancel_reason(message: types.Message, state: FSMContext):
    """Обработка причины отмены задачи"""
    reason = message.text
    async with state.proxy() as data:
        task_id = data['task_id']
    
    task = await get_task_by_id(task_id)
    if not task:
        await message.answer("Задача не найдена!")
        await state.finish()
        return
    
    await update_task_status(task_id, 'cancelled_by_admin', admin_comment=reason)
    
    # Обновляем сообщение в группе
    await message.bot.edit_message_reply_markup(
        chat_id=config.ADMIN_GROUP_ID,
        message_id=task.admin_message_id,
        reply_markup=None
    )
    
    # Уведомляем клиента
    await message.bot.send_message(
        chat_id=task.telegram_user_id,
        text=f"Задача №{task_id} отменена администратором.\nПричина: {reason}"
    )
    
    await message.answer("Задача отменена!")
    await state.finish()

async def process_task_complete(callback: types.CallbackQuery, state: FSMContext):
    """Обработка завершения задачи"""
    task_id = int(callback.data.split('_')[1])
    
    async with state.proxy() as data:
        data['task_id'] = task_id
    
    await AdminStates.waiting_for_completion_report.set()
    await callback.message.answer("Напишите отчет о выполнении задачи:")
    await callback.answer()

async def process_completion_report(message: types.Message, state: FSMContext):
    """Обработка отчета о выполнении задачи"""
    report = message.text
    async with state.proxy() as data:
        task_id = data['task_id']
    
    task = await get_task_by_id(task_id)
    if not task:
        await message.answer("Задача не найдена!")
        await state.finish()
        return
    
    await update_task_status(task_id, 'completed', completion_report=report)
    
    # Обновляем сообщение в группе
    await message.bot.edit_message_reply_markup(
        chat_id=config.ADMIN_GROUP_ID,
        message_id=task.admin_message_id,
        reply_markup=None
    )
    
    # Уведомляем клиента
    await message.bot.send_message(
        chat_id=task.telegram_user_id,
        text=f"Задача №{task_id} завершена.\nОтчет о выполнении: {report}"
    )
    
    await message.answer("Задача завершена!")
    await state.finish()

async def show_admin_menu(message: types.Message):
    """Показать меню администратора"""
    if str(message.from_user.id) not in config.ADMINS:
        return
    
    await message.answer(
        "Меню администратора:",
        reply_markup=admin_search_keyboard()
    )

async def search_tasks(callback: types.CallbackQuery, state: FSMContext):
    """Поиск задач"""
    search_type = callback.data.split('_')[1]
    
    async with state.proxy() as data:
        data['search_type'] = search_type
    
    await AdminStates.waiting_for_search_query.set()
    await callback.message.answer(f"Введите {'номер телефона' if search_type == 'phone' else 'название компании'} для поиска:")
    await callback.answer()

async def process_search_query(message: types.Message, state: FSMContext):
    """Обработка поискового запроса"""
    query = message.text
    async with state.proxy() as data:
        search_type = data['search_type']
    
    if search_type == 'phone':
        tasks = await get_tasks_by_client(query)
    else:
        tasks = await get_tasks_by_company(query)
    
    if not tasks:
        await message.answer("Задачи не найдены.")
        await state.finish()
        return
    
    for task in tasks:
        status_map = {
            'new': 'Новая',
            'in_progress': 'В работе',
            'completed': 'Завершена',
            'cancelled_by_admin': 'Отменена администратором',
            'cancelled_by_client': 'Отменена клиентом'
        }
        
        message_text = (
            f"Задача №{task.id}\n"
            f"Клиент: @{task.telegram_username} ({task.client_phone})\n"
            f"Компания: {task.company}\n"
            f"Название: {task.title}\n"
            f"Описание: {task.description}\n"
            f"Приоритет: {task.priority}/5\n"
            f"Статус: {status_map[task.status]}\n"
            f"Дата создания: {task.created_at.strftime('%d.%m.%Y %H:%M')}"
        )
        
        await message.answer(message_text)
    
    await state.finish()

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков для администраторов"""
    # Обработчики callback-запросов
    dp.register_callback_query_handler(process_task_take, lambda c: c.data.startswith('take_'))
    dp.register_callback_query_handler(process_task_cancel, lambda c: c.data.startswith('cancel_'))
    dp.register_callback_query_handler(process_task_complete, lambda c: c.data.startswith('complete_'))
    dp.register_callback_query_handler(search_tasks, lambda c: c.data.startswith('search_'))
    
    # Обработчики сообщений
    dp.register_message_handler(show_admin_menu, commands=['admin'], state="*")
    dp.register_message_handler(process_cancel_reason, state=AdminStates.waiting_for_cancel_reason)
    dp.register_message_handler(process_completion_report, state=AdminStates.waiting_for_completion_report)
    dp.register_message_handler(process_search_query, state=AdminStates.waiting_for_search_query)
