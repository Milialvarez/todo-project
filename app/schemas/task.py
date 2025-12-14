from pydantic import BaseModel

from app.db.models import StatusEnum

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: StatusEnum = StatusEnum.pending

class TaskUpdate(BaseModel):
    task_id: int
    title: str | None = None
    description: str | None = None
    status: StatusEnum | None = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: StatusEnum

    class Config:
        orm_mode = True
