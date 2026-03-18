"""
KOL脚本润色技能
用于润色KOL达人的脚本内容
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory
from skills.custom.kol_polishing.prompts import PROMPT_TEMPLATES
from skills.custom.kol_polishing.knowledge_base import (
    KnowledgeBase, Brief, SoftRequirement, ReferenceScript, knowledge_base
)


class KOLScriptPolishingSkill(BaseSkill):
    """KOL脚本润色技能"""
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="kol_script_polishing",
            description="润色KOL达人脚本，使其口语化、自然、无AI感",
            category=SkillCategory.SCRIPT_MODIFICATION,
            version="1.0.0",
            parameters={
                "polish_mode": "full",  # full, quick, style_transfer, multi_version
                "creativity_level": 5,
                "preserve_original_tone": True,
                "max_reference_count": 3
            }
        )
    
    def __init__(self, config: SkillConfig):
        super().__init__(config)
        self.kb = knowledge_base
    
    def execute(self, **kwargs) -> SkillResult:
        """
        执行脚本润色
        
        Args:
            script: 待润色的脚本内容（必需）
            brief_id: Brief ID（可选，默认使用当前活跃的Brief）
            quarter: 季度（可选，如 "2024Q1"）
            requirement_ids: 软性要求ID列表（可选）
            reference_ids: 优秀脚本ID列表（可选）
            polish_mode: 润色模式（full/quick/style_transfer/multi_version）
            target_style: 目标风格（style_transfer模式需要）
            creativity_level: 创意程度（1-10）
            
        Returns:
            SkillResult: 润色结果
        """
        try:
            # 获取必需参数
            script = kwargs.get("script", "")
            if not script:
                return SkillResult(
                    success=False,
                    error="缺少必需参数：script"
                )
            
            # 获取润色模式
            polish_mode = kwargs.get("polish_mode", self.config.parameters.get("polish_mode", "full"))
            
            # 根据模式执行不同的润色
            if polish_mode == "quick":
                return self._quick_polish(script, kwargs)
            elif polish_mode == "style_transfer":
                return self._style_transfer_polish(script, kwargs)
            elif polish_mode == "multi_version":
                return self._multi_version_polish(script, kwargs)
            else:
                return self._full_polish(script, kwargs)
                
        except Exception as e:
            return SkillResult(
                success=False,
                error=str(e)
            )
    
    def _full_polish(self, script: str, kwargs: Dict) -> SkillResult:
        """完整润色模式"""
        # 获取Brief
        brief_id = kwargs.get("brief_id")
        quarter = kwargs.get("quarter")
        
        if brief_id:
            brief = self.kb.get_brief(brief_id)
        else:
            brief = self.kb.get_active_brief(quarter)
        
        brief_content = self._format_brief(brief) if brief else "暂无Brief信息"
        
        # 获取软性要求
        requirement_ids = kwargs.get("requirement_ids", [])
        requirements = self._get_requirements(requirement_ids)
        
        # 获取优秀脚本参考
        reference_ids = kwargs.get("reference_ids", [])
        max_refs = self.config.parameters.get("max_reference_count", 3)
        references = self._get_references(reference_ids, max_refs)
        
        # 生成提示词
        prompt = PROMPT_TEMPLATES["full_polishing"].format(
            brief=brief_content,
            soft_requirements=requirements,
            reference_scripts=references,
            original_script=script
        )
        
        # 这里应该调用AI模型
        # 简化版：返回提示词和模拟结果
        polished_script = self._simulate_polishing(script)
        
        return SkillResult(
            success=True,
            data={
                "original_script": script,
                "polished_script": polished_script,
                "brief_used": brief_content,
                "requirements_used": requirements,
                "references_used": references,
                "prompt": prompt,
                "mode": "full"
            },
            metadata={
                "skill": self.config.name,
                "version": self.config.version,
                "polish_mode": "full",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _quick_polish(self, script: str, kwargs: Dict) -> SkillResult:
        """快速润色模式"""
        prompt = PROMPT_TEMPLATES["quick_polish"].format(script=script)
        
        # 简化版：模拟润色
        polished_script = self._simulate_polishing(script, quick=True)
        
        return SkillResult(
            success=True,
            data={
                "original_script": script,
                "polished_script": polished_script,
                "prompt": prompt,
                "mode": "quick"
            },
            metadata={
                "skill": self.config.name,
                "version": self.config.version,
                "polish_mode": "quick"
            }
        )
    
    def _style_transfer_polish(self, script: str, kwargs: Dict) -> SkillResult:
        """风格迁移润色模式"""
        target_style = kwargs.get("target_style")
        if not target_style:
            return SkillResult(
                success=False,
                error="style_transfer模式需要提供target_style参数"
            )
        
        tone = kwargs.get("tone", "neutral")
        expressions = kwargs.get("expressions", [])
        audience = kwargs.get("audience", "通用受众")
        
        prompt = PROMPT_TEMPLATES["style_transfer"].format(
            script=script,
            target_style=target_style,
            tone=tone,
            expressions="、".join(expressions) if expressions else "无特殊要求",
            audience=audience
        )
        
        # 简化版：模拟润色
        polished_script = self._simulate_polishing(script, style=target_style)
        
        return SkillResult(
            success=True,
            data={
                "original_script": script,
                "polished_script": polished_script,
                "target_style": target_style,
                "prompt": prompt,
                "mode": "style_transfer"
            },
            metadata={
                "skill": self.config.name,
                "version": self.config.version,
                "polish_mode": "style_transfer"
            }
        )
    
    def _multi_version_polish(self, script: str, kwargs: Dict) -> SkillResult:
        """多版本润色模式"""
        brief_id = kwargs.get("brief_id")
        brief = self.kb.get_brief(brief_id) if brief_id else self.kb.get_active_brief()
        brief_content = self._format_brief(brief) if brief else "暂无Brief信息"
        
        prompt = PROMPT_TEMPLATES["multi_version"].format(
            script=script,
            brief=brief_content
        )
        
        # 简化版：模拟生成多版本
        versions = {
            "活泼俏皮风": self._simulate_polishing(script, style="活泼俏皮"),
            "真诚分享风": self._simulate_polishing(script, style="真诚分享"),
            "专业种草风": self._simulate_polishing(script, style="专业种草")
        }
        
        return SkillResult(
            success=True,
            data={
                "original_script": script,
                "versions": versions,
                "prompt": prompt,
                "mode": "multi_version"
            },
            metadata={
                "skill": self.config.name,
                "version": self.config.version,
                "polish_mode": "multi_version"
            }
        )
    
    def _simulate_polishing(self, script: str, quick: bool = False, style: str = None) -> str:
        """
        模拟润色（简化版）
        实际使用时应该调用AI模型
        """
        # 简单的模拟处理
        polished = script
        
        # 去除明显的书面语
        replacements = {
            "因此": "所以",
            "但是": "不过",
            "然而": "但",
            "此外": "另外",
            "综上所述": "总之",
            "首先": "先说",
            "其次": "然后",
            "最后": "最后呢"
        }
        
        for old, new in replacements.items():
            polished = polished.replace(old, new)
        
        # 添加风格标记
        if style:
            polished = f"[{style}风格] {polished}"
        elif not quick:
            polished = f"[润色后] {polished}"
        
        return polished
    
    def _format_brief(self, brief: Brief) -> str:
        """格式化Brief信息"""
        content = f"""
