from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: int = Field(primary_key=True)
    name: str = Field(min_length=1, max_length=100, unique=True)
    description: str = Field(min_length=1, max_length=500)
    employees: List["Employee"] = Relationship(back_populates="team")
    tasks: List["Task"] = Relationship(back_populates="team")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)