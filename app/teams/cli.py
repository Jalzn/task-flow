import typer

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from app.database import get_session
from app.teams.schemas import TeamCreate, TeamResponse
from app.teams.services import TeamService

console = Console()

app = typer.Typer()

@app.command("create")
def create(
    name: str = typer.Option(..., "--name",help="Nome do time"),
    description: str = typer.Option(None, "--description", help="Descrição do time")
):
    service = TeamService(get_session())

    try:
        schema = TeamCreate(name=name, description=description)
        team = service.create(schema)

        console.print(
            Panel(
                f"[green]Time criado com sucesso![/green]\n"
                f"ID: {team.id}\n"
                f"Nome: {team.name}\n"
                f"Descrição: {team.description or 'N/A'}",
                title="✅ Sucesso",
                border_style="green"
            )
        )
    except Exception as e:
        console.print(f"[red]Erro ao criar time: {e}[/red]")


@app.command("list")
def list_teams():
    service = TeamService(get_session())
    try:
        teams = service.get_all()

        if len(teams) == 0:
            console.print("[yellow]Nenhum time encontrado.[/yellow]")
            return

        table = Table(title="📋 Lista de Times")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nome", style="magenta")
        table.add_column("Descrição")
        table.add_column("Funcionários", justify="center")
        table.add_column("Tarefas", justify="center")
        
        for team in teams:
            table.add_row(
                str(team.id),
                team.name,
                team.description or "N/A",
                str(team.employees_count),
                str(team.tasks_count)
            )
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Erro ao criar time: {e}[/red]")