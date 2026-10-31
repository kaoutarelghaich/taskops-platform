import os
import threading
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response, status
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field

APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="TaskOps API", version=APP_VERSION)
Instrumentator().instrument(app).expose(app, include_in_schema=False)

TASKS_GAUGE = Gauge("taskops_tasks", "Number of tasks currently stored")


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class Task(TaskIn):
    id: str


# In-memory store: fine for a demo, use a real database for multi-replica deployments.
_tasks: dict[str, Task] = {}
_lock = threading.Lock()


@app.get("/")
def root() -> dict:
    return {"service": "taskops-api", "version": APP_VERSION}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict:
    return {"status": "ready"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    with _lock:
        return list(_tasks.values())


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskIn) -> Task:
    task = Task(id=str(uuid4()), **payload.model_dump())
    with _lock:
        _tasks[task.id] = task
        TASKS_GAUGE.set(len(_tasks))
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    with _lock:
        task = _tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskIn) -> Task:
    with _lock:
        if task_id not in _tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        task = Task(id=task_id, **payload.model_dump())
        _tasks[task_id] = task
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> Response:
    with _lock:
        if _tasks.pop(task_id, None) is None:
            raise HTTPException(status_code=404, detail="Task not found")
        TASKS_GAUGE.set(len(_tasks))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
