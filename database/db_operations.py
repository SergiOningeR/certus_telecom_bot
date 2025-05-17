from sqlalchemy.orm import Session
from .models import Task, AdminAction
from .setup_db import SessionLocal
from datetime import datetime
from typing import Optional

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_task(task_data: dict) -> int:
    """Создание новой задачи в БД"""
    db = SessionLocal()
    try:
        task = Task(
            title=task_data['title'],
            description=task_data['description'],
            client_phone=task_data['phone'],
            priority=task_data['priority'],
            image_path=task_data.get('image_path'),
            company=task_data['company'],
            telegram_user_id=task_data['telegram_user_id'],
            telegram_username=task_data.get('telegram_username')
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id
    finally:
        db.close()

async def get_task_by_id(task_id: int) -> Optional[Task]:
    """Получение задачи по ID"""
    db = SessionLocal()
    try:
        return db.query(Task).filter(Task.id == task_id).first()
    finally:
        db.close()

async def update_task_status(
    task_id: int,
    new_status: str,
    admin_comment: str = None,
    completion_report: str = None
) -> bool:
    """Обновление статуса задачи"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.status = new_status
        if admin_comment:
            task.admin_comment = admin_comment
        if completion_report:
            task.completion_report = completion_report
        
        db.commit()
        return True
    finally:
        db.close()

async def get_client_tasks(telegram_user_id: int) -> list[Task]:
    """Получение всех задач клиента"""
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            Task.telegram_user_id == telegram_user_id
        ).order_by(Task.created_at.desc()).all()
    finally:
        db.close()

async def get_all_active_tasks() -> list[Task]:
    """Получение всех активных задач"""
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            Task.status.in_(['new', 'in_progress'])
        ).order_by(Task.priority.desc(), Task.created_at).all()
    finally:
        db.close()

async def get_tasks_by_client(phone: str) -> list[Task]:
    """Поиск задач по номеру телефона клиента"""
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            Task.client_phone.like(f"%{phone}%")
        ).order_by(Task.created_at.desc()).all()
    finally:
        db.close()

async def get_tasks_by_company(company: str) -> list[Task]:
    """Поиск задач по названию компании"""
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            Task.company.like(f"%{company}%")
        ).order_by(Task.created_at.desc()).all()
    finally:
        db.close()

async def cancel_task(task_id: int, by_client: bool = False) -> bool:
    """Отмена задачи"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.status = 'cancelled_by_client' if by_client else 'cancelled_by_admin'
        db.commit()
        return True
    finally:
        db.close()
