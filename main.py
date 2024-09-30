import os
from dotenv import load_dotenv

load_dotenv(".env.local")

from fastapi import FastAPI
from celery import Celery

# Get Redis URL from environment or use default
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize FastAPI app
app = FastAPI()

# Initialize Celery app
celery_app = Celery("tasks", broker=redis_url)


@app.post("/add-task/")
def add_task(data: dict):
    # Send task to Celery
    task = celery_app.send_task("tasks.generate_report", args=[data["task_data"]])
    return {"status": "Task sent to Celery", "task_id": task.id}
