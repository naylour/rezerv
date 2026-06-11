from typing import Annotated

import typer

from backup import create_backup

backup_app = typer.Typer()


@backup_app.command()
def backup(
    full: Annotated[bool, typer.Option(help="Создать полную копию")] = False,
    ignore: Annotated[
        list[str], typer.Option(help="Шаблоны файлов для игнорирования")
    ] = [],
    gitignore: Annotated[
        bool, typer.Option(help="Игнорировать файлы из .gitignore")
    ] = False,
):
    """Создаёт резервную копию отслеживаемой папки."""
    create_backup(full, ignore, gitignore)
