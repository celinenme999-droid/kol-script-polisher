"""
达人主页分析模块
支持：小红书、抖音、微博
使用MCP web-reader抓取主页内容并分析风格
"""

import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse


def detect_platform(url: str) -> Optional[str]:
    """检测URL对应的平台"""
    url_lower = url.lower()
    
    if "xiaohongshu.com" in url_lower or "xhslink.com" in url_lower:
        return "xiaohongshu"
    elif "douyin.com" in url_lower or "iesdouyin.com" in url_lower:
        return "douyin"
    elif "weibo.com" in url_lower or "weibo.cn" in url_lower:
        return "weibo"
    elif "bilibili.com" in url_lower or "b23.tv" in url_lower:
        return "bilibili"
    
    return None


def extract_xiaohongshu_user_id(url: str) -> Optional[str]:
    """从URL提取小红书用户ID"""
    patterns = [
        r"xiaohongshu\.com/user/profile/([a-zA-Z0-9]+)",
        r"xiaohongshu\.com/explore/user/([a-zA-Z0-9]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_douyin_user_id(url: str) -> Optional[str]:
    """从URL提取抖音用户ID"""
    patterns = [
        r"douyin\.com/user/([a-zA-Z0-9_-]+)",
        r"douyin\.com/@([a-zA-Z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


class InfluencerAnalyzer:
    """达人主页分析器"""
    
    # 达人类型关键词
    PARENTING_KEYWORDS = [
        "宝妈", "亲子", "育儿", "宝宝", "妈妈", "带娃", 
        "孕妈", "辅食", "早教", "幼儿园", "儿童"
    ]
    
    TECH_KEYWORDS = [
        "数码", "科技", "测评", "评测", "手机", "电脑",
        "显卡", "装机", "游戏", "智能家居", "科技宅"
    ]
    
    LIFESTYLE_KEYWORDS = [
        "日常", "生活", "vlog", "穿搭", "好物", "分享",
        "探店", "美食", "旅游", "装修"
    ]
    
    @classmethod
    def analyze_from_text(cls, text: str) -> Dict[str, Any]:
        """从文本内容分析达人风格"""
        text_lower = text.lower()
        
        result = {
            "detected_type": "unknown",
            "type_confidence": 0,
            "style_hints": [],
            "common_expressions": [],
            "tone": "中性"
        }
        
        # 检测达人类型
        parenting_score = sum(1 for kw in cls.PARENTING_KEYWORDS if kw in text)
        tech_score = sum(1 for kw in cls.TECH_KEYWORDS if kw in text)
        lifestyle_score = sum(1 for kw in cls.LIFESTYLE_KEYWORDS if kw in text)
        
        scores = {
            "亲子好物": parenting_score,
            "科技测评": tech_score,
            "生活好物": lifestyle_score
        }
        
        if max(scores.values()) > 0:
            result["detected_type"] = max(scores, key=scores.get)
            result["type_confidence"] = max(scores.values()) / sum(scores.values()) if sum(scores.values()) > 0 else 0
        
        # 提取常用表达
        expressions = []
        expr_patterns = [
            ("姐妹们", "姐妹称呼"),
            ("宝妈们", "宝妈称呼"),
            ("各位", "通用称呼"),
            ("大家", "通用称呼"),
            ("咱们", "亲近称呼"),
            ("真心推荐", "推荐语气"),
            ("闭眼入", "强烈推荐"),
            ("赶紧冲", "紧迫感"),
            ("亲测", "实测验证"),
            ("实测", "实测验证"),
        ]
        
        for expr, desc in expr_patterns:
            if expr in text:
                expressions.append(f"{expr}({desc})")
        
        result["common_expressions"] = expressions
        
        # 判断语气
        if "！" in text or "～" in text or "哈" in text:
            result["tone"] = "活泼亲切"
        elif "数据显示" in text or "实测" in text:
            result["tone"] = "专业客观"
        else:
            result["tone"] = "中性平和"
        
        # 提取风格提示
        style_hints = []
        if "宝妈" in text and "测评" in text:
            style_hints.append("宝妈视角的测评风格")
        if "姐妹" in text:
            style_hints.append("姐妹间的分享语气")
        if "专业" in text or "客观" in text:
            style_hints.append("专业客观的分析态度")
        
        result["style_hints"] = style_hints
        
        return result
    
    @classmethod
    def analyze_from_url(cls, url: str, page_content: str = None) -> Dict[str, Any]:
        """从URL分析达人（如果提供了page_content则使用，否则需要MCP抓取）"""
        platform = detect_platform(url)
        
        result = {
            "url": url,
            "platform": platform or "未知平台",
            "platform_supported": platform is not None,
            "analysis": None,
            "raw_content_preview": None
        }
        
        if page_content:
            result["raw_content_preview"] = page_content[:500] + "..." if len(page_content) > 500 else page_content
            result["analysis"] = cls.analyze_from_text(page_content)
        
        return result


def format_analysis_result(analysis: Dict[str, Any]) -> str:
    """格式化分析结果为可读文本"""
    if not analysis:
        return "未能分析"
    
    lines = []
    
    if analysis.get("detected_type"):
        confidence = analysis.get("type_confidence", 0) * 100
        lines.append(f"📊 推测类型: {analysis['detected_type']} (置信度: {confidence:.0f}%)")
    
    if analysis.get("tone"):
        lines.append(f"🎵 语言语气: {analysis['tone']}")
    
    if analysis.get("common_expressions"):
        lines.append(f"💬 常用表达: {', '.join(analysis['common_expressions'])}")
    
    if analysis.get("style_hints"):
        lines.append(f"✨ 风格特点: {'; '.join(analysis['style_hints'])}")
    
    return "\n".join(lines)
