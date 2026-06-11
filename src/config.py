from pathlib import Path

CWD_PATH: Path = Path.cwd()
REZERV_PATH: Path = CWD_PATH / ".rezerv"
SNAPSHOT_PATH: Path = REZERV_PATH / "snapshot.json"
MANIFEST_PATH: Path = REZERV_PATH / "manifest.json"
LOGS_PATH: Path = REZERV_PATH / "logs.log"
BACKUPS_DIR: Path = CWD_PATH / "backups"
RESTORED_DIR: Path = CWD_PATH / "restored_data"
