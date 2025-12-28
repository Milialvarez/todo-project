from typing import Optional
from pydantic import BaseModel
from datetime import date

class ReminderCreate(BaseModel):
    date: date
    description: str 

class ReminderUpdate(BaseModel):
    reminder_id: int
    date: Optional[date] | None
    description: Optional[str] = None

class ReminderRead(BaseModel):
    id: int
    date: date | None
    description: str

    class Config:
        from_attributes = True
