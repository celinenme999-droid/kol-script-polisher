@echo off
REM 脚本修改工作流 - 快速启动脚本 (Windows)

echo ==================================
echo   脚本修改工作流 - 快速启动
echo ==================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python版本：%PYTHON_VERSION%
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
    echo ✅ 虚拟环境创建成功
    echo.
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo.

REM 安装依赖
echo 📥 安装依赖包...
pip install -r requirements.txt
echo ✅ 依赖包安装完成
echo.

REM 安装Playwright浏览器
echo 🌐 安装Playwright浏览器...
playwright install chromium
echo ✅ Playwright浏览器安装完成
echo.

REM 创建必要的目录
echo 📁 创建必要的目录...
if not exist "data" mkdir data
if not exist "output" mkdir output
if not exist "templates" mkdir templates
echo ✅ 目录创建完成
echo.

REM 生成示例模板
echo 📊 生成示例Excel模板...
python create_template.py
echo ✅ 示例模板生成完成
echo.

REM 启动应用
echo ==================================
echo   🚀 启动应用...
echo ==================================
echo.
echo 应用将在浏览器中打开：http://localhost:8501
echo.
echo 按 Ctrl+C 停止应用
echo.

streamlit run app.py

pause
