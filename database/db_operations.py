from sqlalchemy.orm import Session
from .models import Task
from .setup_db import SessionLocal

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
        return task.id
    finally:
        db.close()
