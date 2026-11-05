# 多用户个人工作台

这是一个使用 **Python Flask + SQLite（WAL）+ Bootstrap 5 服务端渲染** 的中文多用户个人工作台项目。

当前处于 **M0 工程基线**：只有应用骨架、健康检查、数据库连接和迁移基线，尚未开放安装向导、注册登录、任务、提醒等业务功能。完整范围及验收计划见 [docs/plan.md](docs/plan.md)。

## 一、最简单的启动方式（Windows 图形界面）

1. 在文件资源管理器中打开项目目录 `D:\qoder`。
2. 双击 `start.bat`。
3. 看到黑色窗口显示 Flask 正在运行后，保持窗口开启。
4. 打开 Chrome 或 Edge，在地址栏输入：`http://127.0.0.1:5000/healthz`。

你不需要修改代码，也不需要输入命令。若窗口提示运行环境未安装，请联系开发工程师处理。

## 二、怎样确认启动成功

浏览器中的健康检查应显示：

- `状态`：`正常`
- `数据库`：`已连接`
- `数据库日志模式`：`WAL`
- `外键约束`：`已开启`
- `时区`：`Asia/Shanghai（UTC+08:00）`
- `当前时间`：带 `+08:00`
- `数据目录`：`data/`

关闭 `start.bat` 打开的窗口即可停止本地应用。重新双击启动后，健康检查仍应正常。

## 三、数据放在哪里

| 内容 | 目录 |
|---|---|
| SQLite 数据库及 WAL 文件 | `data/app.db*` |
| 上传文件 | `data/uploads/` |
| 一次性备份临时文件 | `data/backups/` |
| 应用日志 | `data/logs/app.log` |

数据库、上传文件、备份、日志和真实 `.env` 均已排除在 Git 之外。测试使用独立临时数据库，不会读写正式 `data/app.db`。

## 四、工程初始化（供开发工程师使用）

以下不是用户操作步骤。用户只需使用上面的 `start.bat`。

环境要求：Python 3.12，Windows 10/11。

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python scripts\create_local_env.py
.venv\Scripts\python -m flask --app run.py db upgrade
.venv\Scripts\python run.py
```

`create_local_env.py` 只在 `.env` 不存在时生成随机密钥，已有配置绝不覆盖，也不会把密钥打印到终端。

## 五、运行自动化验收

```bash
.venv\Scripts\python -m pytest
```

测试覆盖：

1. 健康检查返回中文状态、WAL、外键和东八区时间。
2. 健康响应不缓存、不泄露本机绝对路径或密钥。
3. 数据库及运行目录全部位于 `data/`。
4. WAL 在 SQLAlchemy 重连和原生 SQLite 新连接后保持有效。
5. 外键约束会拒绝无效数据，写锁等待为 5 秒。

## 六、目录结构

```text
app/
├── __init__.py          # Flask 应用工厂
├── config.py            # 东八区、data/ 和数据库配置
├── database.py          # SQLite WAL、外键、忙等待
├── extensions.py        # SQLAlchemy 与 Alembic 扩展
├── models/              # 后续对应里程碑的数据模型
├── routes/              # 当前只有 health.py
├── services/            # 后续业务服务
├── templates/           # Jinja2 + Bootstrap 5 基础模板
└── static/              # 本地 Bootstrap 与项目静态资源
data/                    # 不提交 Git 的运行数据
migrations/              # Alembic 数据库迁移
scripts/                 # 本地配置辅助脚本
tests/                   # 独立临时数据库自动化测试
docs/plan.md             # 已确认 P0 开发总纲
.trae/rules.md           # 五条长期协作规则
run.py                   # 本地启动入口
start.bat                # 用户双击启动入口
```

## 七、当前边界

- 本轮没有实现任何业务页面或业务表。
- `/healthz` 只是技术健康检查，不是用户功能。
- 后续每轮只开发指定模块，完成后运行验收、列出假设并提交中文 Git。
- Zeabur、HTTPS、安装向导及管理员应急重置步骤将在对应里程碑补充，当前不声称已经支持生产部署。
- Zeabur 的 5 个环境变量与填写步骤见 [docs/zeabur-env.md](docs/zeabur-env.md)；密钥清单只保存在本机 `data/zeabur-variables.txt`。
