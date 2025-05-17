from sqlalchemy.orm import Session
from .models import Task
from .setup_db import SessionLocal
from datetime import datetime
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

async def get_client_tasks(telegram_user_id: int):
    db = SessionLocal()
    try:
        return db.query(Task).filter(
            Task.telegram_user_id == telegram_user_id
        ).order_by(Task.created_at.desc()).all()
    except Exception as e:
        logger.error(f"DB error: {e}")
        return []
    finally:
        db.close()

async def cancel_task(task_id: int, by_client: bool = False):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.status = "cancelled_by_client" if by_client else "cancelled_by_admin"
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"DB error: {e}")
        return False
    finally:
        db.close()

async def get_task_by_id(task_id: int):
    db = SessionLocal()
    try:
        return db.query(Task).filter(Task.id == task_id).first()
    except Exception as e:
        logger.error(f"DB error: {e}")
        return None
    finally:
        db.close()

async def update_task_status(task_id: int, new_status: str, admin_comment: str = None):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.status = new_status
        if admin_comment:
            task.admin_comment = admin_comment
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"DB error: {e}")
        return False
    finally:
        db.close()
