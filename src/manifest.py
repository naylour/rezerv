import json
from dataclasses import asdict, dataclass

from config import MANIFEST_PATH
from logger import logger
from shared import UpsertResult, file


@dataclass
class Manifest:
    watch_dir: str
    backups_dir: str


def set_new_manifest(watch_dir: str, backups_dir: str):
    """Записывает манифест с путями проекта."""
    MANIFEST_PATH.write_text(
        json.dumps(asdict(Manifest(watch_dir, backups_dir)), indent=4)
    )


def read_manifest() -> Manifest:
    """Читает манифест из файла."""
    return Manifest(**json.loads(MANIFEST_PATH.read_text()))


def upsert_manifest(force=False) -> UpsertResult:
    """Создаёт файл манифеста, если его нет."""
    result = file.upsert(MANIFEST_PATH, force)

    if result == UpsertResult.CREATED:
        logger.info("Файл манифеста создан")
    elif result == UpsertResult.ALREADY_EXIST:
        logger.warning("Файл манифеста уже существует")

    return result
