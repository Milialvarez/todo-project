from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import models
from app.core.deps import get_current_user
from app.schemas.reminder import ReminderCreate, ReminderRead, ReminderUpdate

router = APIRouter()

# already working well
@router.post("/", response_model=ReminderRead, status_code=status.HTTP_201_CREATED)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    new_reminder = models.Reminder(
        description=reminder.description,
        date=reminder.date,       
        user_id=current_user.id
    )

    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return new_reminder

# already working well
@router.put("/", response_model=ReminderRead)
def update_reminder(reminder: ReminderUpdate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    reminder_from_db = db.query(models.Reminder).filter(models.Reminder.id == reminder.reminder_id).first()
    if not reminder_from_db:
        raise HTTPException(status_code=404, detail="reminder not found")

    if reminder_from_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this reminder")

    if reminder.description is None and reminder.date is None:
        raise HTTPException(status_code=400, detail="At least one field must be provided")

    if reminder_from_db.description is not None:
        reminder_from_db.description = reminder.description

    db.commit()
    db.refresh(reminder_from_db)
    return reminder_from_db


@router.delete("/{rem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(rem_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    reminder_from_db = db.query(models.Reminder).filter(models.Reminder.id == rem_id).first()
    if not reminder_from_db:
        raise HTTPException(status_code=404, detail="Reminder not found")

    if reminder_from_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this reminder")

    db.delete(reminder_from_db)
    db.commit()
    return None

# already working well
@router.get("/me", response_model=List[ReminderRead])
def get_my_reminders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    rems = (
        db.query(models.Reminder)
        .filter(models.Reminder.user_id == current_user.id)
        .order_by(models.Reminder.date)
        .all()
    )
    return rems

