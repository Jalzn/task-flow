from typing import Optional
from pydantic import BaseModel, Field

from app.tasks.models import TaskPriority, TaskStatus


# class TaskResponse(BaseModel):
#     title: str = Field(index=True, min_length=1, max_length=200)
#     description: Optional[str] = Field(default=None, max_length=1000)
#     status: TaskStatus = Field(default=TaskStatus.PENDING)
#     priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
#     team_id: int = Field(foreign_key="team.id")
#     assignee_id: Optional[int] = Field(default=None, foreign_key="employee.id")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    team_id: int
    owner_id: Optional[int] = None
    priority: TaskPriority = TaskPriority.MEDIUM