from typing import Any
from .base import BASE_DIR


DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AKKOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

CORS_ORIGIN_WHITELIST: list[str] = [
    "http://localhost:5173",
]
