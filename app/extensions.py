"""Flask 扩展集中定义，避免循环导入。"""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
