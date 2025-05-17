from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from database.models import Task
from database.setup_db import SessionLocal
from config.config import config

app = FastAPI(title="Certus Admin Panel")
api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/tasks/")
async def get_task_image(task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task.image_path:
        raise HTTPException(404)
    return FileResponse(Path(config.IMAGE_STORAGE) / task.image_path)

async def get_tasks(api_key: str = Depends(api_key_header)):
    if api_key != config.ADMIN_API_KEY:
        raise HTTPException(status_code=403)
    
    db = SessionLocal()
    try:
        tasks = db.query(Task).limit(100).all()
        return tasks
    finally:
        db.close()
