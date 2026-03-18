"""
达人风格适配Skill
根据达人风格调整脚本的语言风格
"""

from typing import Dict, Any
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory


class InfluencerStyleAdaptationSkill(BaseSkill):
    """达人风格适配Skill"""
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="influencer_style_adaptation",
            description="根据达人风格调整脚本的语言风格",
            category=SkillCategory.SCRIPT_MODIFICATION,
            version="1.0.0",
            parameters={
                "style_keywords": [],
                "tone": "neutral",
                "adaptation_level": 5
            }
        )
    
    def execute(self, script: str, influencer_style: Dict[str, Any], **kwargs) -> SkillResult:
        """
        执行达人风格适配
        
        Args:
            script: 原始脚本
            influencer_style: 达人风格分析结果
            **kwargs: 其他参数
            
        Returns:
            SkillResult: 适配结果
        """
        try:
            # 根据达人风格调整脚本
            adapted_script = self._adapt_to_style(script, influencer_style)
            
            return SkillResult(
                success=True,
                data={
                    "original_script": script,
                    "adapted_script": adapted_script,
                    "influencer_style": influencer_style,
                    "adaptations": self._get_adaptations(influencer_style)
                },
                metadata={
                    "skill": self.config.name,
                    "version": self.config.version
                }
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=str(e)
            )
    
    def _adapt_to_style(self, script: str, style: Dict[str, Any]) -> str:
        """根据风格调整脚本"""
        adapted = script
        
        # 根据语言基调调整
        tone = style.get("tone", "neutral")
        if tone == "活泼":
            adapted = adapted.replace("。", "～")
            adapted = adapted.replace("，", "，")
        elif tone == "幽默":
            if not adapted.startswith("哈哈，"):
                adapted = "哈哈，" + adapted
        elif tone == "正式":
            # 移除口语化表达
            adapted = adapted.replace("嘛", "")
            adapted = adapted.replace("呢", "")
        
        # 添加风格标记
        adapted = f"[{style.get('style', '适配')}] {adapted}"
        
        return adapted
    
    def _get_adaptations(self, style: Dict[str, Any]) -> list:
        """获取适配内容"""
        adaptations = []
        
        if "tone" in style:
            adaptations.append(f"语言基调：{style['tone']}")
        
        if "style" in style:
            adaptations.append(f"内容风格：{style['style']}")
        
        if "type" in style:
            adaptations.append(f"达人类型：{style['type']}")
        
        return adaptations
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """获取参数schema"""
        return {
            "script": {
                "type": "string",
                "required": True,
                "description": "需要适配的脚本内容"
            },
            "influencer_style": {
                "type": "object",
                "required": True,
                "description": "达人风格分析结果",
                "properties": {
                    "tone": {"type": "string", "description": "语言基调"},
                    "style": {"type": "string", "description": "内容风格"},
                    "type": {"type": "string", "description": "达人类型"}
                }
            },
            "style_keywords": {
                "type": "array",
                "required": False,
                "description": "风格关键词",
                "default": []
            },
            "tone": {
                "type": "string",
                "required": False,
                "description": "语气调整",
                "default": "neutral",
                "enum": ["neutral", "活泼", "幽默", "正式", "感性"]
            },
            "adaptation_level": {
                "type": "integer",
                "required": False,
                "description": "适配程度（1-10）",
                "default": 5,
                "min": 1,
                "max": 10
            }
        }
