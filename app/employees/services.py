from typing import List
from sqlmodel import Session, select

from app.employees import utils
from app.employees.models import Employee
from app.employees.schemas import EmployeeCreate


class EmployeeService:
    def __init__(self, session: Session):
        self.session = session

    def create_employee(self, schema: EmployeeCreate) -> Employee:
        is_valid_email = utils.validate_email(schema.email)

        if not is_valid_email:
            raise Exception("Email invalido.")
        
        if self.exists_by_name(schema.name) or self.exists_by_email(schema.email):
            raise Exception("Funcionario ja cadastrado.")

        employee = Employee(
            name = schema.name,
            email = schema.email,
            team_id = schema.team_id
        )

        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)

        return employee

    
    def get_all_employees(self) -> List[Employee]:
        employees = self.session.exec(select(Employee)).all()
        return employees
    
    def get_employee_by_id(self, id: int) -> Employee:
        employee = self.session.exec(select(Employee).where(Employee.id == id)).first()
        
        if not employee:
            raise Exception("Funcionario nao encontrado")

        return employee

    def exists_by_name(self, name: str) -> bool:
        employee = self.session.exec(select(Employee).where(Employee.name == name)).first()

        return True if employee else False

    def exists_by_email(self, email: str) -> bool:
        employee = self.session.exec(select(Employee).where(Employee.email == email)).first()

        return True if employee else False