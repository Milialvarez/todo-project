from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import case
from sqlalchemy.orm import Session
from app.core.exceptions import PermissionDeniedError, TaskNotFoundError
from app.db.session import get_db
from app.db.models import models
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
        raise TaskNotFoundError(task.task_id)

    if task_from_db.user_id != current_user.id:
        raise PermissionDeniedError()

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
        raise TaskNotFoundError(task_id)

    if task_from_db.user_id != current_user.id:
        raise PermissionDeniedError()

    db.delete(task_from_db)
    db.commit()
    return None


@router.get("/me", response_model=List[TaskRead])
def get_my_tasks(db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)):
    tasks = (
        db.query(models.Task)
        .filter(models.Task.user_id == current_user.id)
        .order_by(
            case(
                    (models.Task.status == "pending", 1),
                    (models.Task.status == "in_progress", 2),
                    (models.Task.status == "completed", 3),
                else_=4
            ).asc()  
        )
        .all()
    )
    return tasks

@router.get("/status/{status}", response_model=List[TaskRead]) 
def get_tasks_by_status( status: models.StatusEnum, 
                        db: Session = Depends(get_db), 
                        current_user: models.User = Depends(get_current_user) ): 
    tasks = (db.query(models.Task)
             .filter( models.Task.status == status, models.Task.user_id == current_user.id )
             .all())
    return tasks