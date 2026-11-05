"""测试使用独立临时数据库，绝不接触 data/app.db。"""

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app(tmp_path):
    data_dir = tmp_path / "data"
    database_path = data_dir / "test.db"
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-only-secret",
            "DATA_DIR": data_dir,
            "UPLOAD_DIR": data_dir / "uploads",
            "BACKUP_DIR": data_dir / "backups",
            "LOG_DIR": data_dir / "logs",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
        }
    )
    yield application
    with application.app_context():
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()
