from typing import Any, Dict, List, Optional

from sqlmodel import Session, select

from app.tasks.models import Task, TaskStatus
from app.tasks.schemas import TaskCreate


class TaskService:
    """Serviço para operações com tarefas."""

    def __init__(self, session: Session):
        self.session = session
    
    def create_task(self, schema: TaskCreate) -> Task:
        task = Task(
            title = schema.title,
            description = schema.description,
            team_id = schema.team_id,
            owner_id = schema.owner_id,
            priority = schema.priority,
            status = TaskStatus.PENDING
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        raise Exception("Method not implemented")
    
    def get_all_tasks(self) -> List[Task]:
        return self.session.exec(select(Task)).all()
    
    def get_tasks_by_team(self, team_id: int) -> List[Task]:
        raise Exception("Method not implemented")
    
    def get_tasks_by_employee(self, employee_id: int) -> List[Task]:
        raise Exception("Method not implemented")
    
    def update_task(self, task_id: int) -> Optional[Task]:
        raise Exception("Method not implemented")
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        raise Exception("Method not implemented")
    
    def assign_task(self, task_id: int, employee_id: int) -> Optional[Task]:
        raise Exception("Method not implemented")
    
    def delete_task(self, task_id: int) -> bool:
        raise Exception("Method not implemented")
    
    def get_task_statistics(self) -> Dict[str, Any]:
        raise Exception("Method not implemented")