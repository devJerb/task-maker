from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(title="Custom Connector", version="1.0.0", docs_url="/")


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: str
    created_at: datetime
    completed: bool = False

    class Config:
        from_attributes = True


# In-memory storage
tasks_db = {}


@app.get("/")
async def root():
    """Root endpoint returning API status"""
    return {"status": "online", "timestamp": datetime.now()}


@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """Create a new task"""
    task_id = str(uuid.uuid4())
    task_dict = task.model_dump()
    task_dict.update({"id": task_id, "created_at": datetime.now(), "completed": False})
    tasks_db[task_id] = task_dict
    return task_dict


@app.get("/tasks/", response_model=List[Task])
async def list_tasks():
    """List all tasks"""
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task by ID"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return tasks_db[task_id]


@app.patch("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskBase):
    """Update a task"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    task_dict = tasks_db[task_id]
    update_data = task.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        task_dict[field] = value

    tasks_db[task_id] = task_dict
    return task_dict


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    del tasks_db[task_id]
    return None


@app.post("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: str):
    """Mark a task as completed"""
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    tasks_db[task_id]["completed"] = True
    return tasks_db[task_id]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
