from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from pathlib import Path
from database.models import Task
from database.setup_db import SessionLocal
from config.config import config, TaskStatus
from typing import List
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Certus Admin Panel")
api_key_header = APIKeyHeader(name="X-API-Key")

# ... (полная реализация всех endpoints) ...

@app.post("/tasks/{task_id}/complete")
async def complete_task(
    task_id: int,
    report: str,
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    api_key: str = Depends(api_key_header)
):
    if api_key != config.ADMIN_API_KEY:
        raise HTTPException(status_code=403)
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404)
    
    task.status = TaskStatus.COMPLETED
    task.completion_report = report
    
    if image:
        file_path = Path(config.IMAGE_STORAGE) / f"complete_{task_id}.jpg"
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        task.completion_image = str(file_path)
    
    db.commit()
    return {"status": "completed"}
