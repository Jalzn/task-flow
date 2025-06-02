from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    id: int = Field(primary_key=True)

    team_id: int = Field(foreign_key="teams.id")
    team: Optional["Team"] = Relationship(back_populates="employees")

    name: str = Field(min_length=1, max_length=100, unique=True)
    email: str = Field(min_length=1, max_length=255, unique=True)

    tasks: List["Task"] = Relationship(back_populates="owner")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)