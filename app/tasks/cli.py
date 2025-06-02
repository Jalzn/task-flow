import typer

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.database import get_session
from app.tasks.models import TaskPriority, TaskStatus
from app.tasks.schemas import TaskCreate
from app.tasks.services import TaskService

console = Console()

app = typer.Typer()

def get_priority_color(priority: TaskPriority) -> str:
    """Retorna a cor baseada na prioridade."""
    colors = {
        TaskPriority.HIGH: "red",
        TaskPriority.MEDIUM: "yellow", 
        TaskPriority.LOW: "green"
    }
    return colors.get(priority, "white")


def get_status_color(status: TaskStatus) -> str:
    """Retorna a cor baseada no status."""
    colors = {
        TaskStatus.PENDING: "yellow",
        TaskStatus.IN_PROGESS: "blue",
        TaskStatus.COMPLETED: "green"
    }
    return colors.get(status, "white")


@app.command("create")
def create(
    title: str = typer.Option(..., help="Título da tarefa"),
    description: str = typer.Option(..., help="Descrição da tarefa"),
    team_id: int = typer.Option(..., help="ID do time"),
    owner_id: int = typer.Option(None, "--assignee", "-a", help="ID do funcionário responsável"),
    priority: TaskPriority = typer.Option(TaskPriority.MEDIUM, "--priority", "-p", help="Prioridade da tarefa")

):
    service = TaskService(get_session())

    try:
        schema = TaskCreate(
            title=title,
            description=description,
            team_id=team_id,
            owner_id=owner_id,
            priority=priority
        )

        task = service.create_task(schema)

        console.print(
            Panel(
                f"[green]Tarefa criada com sucesso![/green]\n"
                f"ID: {task.id}\n"
                f"Título: {task.title}\n"
                f"Descrição: {task.description or 'N/A'}\n"
                f"Status: {task.status.value}\n"
                f"Prioridade: {task.priority.value}\n"
                f"Time ID: {task.team_id}\n"
                f"Responsável ID: {task.owner_id or 'Não atribuído'}",
                title="✅ Sucesso",
                border_style="green"
            )
        )
    except Exception as e:
        console.print(f"[red]Erro ao criar tarefa: {e}[/red]")
        raise typer.Exit(1)


@app.command("list")
def list_tasks():
    service = TaskService(get_session())

    try:
        tasks = service.get_all_tasks()

        if not tasks:
            console.print("[yellow]Nenhuma tarefa encontrada.[/yellow]")
            return
        
        table = Table(title="📋 Lista de Tarefas")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Título", style="magenta")
        table.add_column("Status")
        table.add_column("Prioridade")
        table.add_column("Time")
        table.add_column("Responsável")
        
        for task in tasks:
            status_color = get_status_color(task.status)
            priority_color = get_priority_color(task.priority)
            
            table.add_row(
                str(task.id),
                task.title,
                f"[{status_color}]{task.status}[/{status_color}]",
                f"[{priority_color}]{task.priority}[/{priority_color}]",
                task.team.name,
                task.owner_id or "Não atribuído"
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Erro ao listar tarefa: {e}[/red]")
        raise typer.Exit(1)