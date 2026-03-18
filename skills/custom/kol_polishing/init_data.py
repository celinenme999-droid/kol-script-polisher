#!/usr/bin/env python3
"""
数据初始化脚本
将Brief、参考脚本、软性要求导入知识库
"""

import json
import os
from datetime import datetime

# 数据目录
DATA_DIR = "/Users/fengyiman/Desktop/UAD/script-modifier-workflow/data/kol_polishing"
BRIEFS_DIR = os.path.join(DATA_DIR, "briefs/parenting")
BRIEFS_DIR = os.path.join(DATA_DIR, "briefs/tech_review")
BRIEFS_DIR = os.path.join(DATA_DIR, "briefs/comparison")
REFS_DIR = os.path.join(DATA_DIR, "references/parenting")
REFS_DIR = os.path.join(DATA_DIR, "references/tech_review")
REFS_DIR = os.path.join(DATA_DIR, "references/comparison")
REQ_DIR = os.path.join(DATA_DIR, "requirements")


def ensure_dirs():
    """确保所有目录存在"""
    for dir_path in [BRIEFS_DIR, REFS_DIR, REF_DIR, REF_DIR, REF_DIR]:
        os.makedirs(dir_path, exist_ok=True)


def copy_source_files():
    """复制原始文件到数据目录"""
    source_dir = "/Users/fengyiman/Desktop/try/knowledge_base"
    
    # 复制Brief文件
    import shutil
    brief_files = [
        "Brief-亲子教育&好物推荐&科技测评达人 .pdf",
        "Brief-竞对横评 达人.pdf"
    ]
    
    for brief_file in brief_files:
        src = os.path.join(source_dir, brief_file)
        # 亲子好物科技测评Brief -> parenting目录
        if "亲子" in brief_file or "好物" in brief_file or "科技" in brief_file:
            dst = os.path.join(BRIEFS_DIR, "parenting", brief_file)
        # 竞对横评Brief -> comparison目录
        elif "竞对" in brief_file or "横评" in brief_file:
            dst = os.path.join(BRIEFS_DIR, "comparison", brief_file)
        else:
            dst = os.path.join(BRIEFS_DIR, "tech_review", brief_file)
    
    # 复制Excel参考脚本
    excel_files = [
        "参考脚本-小红书亲子教育KOL脚本-啊是小星星啊.xlsx",
        "参考脚本-小红书好物推荐KOL脚本-夕熙妈咪.xlsx",
        "参考脚本-小红书科技测评KOL脚本-不赖的皮特Pitt.xlsx",
        "参考脚本-小红书竞对横评KOL脚本-又又又小姐.xlsx"
    ]
    
    for excel_file in excel_files:
        src = os.path.join(source_dir, excel_file)
        # 亲子教育 -> parenting
        if "亲子教育" in excel_file:
            dst = os.path.join(REFS_DIR, "parenting", excel_file)
        # 好物推荐 -> parenting
        elif "好物推荐" in excel_file:
            dst = os.path.join(REFS_DIR, "parenting", excel_file)
        # 科技测评 -> tech_review
        elif "科技测评" in excel_file:
            dst = os.path.join(REFS_DIR, "tech_review", excel_file)
        # 竞对横评 -> comparison
        elif "竞对横评" in excel_file:
            dst = os.path.join(REFS_DIR, "comparison", excel_file)
    
    # 复制软性要求
    docx_file = "通用软性要求.docx"
    shutil.copy(
        os.path.join(source_dir, docx_file),
        REQ_DIR
    )
    print(f"✅ 软性要求已复制到: {REQ_DIR}")
    
    # 复制固定空白模板
    template_file = "固定空白模板.xlsx"
    dst = os.path.join(REFS_DIR, "parenting", template_file)  # 也放到parenting
    shutil.copy(
        os.path.join(source_dir, template_file),
        os.path.join(REFS_DIR, "parenting", template_file)
    )
    print("\n✅ 文件复制完成！");


def create_initial_data():
    """创建初始数据文件"""
    # 亲子好物Brief
    parenting_brief = {
        "id": "brief_parenting_001",
        "quarter": "2026Q2",
        "brand": "惠普",
        "product": "惠普59x/67x家用学习打印一体机",
        "category": "parenting",
        "content": "亲子好物类达人Brief内容",
        "core_points": [
            "创新6重维稳技术",
            "打印品质稳",
            "持续输出稳", 
            "超大打印量",
            "连接稳定",
            "个性化打印",
            "低成本维护"
        ],
        "forbidden_words": ["绝对", "最好", "第一", "顶级", "必买"],
        "tone_style": "轻松活泼、温馨有爱",
        "created_at": datetime.now().isoformat()
    }
    
    with open(os.path.join(BRIEFS_DIR, "parenting", "brief_2026Q2.json"), 'w', encoding='utf-8') as f:
        json.dump(parenting_brief, f, ensure_ascii=False, indent=2)
    
    # 竞对横评Brief
    comparison_brief = {
        "id": "brief_comparison_001",
        "quarter": "2026Q2",
        "brand": "惠普",
        "product": "惠普58x家用连供打印一体机",
        "category": "comparison",
        "content": "竞对横评类达人Brief内容",
        "core_points": [
            "创新6重维稳技术",
            "打印品质对比优势",
            "输出稳定性优势",
            "维护成本优势",
            "纸张适配优势"
        ],
        "forbidden_words": ["绝对", "最好", "第一", "顶级", "必买"],
        "tone_style": "客观专业、有说服力",
        "created_at": datetime.now().isoformat()
    }
    
    with open(os.path.join(BRIEFS_DIR, "comparison", "brief_2026Q2.json"), 'w', encoding='utf-8') as f:
        json.dump(comparison_brief, f, ensure_ascii=False, indent=2)
    
    # 软性要求
    soft_requirements = {
        "id": "req_001",
        "category": "通用要求",
        "content": """
1. 开头切入点要自然
2. 拍摄风格轻松自然
3. 标题封面要吸睛
4. 结尾推荐要真诚
5. 避免生硬植入
6. 口语化、无AI感
        """,
        "created_at": datetime.now().isoformat()
    }
    
    with open(os.path.join(REQ_DIR, "requirements.json"), 'w', encoding='utf-8') as f:
        json.dump({"soft_requirements": [soft_requirements]}, f, ensure_ascii=False, indent=2)
    
    print("✅ 初始数据创建完成!")


if __name__ == "__main__":
    ensure_dirs()
    copy_source_files()
    create_initial_data()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎉 数据初始化完成!")
    print("="*60)
