from pathlib import Path
from typing import Annotated

import typer

from config import BACKUPS_DIR, LOGS_PATH, REZERV_PATH
from logger import logger
from manifest import set_new_manifest, upsert_manifest
from shared import UpsertResult
from snapshot import upsert_snapshot

init_app = typer.Typer()


@init_app.command()
def init(
    watch_dir: Annotated[Path, typer.Argument(help="Отслеживаемая директория")],
    backups_dir: Annotated[
        Path, typer.Argument(help="Директория для резервных копий")
    ] = BACKUPS_DIR,
    force_manifest: Annotated[bool, typer.Option(help="Пересоздать манифест")] = False,
    force_snapshot: Annotated[bool, typer.Option(help="Сбросить снимок")] = False,
):
    """Инициализирует проект: манифест, снимок и журнал."""
    LOGS_PATH.write_text("")

    logger.info("Начинается инициализация проекта")

    watch_dir = Path.cwd() / watch_dir
    if not watch_dir.exists():
        logger.warning(f"Директории {watch_dir} не существует")
        return

    backups_dir = Path.cwd() / backups_dir
    if not backups_dir.exists():
        backups_dir.mkdir()

    logger.info(f"Отслеживаемая директория: {watch_dir}")
    logger.info(f"Путь до кэша rezerv'a: {REZERV_PATH}")

    result = upsert_manifest(force_manifest)
    if result == UpsertResult.CREATED:
        set_new_manifest(watch_dir.as_posix(), backups_dir.as_posix())

    upsert_snapshot(force_snapshot)

    logger.info("Rezerv инициализирован!")
