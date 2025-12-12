from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,       
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/", response_model=TaskRead)
def update_task(task: TaskUpdate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    task_from_db = db.query(models.Task).filter(models.Task.id == task.task_id).first()
    if not task_from_db:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_from_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

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


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    task_from_db = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task_from_db:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_from_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(task_from_db)
    db.commit()
    return None


@router.get("/me", response_model=List[TaskRead])
def get_my_tasks(db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    return tasks
