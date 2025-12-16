from pydantic import BaseModel
from sqlalchemy import Date

from app.db.models.models import StatusEnum

class ReminderCreate(BaseModel):
    date: Date
    description: str | None = None

class ReminderUpdate(BaseModel):
    reminder_id: int
    description: str | None = None
    date: Date

class ReminderRead(BaseModel):
    id: int
    description: str | None = None
    date: Date
    class Config:
        orm_mode = True
