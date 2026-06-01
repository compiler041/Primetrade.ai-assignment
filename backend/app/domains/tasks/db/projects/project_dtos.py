from enum import Enum
from pydantic import BaseModel
import datetime
import typing as t
from app.domains.tasks.db.tasks.task_dtos import Task


class Status(str, Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    done = "done"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ProjectBase(BaseModel):
    description: str | None = None
    due_date: datetime.date | None = None
    assignee: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    title: str

    class Config:
        orm_mode = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    tasks: list[Task] = []
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
