from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.employees.models import Employee
from app.teams.models import Team


class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def __str__(self) -> str:
        values = {
            TaskPriority.LOW: "Baixa",
            TaskPriority.MEDIUM: "Media",
            TaskPriority.HIGH: "Alta",
        }

        return values[self]


class TaskStatus(Enum):
    PENDING = 0
    IN_PROGESS = 1
    COMPLETED = 2

    def __str__(self) -> str:
        values = {
            TaskStatus.PENDING: "Pendente",
            TaskStatus.IN_PROGESS: "Em Progresso",
            TaskStatus.COMPLETED: "Finalizada",
        }

        return values[self]


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(primary_key=True)

    owner_id: Optional[int] = Field(default=None, nullable=True, foreign_key="employees.id")
    owner: Optional["Employee"] = Relationship(back_populates="tasks")
    team_id: int = Field(foreign_key="teams.id")
    team: Team = Relationship(back_populates="tasks")

    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)
    status: TaskStatus = Field()
    priority: TaskPriority = Field()

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)