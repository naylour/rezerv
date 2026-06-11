from typing import Annotated

import typer

from backup import list_backups, restore_backup

restore_app = typer.Typer()


@restore_app.command()
def restore(
    name: Annotated[
        str | None, typer.Argument(help="Имя архива для восстановления")
    ] = None,
):
    """Восстанавливает данные из выбранной копии."""
    backups = list_backups()

    if not backups:
        print("Резервные копии не найдены")
        return

    if name is not None:
        archive = next((item for item in backups if item.name == name), None)
        if archive is None:
            print(f"Архив {name} не найден")
            return
        restore_backup(archive)
        return

    print("Доступные резервные копии:")
    for index, archive in enumerate(backups, start=1):
        print(f"{index}. {archive.name}")

    choice = typer.prompt("Введите номер копии для восстановления", type=int)
    if choice < 1 or choice > len(backups):
        print("Неверный номер резервной копии")
        return

    restore_backup(backups[choice - 1])
