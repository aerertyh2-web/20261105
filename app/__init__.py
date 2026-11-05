"""个人工作台 Flask 应用工厂。"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

from app import database  # noqa: F401  注册 SQLite 连接监听器
from app.config import Config
from app.extensions import db, migrate


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.from_mapping(test_config)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("缺少 SECRET_KEY，请先完成本地环境配置。")

    data_dir = Path(app.config["DATA_DIR"])
    app.config["DATA_DIR"] = data_dir
    for key, directory_name in (
        ("UPLOAD_DIR", "uploads"),
        ("BACKUP_DIR", "backups"),
        ("LOG_DIR", "logs"),
    ):
        directory = Path(app.config.get(key, data_dir / directory_name))
        directory.mkdir(parents=True, exist_ok=True)
        app.config[key] = directory

    app.json.ensure_ascii = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.health import bp as health_bp

    app.register_blueprint(health_bp)
    _configure_logging(app)
    return app


def _configure_logging(app):
    if app.testing or app.logger.handlers:
        return

    handler = RotatingFileHandler(
        app.config["LOG_DIR"] / "app.log",
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s：%(message)s")
    )
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
