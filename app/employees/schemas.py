from typing import Optional
from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    """Schema para criação de Funcionário."""
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=255)
    team_id: int = Field()


class EmployeeRead(BaseModel):
    """Schema para leitura de Funcionário."""
    id: int
    team_name: str = ""
    task_count: int = 0


class EmployeeUpdate(BaseModel):
    """Schema para atualização de Funcionário."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=1, max_length=255)
    team_id: Optional[int] = Field(default=None)
