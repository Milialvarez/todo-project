from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime

class ReminderCreate(BaseModel):
    date: datetime.date = Field(
        ...,
        description="Date reminder",
        example="2026-01-15"
    )

    description: str = Field(
        ...,
        min_length=3,
        max_length=255
    )

    @field_validator("date")
    @classmethod
    def date_cannot_be_in_the_past(cls, value: datetime.date):
        if value < datetime.date.today():
            raise ValueError("the reminder date cannot have passed")
        return value


class ReminderUpdate(BaseModel):
    reminder_id: int = Field(
        ...,
        gt=0,
        description="ID of the reminder to be updated",
        example=1
    )

    date: Optional[datetime.date] = Field(
        None,
        description="New reminder's date",
        example="2026-02-01"
    )

    description: Optional[str] = Field(
        None,
        min_length=3,
        max_length=255,
        description="New reminder's description",
        example="Go shopping christmas gifts"
    )

    @field_validator("date")
    @classmethod
    def date_cannot_be_in_the_past(cls, value: Optional[datetime.date]):
        if value and value < date.today():
            raise ValueError("the reminder date cannot have passed")
        return value


class ReminderRead(BaseModel):
    id: int = Field(
        ...,
        example=1
    )

    date: Optional[datetime.date] = Field(
        None,
        example="2026-01-15"
    )

    description: str = Field(
        ...,
        example="Pay spotify premium"
    )

    class Config:
        from_attributes = True

