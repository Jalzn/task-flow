import typer

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from app.database import get_session
from app.employees.schemas import EmployeeCreate
from app.employees.services import EmployeeService

console = Console()

app = typer.Typer()

@app.command("create")
def create(
    name: str = typer.Option(..., "--name", help="Nome do funcionario"),
    email: str = typer.Option(..., "--email", help="Email do funcionario"),
    team: int = typer.Option(..., "--team", help="Id do time responsavel pelo funcionario")
):
    service = EmployeeService(get_session())

    try:
        schema = EmployeeCreate(name = name, email = email, team_id = team)
        employee = service.create_employee(schema)

        console.print(
            Panel(
                f"[green]Funcionário criado com sucesso![/green]\n"
                f"ID: {employee.id}\n"
                f"Nome: {employee.name}\n"
                f"Email: {employee.email}\n"
                f"Time ID: {employee.team_id}",
                title="✅ Sucesso",
                border_style="green"
            )
        )
    except Exception as e:
        console.print(f"[red]Erro ao criar funcionário: {e}[/red]")
        raise typer.Exit(1)


@app.command("list")
def list_employees():
    service = EmployeeService(get_session())

    try:
        employees = service.get_all_employees()
        
        if not employees:
            console.print("[yellow]Nenhum funcionário encontrado.[/yellow]")
            return
        
        table = Table(title="👥 Lista de Funcionários")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nome", style="magenta")
        table.add_column("Email", style="blue")
        table.add_column("Time")
        table.add_column("Tarefas", justify="center")
        
        for employee in employees:
            table.add_row(
                str(employee.id),
                employee.name,
                employee.email,
                employee.team.name,
                str(len(employee.tasks))
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Erro ao listar funcionários: {e}[/red]")
        raise typer.Exit(1)