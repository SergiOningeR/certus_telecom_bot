from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()

class TaskStatus(PyEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED_BY_ADMIN = "cancelled_by_admin"
    CANCELLED_BY_CLIENT = "cancelled_by_client"

class TaskPriority(PyEnum):
    LOW = 1
    MEDIUM_LOW = 2
    MEDIUM = 3
    MEDIUM_HIGH = 4
    HIGH = 5

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    client_phone = Column(String(20), nullable=False)
    priority = Column(Integer, nullable=False)
    image_path = Column(String(255))
    company = Column(String(100), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    telegram_user_id = Column(Integer, nullable=False)
    telegram_username = Column(String(50))
    admin_comment = Column(Text)
    completion_report = Column(Text)

class AdminAction(Base):
    __tablename__ = 'admin_actions'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    admin_id = Column(Integer, nullable=False)
    action_type = Column(String(50), nullable=False)
    action_time = Column(DateTime, default=datetime.utcnow)
    details = Column(Text)
