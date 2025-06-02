from typing import List
from sqlmodel import Session, select

from app.teams.models import Team
from app.teams.schemas import TeamCreate, TeamResponse


class TeamService:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, schema: TeamCreate) -> Team:
        team = Team(
            name = schema.name,
            description = schema.description
        )

        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)

        return team

    def get_all(self) -> List[TeamResponse]:
        return [TeamResponse(
            id=t.id,
            name=t.name,
            description=t.description,
            employees_count=len(t.employees),
            tasks_count=len(t.tasks)
        ) for t in self.session.exec(select(Team)).all()]