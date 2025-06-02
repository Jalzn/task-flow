from typing import Optional
from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

class TeamResponse(BaseModel):
    id: int
    name: str
    description: str
    employees_count: int
    tasks_count: int