from fastapi import FastAPI
from pydantic import BaseModel
from tasks import long_task

app = FastAPI()

class TaskRequest(BaseModel):
    task_id: str
    # src_img = 
    # ref_img = 

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/start-task/")
async def start_task(request: TaskRequest):
    task = long_task.apply_async(args=[request.task_id])
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"status": task.state}
    elif task.state != 'FAILURE':
        response = {
            "status": task.state,
            "result": task.result
        }
    else:
        response = {
            "status": task.state,
            "result": str(task.info)
        }
    return response

