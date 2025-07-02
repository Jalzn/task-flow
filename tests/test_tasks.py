import pytest
from pydantic import ValidationError

from app.tasks.services import TaskService
from app.tasks.schemas import TaskCreate
from app.tasks.models import TaskStatus, TaskPriority, Task

from app.teams.services import TeamService
from app.teams.schemas import TeamCreate

from app.employees.services import EmployeeService
from app.employees.schemas import EmployeeCreate

from app.database import create_db_and_tables

from tests.fixtures import session

from typer.testing import CliRunner
from main import app

runner = CliRunner()

@pytest.fixture
def setup_team(session):
    team = TeamService(session).create(TeamCreate(name="Alpha", description="Equipe de testes"))
    return team

@pytest.fixture
def setup_employee(session, setup_team):
    schema = EmployeeCreate(name="Maria", email="maria@email.com", team_id=setup_team.id)
    return EmployeeService(session).create_employee(schema)

@pytest.fixture(autouse= True)
def setup_database():
    create_db_and_tables(test=True)

def test_create_task_success(session, setup_team):
    schema = TaskCreate(
        title="Revisar código",
        description="Verificar pull requests",
        team_id=setup_team.id,
        priority=TaskPriority.MEDIUM
    )
    task = TaskService(session).create_task(schema)
    assert task.id is not None
    assert task.title == "Revisar código"
    assert task.status == TaskStatus.PENDING

def test_create_task_missing_title():
    with pytest.raises(ValidationError) as exc:
        TaskCreate(description="Desc", team_id=1)
    assert "Field required" in str(exc.value)

def test_create_task_name_max_length():
    long_title = "x"*201
    with pytest.raises(ValidationError) as exc:
        TaskCreate(title=long_title, description="Desc", team_id=1)
    assert "String should have at most 200 characters" in str(exc.value)

def test_create_task_default_description_none():
    schema = TaskCreate(title="T1", team_id=1)
    assert schema.description is None

def test_create_task_description_max_length():
    long_description = "x"*1001
    with pytest.raises(ValidationError) as exc:
        TaskCreate(title="title", description=long_description, team_id=1)
    assert "String should have at most 1000 characters" in str(exc.value)

def test_create_task_missing_team_id():
    with pytest.raises(ValidationError) as exc:
        TaskCreate(title="T1", description="Desc")
    assert "Field required" in str(exc.value)

def test_create_task_schema_default_priority_medium():
    schema = TaskCreate(
        title="Teste Prioridade Padrão",
        team_id=1
    )
    assert schema.priority == TaskPriority.MEDIUM

def test_create_task_service_default_priority_medium(session, setup_team):
    schema = TaskCreate(
        title="Teste Serviço Prioridade Padrão",
        description="",
        team_id=setup_team.id
    )
    task = TaskService(session).create_task(schema)
    assert task.priority == TaskPriority.MEDIUM

def test_get_all_tasks_returns_created(session, setup_team):
    TaskService(session).create_task(TaskCreate(title="T1", description="D1", team_id=setup_team.id))
    TaskService(session).create_task(TaskCreate(title="T2", description="D2", team_id=setup_team.id))
    tasks = TaskService(session).get_all_tasks()
    assert len(tasks) == 2


def test_get_task_by_id(session, setup_team):
    task = TaskService(session).create_task(TaskCreate(title="Verificar", description="Tarefa", team_id=setup_team.id))
    found = TaskService(session).get_task_by_id(task.id)
    assert found.id == task.id
    assert found.title == "Verificar"


def test_get_tasks_by_team(session, setup_team):
    TaskService(session).create_task(TaskCreate(title="1", description="", team_id=setup_team.id))
    tasks = TaskService(session).get_tasks_by_team(setup_team.id)
    assert len(tasks) == 1


def test_get_tasks_by_employee(session, setup_team, setup_employee):
    task = TaskService(session).create_task(TaskCreate(title="Atribuída", description="", team_id=setup_team.id))
    TaskService(session).assign_task(task.id, setup_employee.id)
    employee_tasks = TaskService(session).get_tasks_by_employee(setup_employee.id)
    assert len(employee_tasks) == 1
    assert employee_tasks[0].id == task.id

def test_update_task_status(session, setup_team):
    task = TaskService(session).create_task(TaskCreate(title="Status Test", description="", team_id=setup_team.id))
    updated = TaskService(session).update_task_status(task.id, TaskStatus.COMPLETED)
    assert updated.status == TaskStatus.COMPLETED


def test_assign_task_to_employee(session, setup_team, setup_employee):
    task = TaskService(session).create_task(TaskCreate(title="Para Maria", description="", team_id=setup_team.id))
    assigned = TaskService(session).assign_task(task.id, setup_employee.id)
    assert assigned.owner_id == setup_employee.id


def test_delete_task(session, setup_team):
    task = TaskService(session).create_task(TaskCreate(title="Excluir", description="", team_id=setup_team.id))
    TaskService(session).delete_task(task.id)
    with pytest.raises(Exception):
        TaskService(session).get_task_by_id(task.id)


def test_get_task_statistics(session, setup_team):
    TaskService(session).create_task(TaskCreate(title="T1", description="", team_id=setup_team.id, priority=TaskPriority.HIGH))
    TaskService(session).create_task(TaskCreate(title="T2", description="", team_id=setup_team.id, priority=TaskPriority.LOW))
    TaskService(session).create_task(TaskCreate(title="T3", description="", team_id=setup_team.id, priority=TaskPriority.MEDIUM))
    TaskService(session).create_task(TaskCreate(title="T4", description="", team_id=setup_team.id, priority=TaskPriority.MEDIUM))
    stats = TaskService(session).get_task_statistics()
    assert isinstance(stats, dict)
    assert stats.get("total") == 4
    assert stats.get("Baixa") == 1
    assert stats.get("Media") == 2
    assert stats.get("Alta") == 1

def test_e2e_create_task_missing_title_argument():
    result = runner.invoke(app, ["tasks", "create"], color=False)
    assert result.exit_code != 0
    assert "Missing option '--title" in result.output

def test_e2e_create_task_missing_description_argument():
    result = runner.invoke(app, ["tasks", "create", "--title", "Task1"], color=False)
    assert result.exit_code != 0
    assert "Missing option '--description" in result.output

def test_e2e_create_task_missing_team_id_argument():
    result = runner.invoke(app, ["tasks", "create", "--title", "Task1", "--description", "Description1"], color=False)
    assert result.exit_code != 0
    assert "Missing option '--team-id" in result.output

def test_e2e_create_task_sucess():
    result = runner.invoke(app, ["tasks", "create", "--title", "Task1", "--description", "Description1", "--team-id","1"], color=False)
    assert result.exit_code == 0
    assert "Tarefa criada com sucesso!" in result.output