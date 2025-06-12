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
        task = self.session.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            raise Exception("Tarefa não encontrada")
        return task
    
    def get_all_tasks(self) -> List[Task]:
        tasks = self.session.exec(select(Task)).all()
        return tasks
    
    def get_tasks_by_team(self, team_id: int) -> List[Task]:
        tasks = self.session.exec(select(Task).where(Task.team_id == team_id)).all()
        return tasks
    
    def get_tasks_by_employee(self, employee_id: int) -> List[Task]:
        tasks = self.session.exec(select(Task).where(Task.owner_id == employee_id)).all()
        return tasks
    
    def update_task(self, task_id: int) -> Optional[Task]:
        pass
        # raise Exception("Method not implemented")
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        task.status = status
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def assign_task(self, task_id: int, employee_id: int) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        task.owner_id = employee_id
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        self.session.delete(task)
        self.session.commit()
        return True
    
    def get_task_statistics(self) -> Dict[str, Any]:
        tasks = self.get_all_tasks() or []
        stats = {
            "Baixa": 0,
            "Media": 0,
            "Alta": 0,
            "total": len(tasks)
        }
        for task in tasks:
            if task.priority is not None:
                prio = str(task.priority)
                stats[prio] = stats.get(prio, 0) + 1
        print(stats)
        return stats