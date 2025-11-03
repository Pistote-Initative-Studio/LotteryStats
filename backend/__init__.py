from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file if present.
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

__all__ = ["PROJECT_ROOT"]
