"""
文档读取工具 - 支持PDF和DOCX
"""

import os
from typing import Optional


def read_pdf(file_path: str) -> str:
    """读取PDF文件内容"""
    import pdfplumber
    
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    
    return "\n\n".join(text_parts)


def read_docx(file_path: str) -> str:
    """读取DOCX文件内容"""
    from docx import Document
    
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def read_document(file_path: str) -> str:
    """自动识别文件类型并读取"""
    if not os.path.exists(file_path):
        return ""
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == ".pdf":
        return read_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return read_docx(file_path)
    else:
        return ""


class DataLoader:
    """数据加载器 - 加载Brief和软性要求"""
    
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "kol_polishing")
    
    BRIEF_PATHS = {
        "parenting": "briefs/parenting",
        "tech_review": "briefs/tech_review",
        "comparison": "briefs/comparison",
    }
    
    @classmethod
    def get_brief(cls, category: str) -> str:
        """获取指定垂类的Brief内容"""
        brief_dir = os.path.join(cls.DATA_DIR, cls.BRIEF_PATHS.get(category, "briefs/parenting"))
        
        if not os.path.exists(brief_dir):
            return ""
        
        for filename in os.listdir(brief_dir):
            if filename.lower().endswith((".pdf", ".docx", ".doc")):
                file_path = os.path.join(brief_dir, filename)
                return read_document(file_path)
        
        return ""
    
    @classmethod
    def get_soft_requirements(cls) -> str:
        """获取通用软性要求"""
        req_dir = os.path.join(cls.DATA_DIR, "requirements")
        
        if not os.path.exists(req_dir):
            return ""
        
        for filename in os.listdir(req_dir):
            if filename.lower().endswith((".pdf", ".docx", ".doc")):
                file_path = os.path.join(req_dir, filename)
                return read_document(file_path)
        
        return ""
    
    @classmethod
    def get_brief_filename(cls, category: str) -> str:
        """获取Brief文件名"""
        brief_dir = os.path.join(cls.DATA_DIR, cls.BRIEF_PATHS.get(category, "briefs/parenting"))
        
        if not os.path.exists(brief_dir):
            return "未找到"
        
        for filename in os.listdir(brief_dir):
            if filename.lower().endswith((".pdf", ".docx", ".doc")):
                return filename
        
        return "未找到"
    
    @classmethod
    def get_requirements_filename(cls) -> str:
        """获取软性要求文件名"""
        req_dir = os.path.join(cls.DATA_DIR, "requirements")
        
        if not os.path.exists(req_dir):
            return "未找到"
        
        for filename in os.listdir(req_dir):
            if filename.lower().endswith((".pdf", ".docx", ".doc")):
                return filename
        
        return "未找到"
