import typer

from rich.console import Console
from rich.panel import Panel

from app import employees, tasks, teams
from app.database import create_db_and_tables

console = Console()

app = typer.Typer(
    name="TODO CLI",
    help="Sistema de Gerenciamento de Tarefas",
    rich_markup_mode="rich"
)

app.add_typer(employees.cli.app, name="employees")
app.add_typer(teams.cli.app, name="teams")
app.add_typer(tasks.cli.app, name="tasks")

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="Mostrar versão")
):
    if version:
        console.print("TODO CLI v1.0.0")
        return
    
    if ctx.invoked_subcommand is None:
        create_db_and_tables()
        
        console.print(
            Panel.fit(
                "[bold blue]TODO CLI[/bold blue]\n"
                "Sistema de Gerenciamento de Tarefas Empresariais\n\n"
                "Use --help para ver comandos disponíveis",
                title="Bem vindo",
                border_style="blue"
            )
        )

if __name__ == "__main__":
    app()