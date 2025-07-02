import pytest
from pydantic import ValidationError
import typer
from typer.testing import CliRunner

from app.database import create_db_and_tables
from main import app

from app.teams.models import Team
from app.teams.schemas import TeamCreate, TeamResponse
from app.teams.services import TeamService

from tests.fixtures import session

@pytest.fixture
def team_service(session):
    return TeamService(session)

@pytest.fixture(autouse= True)
def setup_database():
    create_db_and_tables(test=True)


def test_create_team_success(team_service: TeamService):
    schema = TeamCreate(name="Team A", description="Time de desenvolvimento")
    team = team_service.create(schema)
    assert team.id is not None
    assert team.name == "Team A"
    assert team.description == "Time de desenvolvimento"

def test_creat_team_default_description_none():
    schema = TeamCreate(name="Team B")
    assert schema.description is None

def test_create_team_missing_name():
    with pytest.raises(ValidationError) as exc:
        TeamCreate(description="Team B")
    assert "Field required" in str(exc.value)

def test_create_team_name_max_length():
    long_name = "x"*101
    with pytest.raises(ValidationError) as exc:
        TeamCreate(name=long_name, description="desc")
    assert "String should have at most 100 characters" in str(exc.value)

def test_create_team_description_max_length():
    long_name = "x"*501
    with pytest.raises(ValidationError) as exc:
        TeamCreate(name=long_name, description="desc")
    assert "String should have at most 100 characters" in str(exc.value)

def test_get_all_teams(team_service: TeamService):
    team_service.session.add(Team(name="Team B", description="QA"))
    team_service.session.commit()
    teams = team_service.get_all()
    assert len(teams) == 1
    assert teams[0].name == "Team B"

def test_get_all_teams_empty(team_service: TeamService):
    teams = team_service.get_all()
    assert teams == []

def test_e2e_create_team():
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "teams", "create",
            "--name", "Teste",
            "--description", "Time de teste"
        ]
    )
    assert result.exit_code == 0
    assert "Teste" in result.output

def test_e2e_create_team_with_missing_name():
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "teams", "create",
            "--description", "Time de teste"
        ]
    )
    assert result.exit_code != 0
    assert "Missing option '--name" in result.output


def test_e2e_create_team_with_missing_name():
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "teams", "list",
        ]
    )
    assert result.exit_code == 0
    assert "ID" in result.output
