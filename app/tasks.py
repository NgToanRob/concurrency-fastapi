import asyncio
from celery import Celery
import time

app = Celery(
    'tasks',
    broker='pyamqp://user:password@rabbitmq//',
    backend='redis://redis:6379/0',
)


@app.task
def long_task(task_id: str):
    print(f"Starting task with ID: {task_id}")
    time.sleep(10)
    print(f"Completed task with ID: {task_id}")
    return f"Task {task_id} completed after 5 seconds"
