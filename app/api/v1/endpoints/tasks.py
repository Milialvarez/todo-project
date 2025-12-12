from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas.task import TaskCreate, TaskRead

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
