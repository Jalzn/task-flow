import pytest
from app.tasks.services import TaskService
from app.tasks.schemas import TaskCreate
from app.tasks.models import TaskStatus, TaskPriority, Task
from app.teams.services import TeamService
from app.teams.schemas import TeamCreate
from app.employees.services import EmployeeService
from app.employees.schemas import EmployeeCreate


@pytest.fixture
def setup_team(session):
    team = TeamService(session).create(TeamCreate(name="Alpha", description="Equipe de testes"))
    return team


@pytest.fixture
def setup_employee(session, setup_team):
    schema = EmployeeCreate(name="Maria", email="maria@email.com", team_id=setup_team.id)
    return EmployeeService(session).create_employee(schema)


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


def test_update_task_details(session, setup_team):
    task = TaskService(session).create_task(TaskCreate(title="Original", description="", team_id=setup_team.id))
    updated = TaskService(session).update_task(task.id, TaskUpdate(title="Atualizada", description="Nova"))
    assert updated.title == "Atualizada"
    assert updated.description == "Nova"


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
    stats = TaskService(session).get_task_statistics()
    assert isinstance(stats, dict)
    assert stats.get("total") == 2
