from pathlib import Path
from dotenv import load_dotenv
import os

# project root
BASE_DIR = Path(__file__).resolve().parents[2]

# .env path
ENV_PATH = BASE_DIR / ".env"

# load .env variables
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

def get_env(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)
