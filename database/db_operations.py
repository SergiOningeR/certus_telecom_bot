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

async def create_task(task_data: dict, db: Session) -> int:
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
