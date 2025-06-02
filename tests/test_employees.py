import pytest

from app.employees.models import Employee
from app.employees.schemas import EmployeeCreate
from app.employees.services import EmployeeService

from unittest.mock import patch

from tests.fixtures import session


@pytest.fixture
def service(session):
    return EmployeeService(session)


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
def test_create_employee_duplicate_name_or_email(mock_validate_email, service: EmployeeService):
    schema = EmployeeCreate(name="Jalmir", email="jalmir@email.com", team_id=1)
    service.create_employee(schema)

    # Mesmo nome
    schema_dup_name = EmployeeCreate(name="Jalmir", email="novo@email.com", team_id=1)
    with pytest.raises(Exception, match="Funcionario ja cadastrado"):
        service.create_employee(schema_dup_name)

    # Mesmo email
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


def test_exists_by_name_and_email(service: EmployeeService):
    assert not service.exists_by_name("X")
    assert not service.exists_by_email("x@email.com")

    service.session.add(Employee(name="X", email="x@email.com", team_id=1))
    service.session.commit()

    assert service.exists_by_name("X")
    assert service.exists_by_email("x@email.com")
