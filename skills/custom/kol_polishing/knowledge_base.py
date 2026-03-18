"""
KOL脚本润色技能 - 记忆/知识库模块
用于存储和管理Brief、软性要求、优秀脚本等知识
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Brief:
    """Brief信息"""
    id: str
    quarter: str  # 季度，如 "2024Q1"
    brand: str  # 品牌
    product: str  # 产品
    content: str  # Brief内容
    core_points: List[str]  # 核心卖点
    forbidden_words: List[str]  # 禁用词
    created_at: str
    updated_at: str
    is_active: bool = True


@dataclass
class SoftRequirement:
    """软性要求"""
    id: str
    category: str  # 分类
    content: str  # 要求内容
    examples: List[str]  # 示例
    created_at: str
    is_active: bool = True


@dataclass
class ReferenceScript:
    """优秀脚本参考"""
    id: str
    title: str  # 标题
    content: str  # 脚本内容
    influencer: str  # 达人名称
    platform: str  # 平台
    style: str  # 风格标签
    performance: Dict[str, int]  # 表现数据（点赞、评论等）
    brief_id: str  # 关联的Brief ID
    created_at: str
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class KnowledgeBase:
    """知识库管理器"""
    
    def __init__(self, data_dir: str = "data/kol_polishing"):
        self.data_dir = data_dir
        self.briefs_file = os.path.join(data_dir, "briefs.json")
        self.requirements_file = os.path.join(data_dir, "requirements.json")
        self.references_file = os.path.join(data_dir, "references.json")
        
        # 确保目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 加载数据
        self.briefs: Dict[str, Brief] = self._load_briefs()
        self.requirements: Dict[str, SoftRequirement] = self._load_requirements()
        self.references: Dict[str, ReferenceScript] = self._load_references()
    
    def _load_briefs(self) -> Dict[str, Brief]:
        """加载Briefs"""
        if os.path.exists(self.briefs_file):
            with open(self.briefs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {k: Brief(**v) for k, v in data.items()}
        return {}
    
    def _load_requirements(self) -> Dict[str, SoftRequirement]:
        """加载软性要求"""
        if os.path.exists(self.requirements_file):
            with open(self.requirements_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {k: SoftRequirement(**v) for k, v in data.items()}
        return {}
    
    def _load_references(self) -> Dict[str, ReferenceScript]:
        """加载优秀脚本"""
        if os.path.exists(self.references_file):
            with open(self.references_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {k: ReferenceScript(**v) for k, v in data.items()}
        return {}
    
    def _save_briefs(self):
        """保存Briefs"""
        with open(self.briefs_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.briefs.items()}, f, ensure_ascii=False, indent=2)
    
    def _save_requirements(self):
        """保存软性要求"""
        with open(self.requirements_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.requirements.items()}, f, ensure_ascii=False, indent=2)
    
    def _save_references(self):
        """保存优秀脚本"""
        with open(self.references_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.references.items()}, f, ensure_ascii=False, indent=2)
    
    # Brief管理
    def add_brief(self, brief: Brief) -> str:
        """添加Brief"""
        self.briefs[brief.id] = brief
        self._save_briefs()
        return brief.id
    
    def get_brief(self, brief_id: str) -> Optional[Brief]:
        """获取Brief"""
        return self.briefs.get(brief_id)
    
    def get_active_brief(self, quarter: str = None) -> Optional[Brief]:
        """获取当前活跃的Brief"""
        active_briefs = [b for b in self.briefs.values() if b.is_active]
        if quarter:
            active_briefs = [b for b in active_briefs if b.quarter == quarter]
        return active_briefs[0] if active_briefs else None
    
    def list_briefs(self) -> List[Brief]:
        """列出所有Briefs"""
        return list(self.briefs.values())
    
    def update_brief(self, brief_id: str, **kwargs) -> bool:
        """更新Brief"""
        if brief_id not in self.briefs:
            return False
        brief = self.briefs[brief_id]
        for key, value in kwargs.items():
            if hasattr(brief, key):
                setattr(brief, key, value)
        brief.updated_at = datetime.now().isoformat()
        self._save_briefs()
        return True
    
    def delete_brief(self, brief_id: str) -> bool:
        """删除Brief"""
        if brief_id in self.briefs:
            del self.briefs[brief_id]
            self._save_briefs()
            return True
        return False
    
    # 软性要求管理
    def add_requirement(self, requirement: SoftRequirement) -> str:
        """添加软性要求"""
        self.requirements[requirement.id] = requirement
        self._save_requirements()
        return requirement.id
    
    def get_requirement(self, req_id: str) -> Optional[SoftRequirement]:
        """获取软性要求"""
        return self.requirements.get(req_id)
    
    def list_requirements(self, category: str = None) -> List[SoftRequirement]:
        """列出软性要求"""
        reqs = list(self.requirements.values())
        if category:
            reqs = [r for r in reqs if r.category == category]
        return reqs
    
    def delete_requirement(self, req_id: str) -> bool:
        """删除软性要求"""
        if req_id in self.requirements:
            del self.requirements[req_id]
            self._save_requirements()
            return True
        return False
    
    # 优秀脚本管理
    def add_reference(self, reference: ReferenceScript) -> str:
        """添加优秀脚本"""
        self.references[reference.id] = reference
        self._save_references()
        return reference.id
    
    def get_reference(self, ref_id: str) -> Optional[ReferenceScript]:
        """获取优秀脚本"""
        return self.references.get(ref_id)
    
    def list_references(self, platform: str = None, style: str = None) -> List[ReferenceScript]:
        """列出优秀脚本"""
        refs = list(self.references.values())
        if platform:
            refs = [r for r in refs if r.platform == platform]
        if style:
            refs = [r for r in refs if r.style == style or style in r.tags]
        return refs
    
    def search_references(self, keyword: str) -> List[ReferenceScript]:
        """搜索优秀脚本"""
        results = []
        for ref in self.references.values():
            if (keyword in ref.title or 
                keyword in ref.content or 
                keyword in ref.influencer or
                keyword in ref.style or
                any(keyword in tag for tag in ref.tags)):
                results.append(ref)
        return results
    
    def delete_reference(self, ref_id: str) -> bool:
        """删除优秀脚本"""
        if ref_id in self.references:
            del self.references[ref_id]
            self._save_references()
            return True
        return False
    
    # 统计信息
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "briefs_count": len(self.briefs),
            "active_briefs_count": len([b for b in self.briefs.values() if b.is_active]),
            "requirements_count": len(self.requirements),
            "references_count": len(self.references),
            "platforms": list(set(r.platform for r in self.references.values())),
            "styles": list(set(r.style for r in self.references.values()))
        }
    
    # 导入导出
    def export_all(self, output_file: str):
        """导出所有数据"""
        data = {
            "briefs": {k: asdict(v) for k, v in self.briefs.items()},
            "requirements": {k: asdict(v) for k, v in self.requirements.items()},
            "references": {k: asdict(v) for k, v in self.references.items()},
            "exported_at": datetime.now().isoformat()
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def import_all(self, input_file: str):
        """导入数据"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "briefs" in data:
            self.briefs = {k: Brief(**v) for k, v in data["briefs"].items()}
            self._save_briefs()
        
        if "requirements" in data:
            self.requirements = {k: SoftRequirement(**v) for k, v in data["requirements"].items()}
            self._save_requirements()
        
        if "references" in data:
            self.references = {k: ReferenceScript(**v) for k, v in data["references"].items()}
            self._save_references()


# 全局知识库实例
knowledge_base = KnowledgeBase()
