from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from config.config import TaskStatus

Base = declarative_base()

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
    telegram_user_id = Column(Integer, nullable=False)
    telegram_username = Column(String(50))
    admin_comment = Column(Text)
    completion_report = Column(Text)
