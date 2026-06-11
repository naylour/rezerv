import typer

from cli.backup import backup_app
from cli.init import init_app
from cli.list import list_app
from cli.restore import restore_app

cli = typer.Typer(
    name="rezerv",
    add_completion=False,
)

cli.add_typer(init_app)
cli.add_typer(backup_app)
cli.add_typer(list_app)
cli.add_typer(restore_app)


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
):
    if ctx.invoked_subcommand is None:
        print("Добро пожаловать в rezerv!")
        print("Используй --help для получения списка команд")
