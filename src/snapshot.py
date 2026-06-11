import json

from config import SNAPSHOT_PATH
from logger import logger
from shared import UpsertResult, file

Snapshot = dict[str, float]


def upsert_snapshot(force=False):
    """Создаёт файл снимка, если его нет."""
    result = file.upsert(SNAPSHOT_PATH, force)

    if result == UpsertResult.CREATED:
        logger.info("Файл снимка создан")
    elif result == UpsertResult.ALREADY_EXIST:
        logger.warning("Файл снимка уже существует")


def read_snapshot() -> Snapshot:
    """Читает снимок состояния файлов."""
    content = SNAPSHOT_PATH.read_text()
    if not content:
        return {}
    return json.loads(content)


def write_snapshot(snapshot: Snapshot):
    """Сохраняет снимок состояния файлов."""
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=4))
