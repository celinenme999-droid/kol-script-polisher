#!/bin/bash

# 脚本修改工作流 - 快速启动脚本

echo "=================================="
echo "  脚本修改工作流 - 快速启动"
echo "=================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

echo "✅ Python版本：$(python3 --version)"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
    echo ""
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate
echo "✅ 虚拟环境已激活"
echo ""

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt
echo "✅ 依赖包安装完成"
echo ""

# 安装Playwright浏览器
echo "🌐 安装Playwright浏览器..."
playwright install chromium
echo "✅ Playwright浏览器安装完成"
echo ""

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p data output templates
echo "✅ 目录创建完成"
echo ""

# 生成示例模板
echo "📊 生成示例Excel模板..."
python create_template.py
echo "✅ 示例模板生成完成"
echo ""

# 启动应用
echo "=================================="
echo "  🚀 启动应用..."
echo "=================================="
echo ""
echo "应用将在浏览器中打开：http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止应用"
echo ""

streamlit run app.py