品牌：{brief.brand}
产品：{brief.product}
季度：{brief.quarter}

核心卖点：
{chr(10).join(f'- {point}' for point in brief.core_points)}

Brief内容：
{brief.content}

禁用词：{', '.join(brief.forbidden_words) if brief.forbidden_words else '无'}
"""
        return content.strip()
    
    def _get_requirements(self, requirement_ids: List[str]) -> str:
        """获取软性要求"""
        if not requirement_ids:
            # 返回所有活跃的软性要求
            reqs = [r for r in self.kb.list_requirements() if r.is_active]
        else:
            reqs = [self.kb.get_requirement(rid) for rid in requirement_ids]
            reqs = [r for r in reqs if r]
        
        if not reqs:
            return "暂无软性要求"
        
        content = []
        for req in reqs:
            content.append(f"- {req.content}")
            if req.examples:
                content.append(f"  示例：{req.examples[0]}")
        
        return "\n".join(content)
    
    def _get_references(self, reference_ids: List[str], max_count: int) -> str:
        """获取优秀脚本参考"""
        if not reference_ids:
            # 返回最近添加的优秀脚本
            refs = self.kb.list_references()[:max_count]
        else:
            refs = [self.kb.get_reference(rid) for rid in reference_ids[:max_count]]
            refs = [r for r in refs if r]
        
        if not refs:
            return "暂无优秀脚本参考"
        
        content = []
        for i, ref in enumerate(refs, 1):
            content.append(f"""
