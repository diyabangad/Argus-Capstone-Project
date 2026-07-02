from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BACKEND_DIR / "data"
DATABASE_PATH = DATA_DIR / "argus_demo.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"
