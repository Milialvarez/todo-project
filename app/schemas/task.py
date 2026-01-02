from typing import Optional
from pydantic import BaseModel, Field, field_validator

from app.db.models.models import StatusEnum

class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        description= "task title, describes briefly the task",
        example="going to the market"
    )

    description: Optional[str] = Field(
        None,
        description="Task description, explains with more detail the objective of the task",
        example="Buy: napkins, towels, jam, cheese"
    )

    status: StatusEnum = Field(
        default=StatusEnum.pending,
        description="Current status of the task",
        example="pending"
    )

    @field_validator("status")
    @classmethod
    def forbid_completed_on_create(cls, value: StatusEnum):
        if value == StatusEnum.completed:
            raise ValueError("A task cannot be created as completed")
        return value


class TaskUpdate(BaseModel):
    task_id: int = Field(
        ...,
        description="Task ID, allows to determinate wich task is going to be updated",
        example=1
    )
    title: str | None = None
    description: str | None = None
    status: StatusEnum | None = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: StatusEnum

    class Config:
        from_attributes = True
