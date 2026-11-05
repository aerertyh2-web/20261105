@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo 尚未安装本地运行环境，请联系开发工程师完成初始化。
    pause
    exit /b 1
)

if not exist ".env" (
    ".venv\Scripts\python.exe" "scripts\create_local_env.py"
    if errorlevel 1 (
        echo 本地配置创建失败，请联系开发工程师处理。
        pause
        exit /b 1
    )
)

echo 正在启动个人工作台，请稍候……
echo 启动成功后，请在浏览器打开 http://127.0.0.1:5000/healthz
".venv\Scripts\python.exe" "run.py"

if errorlevel 1 (
    echo 应用异常退出，详细信息已写入 data\logs\app.log。
)
pause
