from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
import enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base



# use sqlalchemy as orm to create my tables automatically

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")


class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(
        Enum(StatusEnum, name="status_enum"),
        default=StatusEnum.pending,
        nullable=False
    )
