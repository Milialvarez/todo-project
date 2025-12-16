from pydantic import BaseModel
from datetime import date

class ReminderCreate(BaseModel):
    date: date
    description: str 

class ReminderUpdate(BaseModel):
    reminder_id: int
    date: date
    description: str | None = None

class ReminderRead(BaseModel):
    id: int
    date: date
    description: str | None = None

    class Config:
        from_attributes = True  
