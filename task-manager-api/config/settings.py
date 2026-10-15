import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-123")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", f"sqlite:///{BASE_DIR / 'tasks.db'}")
SQLALCHEMY_TRACK_MODIFICATIONS = False
