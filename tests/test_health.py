"""健康检查验收：状态、中文内容、安全响应。"""


def test_health_reports_wal_foreign_keys_and_shanghai_timezone(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["状态"] == "正常"
    assert payload["数据库"] == "已连接"
    assert payload["数据库日志模式"] == "WAL"
    assert payload["外键约束"] == "已开启"
    assert payload["时区"] == "Asia/Shanghai（UTC+08:00）"
    assert payload["当前时间"].endswith("+08:00")
    assert payload["数据目录"] == "data/"


def test_health_is_chinese_json_and_does_not_cache_or_leak_paths(client):
    response = client.get("/healthz")

    assert response.content_type.startswith("application/json")
    assert response.headers["Cache-Control"] == "no-store"
    assert "正常" in response.get_data(as_text=True)
    assert "D:\\" not in response.get_data(as_text=True)
    assert "SECRET" not in response.get_data(as_text=True)


def test_health_does_not_accept_writes(client):
    response = client.post("/healthz")

    assert response.status_code == 405