【参考脚本 {i}】
达人：{ref.influencer}
平台：{ref.platform}
风格：{ref.style}
表现：👍{ref.performance.get('likes', 0)} 💬{ref.performance.get('comments', 0)}

{ref.content[:200]}...
""")
        
        return "\n".join(content)
    
    # Brief管理方法
    def add_brief(self, quarter: str, brand: str, product: str, content: str,
                  core_points: List[str], forbidden_words: List[str] = None) -> SkillResult:
        """添加Brief"""
        try:
            brief = Brief(
                id=str(uuid.uuid4()),
                quarter=quarter,
                brand=brand,
                product=product,
                content=content,
                core_points=core_points,
                forbidden_words=forbidden_words or [],
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                is_active=True
            )
            brief_id = self.kb.add_brief(brief)
            
            return SkillResult(
                success=True,
                data={
                    "brief_id": brief_id,
                    "brief": asdict(brief)
                }
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))
    
    # 软性要求管理方法
    def add_requirement(self, category: str, content: str, examples: List[str] = None) -> SkillResult:
        """添加软性要求"""
        try:
            requirement = SoftRequirement(
                id=str(uuid.uuid4()),
                category=category,
                content=content,
                examples=examples or [],
                created_at=datetime.now().isoformat(),
                is_active=True
            )
            req_id = self.kb.add_requirement(requirement)
            
            return SkillResult(
                success=True,
                data={
                    "requirement_id": req_id,
                    "requirement": asdict(requirement)
                }
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))
    
    # 优秀脚本管理方法
    def add_reference(self, title: str, content: str, influencer: str, 
                      platform: str, style: str, performance: Dict[str, int],
                      brief_id: str = None, tags: List[str] = None) -> SkillResult:
        """添加优秀脚本"""
        try:
            reference = ReferenceScript(
                id=str(uuid.uuid4()),
                title=title,
                content=content,
                influencer=influencer,
                platform=platform,
                style=style,
                performance=performance,
                brief_id=brief_id,
                created_at=datetime.now().isoformat(),
                tags=tags or []
            )
            ref_id = self.kb.add_reference(reference)
            
            return SkillResult(
                success=True,
                data={
                    "reference_id": ref_id,
                    "reference": asdict(reference)
                }
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """获取参数schema"""
        return {
            "script": {
                "type": "string",
                "required": True,
                "description": "待润色的脚本内容"
            },
            "polish_mode": {
                "type": "string",
                "required": False,
                "description": "润色模式",
                "default": "full",
                "enum": ["full", "quick", "style_transfer", "multi_version"]
            },
            "brief_id": {
                "type": "string",
                "required": False,
                "description": "Brief ID（不填则使用当前活跃的Brief）"
            },
            "quarter": {
                "type": "string",
                "required": False,
                "description": "季度，如 2024Q1"
            },
            "requirement_ids": {
                "type": "array",
                "required": False,
                "description": "软性要求ID列表"
            },
            "reference_ids": {
                "type": "array",
                "required": False,
                "description": "优秀脚本参考ID列表"
            },
            "target_style": {
                "type": "string",
                "required": False,
                "description": "目标风格（style_transfer模式需要）"
            },
            "creativity_level": {
                "type": "integer",
                "required": False,
                "description": "创意程度（1-10）",
                "default": 5,
                "min": 1,
                "max": 10
            }
        }


# 导入asdict用于序列化
from dataclasses import asdict
