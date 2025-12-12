from pydantic import BaseModel

from app.db.models import StatusEnum

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: StatusEnum = StatusEnum.pending
    user_id: int


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: StatusEnum

    class Config:
        orm_mode = True
