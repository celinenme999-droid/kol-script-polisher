# 🌐 部署指南

本指南将帮助您将脚本修改工作流部署到云端，生成可分享的网页链接。

## 📋 部署前准备

1. **准备代码**
   - 确保所有代码文件完整
   - 测试本地运行正常

2. **准备API Key**
   - OpenAI API Key：https://platform.openai.com/api-keys
   - 通义千问 API Key：https://dashscope.aliyun.com/apiKey
   - Claude API Key：https://console.anthropic.com/

3. **GitHub账号**（用于代码托管）

---

## 🚀 方案一：Streamlit Cloud（推荐，免费）

### 步骤1：上传代码到GitHub

```bash
# 初始化Git仓库
cd script-modifier-workflow
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 创建GitHub仓库后，关联远程仓库
git remote add origin https://github.com/your-username/script-modifier-workflow.git

# 推送代码
git push -u origin main
```

### 步骤2：部署到Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 点击 "New app"
3. 填写信息：
   - **Repository**：选择你的GitHub仓库
   - **Branch**：选择 `main`
   - **Main file path**：`app.py`
4. 点击 "Deploy"

### 步骤3：配置环境变量

1. 在Streamlit Cloud应用页面
2. 点击 "Settings" → "Secrets"
3. 添加以下环境变量：
   - `OPENAI_API_KEY`：你的OpenAI API Key
   - `QWEN_API_KEY`：你的通义千问 API Key（可选）
   - `CLAUDE_API_KEY`：你的Claude API Key（可选）

### 步骤4：访问应用

部署完成后，你会获得一个类似这样的链接：
```
https://your-app-name.streamlit.app
```

分享这个链接给团队成员即可使用。

---

## 🚀 方案二：Hugging Face Spaces（免费）

### 步骤1：创建Space

1. 访问 https://huggingface.co/spaces
2. 点击 "Create new Space"
3. 填写信息：
   - **Space name**：例如 `script-modifier-workflow`
   - **License**：选择合适的许可证
   - **SDK**：选择 "Streamlit"
   - **Hardware**：选择 "CPU Basic"（免费）

### 步骤2：上传代码

有两种方式：

**方式A：通过Git上传**
```bash
git clone https://huggingface.co/spaces/your-username/script-modifier-workflow
cd script-modifier-workflow
# 复制你的代码文件到这里
git add .
git commit -m "Initial commit"
git push
```

**方式B：通过网页上传**
1. 在Space页面点击 "Files"
2. 点击 "Add file" → "Upload files"
3. 上传所有代码文件

### 步骤3：配置环境变量

1. 在Space页面点击 "Settings"
2. 找到 "Repository secrets"
3. 添加API Key：
   - `OPENAI_API_KEY`
   - `QWEN_API_KEY`
   - `CLAUDE_API_KEY`

### 步骤4：访问应用

应用会自动构建，完成后访问：
```
https://huggingface.co/spaces/your-username/script-modifier-workflow
```

---

## 🚀 方案三：Railway（有免费额度）

### 步骤1：准备Dockerfile

创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安装Playwright依赖
RUN playwright install-deps chromium

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装Playwright浏览器
RUN playwright install chromium

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8501

# 启动应用
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 步骤2：部署到Railway

1. 访问 https://railway.app/
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择你的GitHub仓库
4. 配置环境变量（在Variables标签页）
5. 点击 "Deploy"

### 步骤3：访问应用

部署完成后，Railway会提供一个公网URL。

---

## 🚀 方案四：Render（有免费额度）

### 步骤1：准备render.yaml

创建 `render.yaml`：

```yaml
services:
  - type: web
    name: script-modifier-workflow
    env: python
    buildCommand: pip install -r requirements.txt && playwright install chromium
    startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: PORT
        value: 8501
      - key: OPENAI_API_KEY
        sync: false
```

### 步骤2：部署到Render

1. 访问 https://render.com/
2. 点击 "New +" → "Web Service"
3. 连接GitHub仓库
4. 配置环境变量
5. 点击 "Create Web Service"

---

## 🔐 安全建议

1. **不要在代码中硬编码API Key**
   - 使用环境变量
   - 使用 `.env` 文件（不要提交到Git）

2. **限制访问权限**
   - 在Streamlit Cloud中可以设置密码保护
   - 使用自定义域名和SSL

3. **监控使用量**
   - 定期检查API调用次数
   - 设置预算限制

---

## 📊 成本估算

| 平台 | 免费额度 | 超出费用 |
|------|----------|----------|
| Streamlit Cloud | 无限制 | 免费 |
| Hugging Face Spaces | CPU Basic免费 | GPU付费 |
| Railway | $5/月 | 按使用量 |
| Render | 免费层 | 按使用量 |

**主要成本：** AI API调用费用
- OpenAI GPT-4：约$0.03/1K tokens
- 通义千问：约¥0.008/1K tokens
- Claude：约$0.015/1K tokens

---

## 🎯 推荐方案

**对于个人/小团队使用：**
- ✅ Streamlit Cloud（最简单，完全免费）

**对于需要更多控制：**
- ✅ Hugging Face Spaces（免费，功能丰富）

**对于企业级应用：**
- ✅ Railway / Render（更多自定义选项）

---

## ❓ 常见问题

**Q: 部署后无法访问？**
A: 检查防火墙设置，确保端口开放。

**Q: API调用失败？**
A: 检查环境变量是否正确配置，API Key是否有效。

**Q: 如何更新应用？**
A: 推送新代码到GitHub，平台会自动重新部署。

**Q: 如何查看日志？**
A: 在部署平台的Logs页面查看。

---

**祝您部署顺利！** 🎉
