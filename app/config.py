"""应用配置：所有持久化数据统一位于项目 data/ 目录。"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def _data_dir() -> Path:
    configured = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))
    if not configured.is_absolute():
        configured = BASE_DIR / configured
    return configured.resolve()


DATA_DIR = _data_dir()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATA_ENCRYPTION_KEY = os.getenv("DATA_ENCRYPTION_KEY")
    TIMEZONE = "Asia/Shanghai"
    TZ = TIMEZONE

    DATA_DIR = DATA_DIR
    UPLOAD_DIR = DATA_DIR / "uploads"
    BACKUP_DIR = DATA_DIR / "backups"
    LOG_DIR = DATA_DIR / "logs"

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{(DATA_DIR / 'app.db').as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    MAX_CONTENT_LENGTH = 1024 * 1024
    JSON_AS_ASCII = False
