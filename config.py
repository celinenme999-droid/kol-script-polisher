"""
配置文件 - 脚本修改工作流
"""

import os
from typing import Dict, Any

# API配置
API_CONFIG = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "models": {
            "gpt-4": "gpt-4",
            "gpt-4-turbo": "gpt-4-turbo-preview",
            "gpt-3.5-turbo": "gpt-3.5-turbo"
        }
    },
    "qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": {
            "qwen-turbo": "qwen-turbo",
            "qwen-plus": "qwen-plus",
            "qwen-max": "qwen-max"
        }
    },
    "claude": {
        "base_url": "https://api.anthropic.com/v1",
        "models": {
            "claude-3-opus": "claude-3-opus-20240229",
            "claude-3-sonnet": "claude-3-sonnet-20240229"
        }
    }
}

# 达人分析提示词模板
INFLUENCER_ANALYSIS_PROMPT = """
请分析以下达人账号主页的内容，提取以下信息：

1. 平台类型（抖音/小红书/微博/B站等）
2. 内容风格（幽默/严肃/感性/理性等）
3. 达人类型（生活/美妆/科技/教育等）
4. 受众群体（年龄/性别/兴趣等）
5. 语言基调（活泼/正式/接地气/文艺等）
6. 常用表达方式（口头禅/句式特点等）

达人主页内容：
{content}

请以JSON格式返回分析结果：
{{
    "platform": "平台",
    "style": "内容风格",
    "type": "达人类型",
    "audience": "受众群体",
    "tone": "语言基调",
    "expressions": ["常用表达1", "常用表达2"]
}}
"""

# 脚本修改提示词模板
SCRIPT_MODIFICATION_PROMPT = """
你是一位专业的短视频脚本修改专家。请根据以下要求修改脚本：

【产品植入要求/Brief】
{brief}

【达人风格分析】
平台：{platform}
内容风格：{style}
达人类型：{type}
受众群体：{audience}
语言基调：{tone}
常用表达：{expressions}

【原始脚本】
{original_script}

【修改要求】
1. 严格遵循产品植入要求
2. 调整语言风格，符合达人特点
3. 确保语序通顺自然
4. 保持脚本的核心信息不变
5. 根据创意程度（{creativity_level}/10）进行调整
6. 语气调整：{tone_adjustment}
7. 长度控制：{length_control}

【历史修改记录】（避免重复）
{history}

请输出修改后的脚本，只返回脚本内容，不要包含其他说明。
"""

# 网页抓取配置
SCRAPER_CONFIG = {
    "timeout": 30,
    "headless": True,
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# 文件配置
FILE_CONFIG = {
    "output_dir": "output",
    "data_dir": "data",
    "templates_dir": "templates",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "allowed_extensions": [".xlsx", ".xls"]
}

# 应用配置
APP_CONFIG = {
    "title": "脚本修改工作流",
    "page_icon": "📝",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "max_history": 50,
    "batch_size": 10
}

# 记忆配置
MEMORY_CONFIG = {
    "enabled": True,
    "max_entries": 100,
    "retention_days": 30
}

# 错误消息
ERROR_MESSAGES = {
    "no_file": "请先上传Excel文件",
    "no_url": "请输入达人账号链接",
    "no_brief": "请填写产品植入要求",
    "no_api_key": "请配置API Key",
    "invalid_file": "文件格式不正确，请上传Excel文件",
    "api_error": "API调用失败，请检查API Key和网络连接",
    "scraper_error": "抓取达人信息失败，请检查链接是否正确"
}

# 成功消息
SUCCESS_MESSAGES = {
    "file_uploaded": "文件上传成功",
    "analysis_complete": "达人分析完成",
    "modification_complete": "脚本修改完成",
    "download_ready": "文件已准备好下载"
}

# 达人平台映射
PLATFORM_MAPPING = {
    "douyin.com": "抖音",
    "xiaohongshu.com": "小红书",
    "weibo.com": "微博",
    "bilibili.com": "B站",
    "kuaishou.com": "快手",
    "youtube.com": "YouTube",
    "tiktok.com": "TikTok"
}

# 默认设置
DEFAULT_SETTINGS = {
    "creativity_level": 5,
    "tone_adjustment": "保持原样",
    "length_control": "保持原长度",
    "api_provider": "OpenAI",
    "model": "gpt-4"
}


def get_api_config(provider: str) -> Dict[str, Any]:
    """获取指定提供商的API配置"""
    return API_CONFIG.get(provider.lower(), {})


def get_prompt_template(template_name: str) -> str:
    """获取提示词模板"""
    templates = {
        "influencer_analysis": INFLUENCER_ANALYSIS_PROMPT,
        "script_modification": SCRIPT_MODIFICATION_PROMPT
    }
    return templates.get(template_name, "")


def get_platform_from_url(url: str) -> str:
    """从URL中提取平台名称"""
    for domain, platform in PLATFORM_MAPPING.items():
        if domain in url:
            return platform
    return "未知平台"


def validate_file(file) -> tuple[bool, str]:
    """验证上传的文件"""
    if file is None:
        return False, ERROR_MESSAGES["no_file"]
    
    if file.size > FILE_CONFIG["max_file_size"]:
        return False, f"文件大小超过限制（最大{FILE_CONFIG['max_file_size'] // 1024 // 1024}MB）"
    
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in FILE_CONFIG["allowed_extensions"]:
        return False, ERROR_MESSAGES["invalid_file"]
    
    return True, SUCCESS_MESSAGES["file_uploaded"]
