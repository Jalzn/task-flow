import pytest

from app.employees.models import Employee
from app.employees.schemas import EmployeeCreate
from app.employees.services import EmployeeService

from app.database import create_db_and_tables

from unittest.mock import patch

from typer.testing import CliRunner
from main import app

from tests.fixtures import session


runner = CliRunner()

@pytest.fixture
def service(session):
    return EmployeeService(session)

@pytest.fixture(autouse= True)
def setup_database():
    create_db_and_tables(test=True)


@patch("app.employees.utils.validate_email", return_value=True)
def test_create_employee_success(mock_validate_email, service: EmployeeService):
    schema = EmployeeCreate(name="Jalmir", email="jalmir@email.com", team_id=1)

    employee = service.create_employee(schema)

    assert employee.id is not None
    assert employee.name == "Jalmir"
    assert employee.email == "jalmir@email.com"


@patch("app.employees.utils.validate_email", return_value=False)
def test_create_employee_invalid_email(mock_validate_email, service: EmployeeService):
    schema = EmployeeCreate(name="Fulano", email="invalido", team_id=2)

    with pytest.raises(Exception, match="Email invalido"):
        service.create_employee(schema)


@patch("app.employees.utils.validate_email", return_value=True)
def test_create_employee_duplicate_name(mock_validate_email, service: EmployeeService):
    schema = EmployeeCreate(name="Jalmir", email="jalmir@email.com", team_id=1)
    service.create_employee(schema)

    schema_dup_name = EmployeeCreate(name="Jalmir", email="novo@email.com", team_id=1)
    with pytest.raises(Exception, match="Funcionario ja cadastrado"):
        service.create_employee(schema_dup_name)

@patch("app.employees.utils.validate_email", return_value=True)
def test_create_employee_duplicate_email(mock_validate_email, service: EmployeeService):
    schema = EmployeeCreate(name="Jalmir", email="jalmir@email.com", team_id=1)
    service.create_employee(schema)

    schema_dup_email = EmployeeCreate(name="Novo", email="jalmir@email.com", team_id=1)
    with pytest.raises(Exception, match="Funcionario ja cadastrado"):
        service.create_employee(schema_dup_email)


def test_get_all_employees(service: EmployeeService):
    assert service.get_all_employees() == []

    service.session.add(Employee(name="Ana", email="ana@email.com", team_id=2))
    service.session.commit()

    employees = service.get_all_employees()
    assert len(employees) == 1
    assert employees[0].name == "Ana"


def test_get_employee_by_id(service: EmployeeService):
    employee = Employee(name="Carlos", email="carlos@email.com", team_id=3)
    service.session.add(employee)
    service.session.commit()
    service.session.refresh(employee)

    result = service.get_employee_by_id(employee.id)
    assert result.name == "Carlos"

    with pytest.raises(Exception, match="Funcionario nao encontrado"):
        service.get_employee_by_id(999)


def test_exists_by_name(service: EmployeeService):
    assert not service.exists_by_name("X")
   
    service.session.add(Employee(name="X", email="x@email.com", team_id=1))
    service.session.commit()

    assert service.exists_by_name("X")

def test_exists_by_email(service: EmployeeService):
    assert not service.exists_by_email("x@email.com")

    service.session.add(Employee(name="X", email="x@email.com", team_id=1))
    service.session.commit()

    assert service.exists_by_email("x@email.com")

def test_e2e_create_employee_no_name():
    result = runner.invoke(app, 
                           [
                               "employees", "create"
                            ])
    
    assert result.exit_code != 0
    assert "Missing option" in result.output
    assert "--name" in result.output

def test_e2e_create_employee_no_email():
    result = runner.invoke(app, 
                           [
                               "employees", "create",
                               "--name", 'Teste'
                            ])
    
    assert result.exit_code != 0
    assert "Missing option" in result.output
    assert "--email" in result.output
    
def teste_e2e_list_employee_empty():
   result = runner.invoke(app, ["employees", "list"])
   
   assert result.exit_code == 0
   assert "Nenhum funcionário encontrado" in result.output
   
def teste_e2e_list_employee_success():
   runner.invoke(app, [
            "teams", "create",
            "--name", "Teste1",
            "--description", "Time de teste1"
        ])
   runner.invoke(app, [
       "employees", "create",
       "--name", "Test1",
       "--email", "test@test.com",
       "--team", "1"])
   result = runner.invoke(app, ["employees", "list"])
   assert "Test1" in result.output
    
