from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import List, Optional
from .models import Task
from .setup_db import SessionLocal
from config.config import config, TaskStatus
import logging

logger = logging.getLogger(__name__)

def get_db() -> Session:
    """Генератор сессий БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_task(task_data: dict) -> int:
    """
    Создание новой задачи
    :param task_data: Данные задачи (dict)
    :return: ID созданной задачи (int)
    """
    db = SessionLocal()
    try:
        task = Task(
            title=task_data['title'],
            description=task_data['description'],
            client_phone=task_data['client_phone'],
            priority=task_data['priority'],
            image_path=task_data.get('image_path'),
            company=task_data['company'],
            telegram_user_id=task_data['telegram_user_id'],
            telegram_username=task_data.get('telegram_username'),
            status=TaskStatus.NEW
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка создания задачи: {e}")
        raise
    finally:
        db.close()

async def get_task_by_id(task_id: int) -> Optional[Task]:
    """
    Получение задачи по ID
    :param task_id: ID задачи (int)
    :return: Объект Task или None
    """
    db = SessionLocal()
    try:
        return db.query(Task).filter(Task.id == task_id).first()
    except Exception as e:
        logger.error(f"Ошибка получения задачи #{task_id}: {e}")
        return None
    finally:
        db.close()

async def get_client_tasks(telegram_user_id: int) -> List[Task]:
    """
    Получение всех задач клиента
    :param telegram_user_id: ID пользователя в Telegram (int)
    :return: Список задач (List[Task])
    """
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            Task.telegram_user_id == telegram_user_id
        ).order_by(Task.created_at.desc()).all()
    except Exception as e:
        logger.error(f"Ошибка получения задач пользователя {telegram_user_id}: {e}")
        return []
    finally:
        db.close()

async def get_all_active_tasks() -> List[Task]:
    """
    Получение всех активных задач (новых и в работе)
    :return: Список задач (List[Task])
    """
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            or_(
                Task.status == TaskStatus.NEW,
                Task.status == TaskStatus.IN_PROGRESS
            )
        ).order_by(
            Task.priority.desc(),
            Task.created_at.asc()
        ).all()
    except Exception as e:
        logger.error(f"Ошибка получения активных задач: {e}")
        return []
    finally:
        db.close()

async def update_task_status(
    task_id: int,
    new_status: TaskStatus,
    admin_comment: str = None,
    completion_report: str = None
) -> bool:
    """
    Обновление статуса задачи
    :param task_id: ID задачи (int)
    :param new_status: Новый статус (TaskStatus)
    :param admin_comment: Комментарий администратора (str, optional)
    :param completion_report: Отчет о выполнении (str, optional)
    :return: Успешность операции (bool)
    """
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            logger.warning(f"Задача #{task_id} не найдена")
            return False

        task.status = new_status
        task.updated_at = datetime.utcnow()

        if admin_comment:
            task.admin_comment = admin_comment
        if completion_report:
            task.completion_report = completion_report

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка обновления задачи #{task_id}: {e}")
        return False
    finally:
        db.close()

async def cancel_task(task_id: int, by_client: bool = False) -> bool:
    """
    Отмена задачи
    :param task_id: ID задачи (int)
    :param by_client: Отмена клиентом? (bool)
    :return: Успешность операции (bool)
    """
    status = TaskStatus.CANCELLED_BY_CLIENT if by_client else TaskStatus.CANCELLED_BY_ADMIN
    return await update_task_status(task_id, status)

async def complete_task(task_id: int, report: str) -> bool:
    """
    Завершение задачи
    :param task_id: ID задачи (int)
    :param report: Отчет о выполнении (str)
    :return: Успешность операции (bool)
    """
    return await update_task_status(
        task_id=task_id,
        new_status=TaskStatus.COMPLETED,
        completion_report=report
    )

async def search_tasks(
    phone: str = None,
    company: str = None,
    status: TaskStatus = None
) -> List[Task]:
    """
    Поиск задач по параметрам
    :param phone: Номер телефона (str, optional)
    :param company: Название компании (str, optional)
    :param status: Статус задачи (TaskStatus, optional)
    :return: Список задач (List[Task])
    """
    db = SessionLocal()
    try:
        query = db.query(Task)
        
        filters = []
        if phone:
            filters.append(Task.client_phone.like(f"%{phone}%"))
        if company:
            filters.append(Task.company.ilike(f"%{company}%"))
        if status:
            filters.append(Task.status == status)
        
        if filters:
            query = query.filter(and_(*filters))
            
        return query.order_by(Task.created_at.desc()).all()
    except Exception as e:
        logger.error(f"Ошибка поиска задач: {e}")
        return []
    finally:
        db.close()

async def delete_task(task_id: int) -> bool:
    """
    Удаление задачи (только для админов)
    :param task_id: ID задачи (int)
    :return: Успешность операции (bool)
    """
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
            
        db.delete(task)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка удаления задачи #{task_id}: {e}")
        return False
    finally:
        db.close()
