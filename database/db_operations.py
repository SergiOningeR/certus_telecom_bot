from sqlalchemy.orm import Session
from .models import Task
from .setup_db import SessionLocal
from config.config import config
import logging

logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def create_task(task_data: dict):
    db = SessionLocal()
    try:
        task = Task(**task_data)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id
    except Exception as e:
        db.rollback()
        logger.error(f"DB error: {e}")
        raise
    finally:
        db.close()

async def get_client_tasks(user_id: int):
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            Task.telegram_user_id == user_id
        ).order_by(Task.created_at.desc()).all()
    except Exception as e:
        logger.error(f"DB error: {e}")
        return []
    finally:
        db.close()

async def update_task_status(task_id: int, new_status: str, comment: str = None):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.status = new_status
        if comment:
            if new_status == "completed":
                task.completion_report = comment
            else:
                task.admin_comment = comment
                
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"DB error: {e}")
        return False
    finally:
        db.close()
