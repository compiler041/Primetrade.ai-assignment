from pydantic import BaseModel, ConfigDict
import datetime
from enum import Enum


class Status(str, Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    done = "done"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description: str | None = None
    due_date: datetime.date | None = None
    assignee: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    title: str


class TaskCreate(TaskBase):
    project_id: int


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_id: int | None = None
