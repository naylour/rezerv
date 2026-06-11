import typer

from backup import list_backups

list_app = typer.Typer()


@list_app.command("list")
def list_command():
    """Показывает список доступных резервных копий."""
    backups = list_backups()

    if not backups:
        print("Резервные копии не найдены")
        return

    print("Доступные резервные копии:")
    for index, archive in enumerate(backups, start=1):
        print(f"{index}. {archive.name}")
