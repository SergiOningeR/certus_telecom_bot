from fastapi import FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from database.models import Task
from database.setup_db import SessionLocal
from config.config import config

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key")

@app.get("/tasks/")
async def get_tasks(api_key: str = Depends(api_key_header)):
    if api_key != config.ADMIN_API_KEY:
        raise HTTPException(status_code=403)
    db = SessionLocal()
    tasks = db.query(Task).all()
    return tasks
