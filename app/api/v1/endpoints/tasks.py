from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()

@router.post("/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == task.user_id).first() #verify user exists
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if task.status not in models.StatusEnum.__members__.values(): #verify is a valid enum for status of the task
        raise ValueError(f"Invalid status: {task.status}")


    new_task = models.Task(
        title=task.title,
        description=task.description,
        status=models.StatusEnum(task.status),
        user_id=task.user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.put("/", response_model=TaskRead)
def update_task(task: TaskUpdate, db:Session = Depends(get_db)):
    task_from_db = db.query(models.Task).filter(models.Task.id == task.task_id).first()

    if not task_from_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.title is None and task.description is None and task.status is None:
        raise HTTPException(status_code=400, detail="At least one field must be provided")
    
    if task.title is not None:
        task_from_db.title = task.title

    if task.description is not None:
        task_from_db.description = task.description

    if task.status is not None:
        task_from_db.status = task.status
    
    db.commit()
    db.refresh(task_from_db)

    return task_from_db

@router.delete("/", response_model=bool)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_from_db = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task_from_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    try:
        db.delete(task_from_db)
        db.commit()
        return True
    except:
        return False

@router.get("/user/{id}", response_model=List[TaskRead])
def get_tasks_by_user_id(user_id: int, db:Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()

    if not tasks:
        raise HTTPException(status_code=500, detail="internal server error")
    
    return tasks
    
