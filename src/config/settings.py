from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

SUPPORTING_DATA_DIR = DATA_DIR / "supporting"

DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_FILE = DATABASE_DIR / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

LOG_DIR = PROJECT_ROOT / "logs"

REPORT_DIR = PROJECT_ROOT / "reports"

for directory in [
    OUTPUT_DIR,
    LOG_DIR,
    DATABASE_DIR,
    REPORT_DIR,
    PROCESSED_DATA_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)