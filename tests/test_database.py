"""SQLite WAL、外键、重连和目录验收。"""

import sqlite3
from pathlib import Path
from urllib.parse import urlparse

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.extensions import db


def _database_path(app):
    return Path(urlparse(app.config["SQLALCHEMY_DATABASE_URI"]).path.lstrip("/"))


def test_database_and_runtime_directories_are_under_data(app):
    database_path = _database_path(app)

    with app.app_context():
        db.session.execute(text("SELECT 1"))

    assert database_path.parent == app.config["DATA_DIR"]
    assert database_path.is_file()
    for key in ("UPLOAD_DIR", "BACKUP_DIR", "LOG_DIR"):
        assert app.config[key].is_dir()
        assert app.config[key].parent == app.config["DATA_DIR"]


def test_wal_and_foreign_keys_survive_engine_reconnect(app):
    with app.app_context():
        first_mode = db.session.execute(text("PRAGMA journal_mode")).scalar()
        db.session.remove()
        db.engine.dispose()
        second_mode = db.session.execute(text("PRAGMA journal_mode")).scalar()
        foreign_keys = db.session.execute(text("PRAGMA foreign_keys")).scalar()
        busy_timeout = db.session.execute(text("PRAGMA busy_timeout")).scalar()

    assert first_mode.lower() == "wal"
    assert second_mode.lower() == "wal"
    assert foreign_keys == 1
    assert busy_timeout == 5000


def test_wal_mode_is_persistent_for_a_new_raw_sqlite_connection(app):
    database_path = _database_path(app)
    with app.app_context():
        db.session.execute(text("SELECT 1"))
        db.engine.dispose()

    connection = sqlite3.connect(database_path)
    try:
        assert connection.execute("PRAGMA journal_mode").fetchone()[0].lower() == "wal"
    finally:
        connection.close()


def test_foreign_key_constraint_rejects_invalid_rows(app):
    with app.app_context():
        db.session.execute(text("CREATE TABLE parent (id INTEGER PRIMARY KEY)"))
        db.session.execute(
            text(
                "CREATE TABLE child ("
                "id INTEGER PRIMARY KEY, "
                "parent_id INTEGER NOT NULL REFERENCES parent(id))"
            )
        )
        with pytest.raises(IntegrityError):
            db.session.execute(text("INSERT INTO child (parent_id) VALUES (999)"))
        db.session.rollback()
