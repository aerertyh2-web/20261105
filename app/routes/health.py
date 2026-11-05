"""不含业务数据的技术健康检查。"""

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Blueprint, current_app, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db

bp = Blueprint("health", __name__)


@bp.get("/healthz")
def healthz():
    try:
        db.session.execute(text("SELECT 1"))
        journal_mode = db.session.execute(text("PRAGMA journal_mode")).scalar()
        foreign_keys = db.session.execute(text("PRAGMA foreign_keys")).scalar()
    except SQLAlchemyError:
        current_app.logger.exception("健康检查无法连接数据库")
        response = jsonify({"状态": "异常", "消息": "数据库连接失败，请稍后再试。"})
        response.status_code = 503
        response.headers["Cache-Control"] = "no-store"
        return response

    checks_passed = str(journal_mode).lower() == "wal" and foreign_keys == 1
    now = datetime.now(ZoneInfo(current_app.config["TIMEZONE"]))
    payload = {
        "状态": "正常" if checks_passed else "异常",
        "数据库": "已连接",
        "数据库日志模式": str(journal_mode).upper(),
        "外键约束": "已开启" if foreign_keys == 1 else "未开启",
        "时区": f"{current_app.config['TIMEZONE']}（UTC+08:00）",
        "当前时间": now.isoformat(timespec="seconds"),
        "数据目录": "data/",
    }
    if not checks_passed:
        payload["消息"] = "数据库运行模式不符合 WAL 或外键约束要求。"

    response = jsonify(payload)
    response.status_code = 200 if checks_passed else 503
    response.headers["Cache-Control"] = "no-store"
    return response
