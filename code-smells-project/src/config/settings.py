import os

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
DEBUG = os.environ.get("DEBUG", "false").lower() in ("1", "true", "yes")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "dev-admin-token")
DB_PATH = os.environ.get("DB_PATH", "loja.db")
