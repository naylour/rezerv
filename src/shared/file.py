from enum import Enum
from pathlib import Path


class UpsertResult(Enum):
    ALREADY_EXIST = "already_exists"
    CREATED = "created"


def upsert(file: Path, force=False) -> UpsertResult:
    """Создаёт файл; при force пересоздаёт существующий."""
    if file.exists():
        if not force:
            return UpsertResult.ALREADY_EXIST
        file.unlink()

    file.touch()

    return UpsertResult.CREATED
