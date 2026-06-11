import shutil
import zipfile
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path

from config import CWD_PATH, RESTORED_DIR
from logger import logger
from manifest import read_manifest
from snapshot import Snapshot, read_snapshot, write_snapshot


def read_gitignore(root: Path) -> list[str]:
    """Читает шаблоны из .gitignore, пропуская пустые строки и комментарии."""
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return []

    patterns = []
    for line in gitignore.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line.rstrip("/"))
    return patterns


def is_ignored(relative: str, patterns: list[str]) -> bool:
    """Проверяет, попадает ли путь под один из шаблонов игнорирования."""
    parts = relative.split("/")
    for pattern in patterns:
        if fnmatch(relative, pattern):
            return True
        if any(fnmatch(part, pattern) for part in parts):
            return True
    return False


def scan_files(watch_dir: Path, patterns: list[str]) -> Snapshot:
    """Собирает отображение относительный путь -> время изменения."""
    snapshot: Snapshot = {}
    for path in watch_dir.rglob("*"):
        if path.is_file():
            relative = path.relative_to(watch_dir).as_posix()
            if is_ignored(relative, patterns):
                continue
            snapshot[relative] = path.stat().st_mtime
    return snapshot


def create_backup(full=False, ignore=None, use_gitignore=False) -> Path | None:
    """Создаёт ZIP-копию изменённых (или всех при full) файлов."""
    manifest = read_manifest()
    watch_dir = Path(manifest.watch_dir)
    backups_dir = Path(manifest.backups_dir)

    if not watch_dir.exists():
        logger.warning(f"Отслеживаемая директория {watch_dir} не найдена")
        return None

    patterns = list(ignore or [])
    if use_gitignore:
        patterns += read_gitignore(CWD_PATH)

    current = scan_files(watch_dir, patterns)
    previous: Snapshot = {} if full else read_snapshot()

    changed = {
        relative: mtime
        for relative, mtime in current.items()
        if previous.get(relative) != mtime
    }

    if not changed:
        logger.info("Изменений нет, резервная копия не требуется")
        return None

    backups_dir.mkdir(parents=True, exist_ok=True)

    kind = "full" if full else "incr"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_path = backups_dir / f"backup_{kind}_{timestamp}.zip"

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for relative in changed:
            archive.write(watch_dir / relative, relative)

    write_snapshot(current)

    logger.info(f"Резервная копия создана: {archive_path}")
    logger.info(f"Файлов в копии: {len(changed)}")
    return archive_path


def list_backups() -> list[Path]:
    """Возвращает отсортированный список архивов из папки бэкапов."""
    backups_dir = Path(read_manifest().backups_dir)
    if not backups_dir.exists():
        return []
    return sorted(backups_dir.glob("*.zip"))


def restore_backup(archive: Path) -> bool:
    """Распаковывает архив в папку восстановления."""
    if not archive.exists():
        logger.warning(f"Архив {archive} не найден")
        return False

    if RESTORED_DIR.exists():
        shutil.rmtree(RESTORED_DIR)
    RESTORED_DIR.mkdir(parents=True)

    with zipfile.ZipFile(archive, "r") as archive_file:
        archive_file.extractall(RESTORED_DIR)

    logger.info(f"Данные восстановлены в {RESTORED_DIR}")
    return True
