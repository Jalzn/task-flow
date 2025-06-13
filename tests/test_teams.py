import pytest

from app.teams.models import Team
from app.teams.schemas import TeamCreate, TeamResponse
from app.teams.services import TeamService

from tests.fixtures import session

@pytest.fixture
def team_service(session):
    return TeamService(session)

def test_create_team_success(team_service: TeamService):
    schema = TeamCreate(name="Team A", description="Time de desenvolvimento")
    team = team_service.create_team(schema)
    assert team.id is not None
    assert team.name == "Team A"
    assert team.description == "Time de desenvolvimento"

def test_get_all_teams(team_service: TeamService):
    assert team_service.get_all_teams() == []
    team_service.session.add(Team(name="Team B", description="QA"))
    team_service.session.commit()
    teams = team_service.get_all_teams()
    assert len(teams) == 1
    assert teams[0].name == "Team B"

def test_get_team_by_id(team_service: TeamService):
    team = Team(name="Team C", description="Infra")
    team_service.session.add(team)
    team_service.session.commit()
    team_service.session.refresh(team)
    found = team_service.get_team_by_id(team.id)
    assert found.name == "Team C"
    with pytest.raises(Exception, match="Equipe nao encontrada"):
        team_service.get_team_by_id(999)

def test_delete_team_success(team_service: TeamService):
    team = Team(name="Team E", description="Delete Me")
    team_service.session.add(team)
    team_service.session.commit()
    team_service.session.refresh(team)
    assert team_service.delete_team(team.id)
    with pytest.raises(Exception):
        team_service.get_team_by_id(team.id)

def test_delete_team_not_found(team_service: TeamService):
    with pytest.raises(Exception, match="Equipe nao encontrada"):
        team_service.delete_team(999)