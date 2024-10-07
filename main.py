import os
import logging
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


@app.post("/add-tasks/")
def add_task(data: dict):
    celery_tasks = {}
    for task in data["tasks"]:
        try:
            flyer_id = task[0]
            created_task = celery_app.send_task(
                "tasks.generate_flyer",
                args=[*task],
            )
            celery_tasks[flyer_id] = created_task.id
            logging.info(f"Task sent to Celery: {created_task}")
        except Exception as e:
            celery_tasks[flyer_id] = None
            logging.error(f"Error sending task to Celery: {e}")
    return {"status": "All Task sent to Celery", "tasks": celery_tasks}
