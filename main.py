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


@app.post("/add-task/")
def add_task(data: dict):
    # Send task to Celery
    # ID	Suburb	Address	Lot	Price	Rego	Facade	FloorPlan	Facade File	Floorplan File	Bedroom	Bathroom	Parking Slot
    flyer_id = data["flyer_id"]
    suburb = data["suburb"]
    address = data["address"]
    lot = data["lot"]
    price = data["price"]
    rego = data["rego"]
    facade = data["facade"]
    floorplan = data["floorplan"]
    facade_file = data["facade_file"]
    floorplan_file = data["floorplan_file"]
    bedroom = data["bedroom"]
    bathroom = data["bathroom"]
    parking_slot = data["parking_slot"]

    task = celery_app.send_task(
        "tasks.generate_flyer",
        args=[
            flyer_id,
            suburb,
            address,
            lot,
            price,
            rego,
            facade,
            floorplan,
            facade_file,
            floorplan_file,
            bedroom,
            bathroom,
            parking_slot,
        ],
    )
    logging.info(f"Task sent to Celery: {data}")
    return {"status": "Task sent to Celery", "task_id": task.id}
