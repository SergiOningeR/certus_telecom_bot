from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from database.db_operations import get_db, get_all_tasks, search_tasks
from database.models import TaskStatus
from config.config import config
import uvicorn

app = FastAPI(title="Certus Telecom Admin Panel")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтирование статики для изображений
app.mount("/images", StaticFiles(directory=config.IMAGES_DIR), name="images")

# Аутентификация
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != config.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# Модели
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    client_phone: str
    priority: int
    company: str
    status: str
    created_at: datetime
    updated_at: datetime
    image_url: Optional[str]
    admin_comment: Optional[str]
    completion_report: Optional[str]

# Роуты
@app.get("/tasks/", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    limit: int = 100,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Получить список всех задач с фильтрацией по статусу"""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    tasks = query.order_by(Task.created_at.desc()).limit(limit).all()
    return [format_task_response(task) for task in tasks]

@app.get("/tasks/search/", response_model=List[TaskResponse])
async def search_tasks_endpoint(
    query: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Поиск задач по компании или номеру телефона"""
    tasks = search_tasks(db, query)
    return [format_task_response(task) for task in tasks]

def format_task_response(task: Task) -> TaskResponse:
    """Форматирование задачи для ответа API"""
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        client_phone=task.client_phone,
        priority=task.priority,
        company=task.company,
        status=task.status.value,
        created_at=task.created_at,
        updated_at=task.updated_at,
        image_url=f"/images/{task.image_path.split('/')[-1]}" if task.image_path else None,
        admin_comment=task.admin_comment,
        completion_report=task.completion_report
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
