"""
脚本优化Skill
优化脚本的语言表达、结构和流畅度
"""

from typing import Dict, Any
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory


class ScriptOptimizationSkill(BaseSkill):
    """脚本优化Skill"""
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="script_optimization",
            description="优化脚本的语言表达、结构和流畅度",
            category=SkillCategory.SCRIPT_MODIFICATION,
            version="1.0.0",
            parameters={
                "focus_areas": ["语言表达", "结构优化", "流畅度"],
                "creativity_level": 5,
                "preserve_original": True
            }
        )
    
    def execute(self, script: str, **kwargs) -> SkillResult:
        """
        执行脚本优化
        
        Args:
            script: 原始脚本
            **kwargs: 其他参数
            
        Returns:
            SkillResult: 优化结果
        """
        try:
            # 这里应该调用AI模型进行优化
            # 简化版：添加一些优化标记
            optimized_script = self._optimize_script(script)
            
            return SkillResult(
                success=True,
                data={
                    "original_script": script,
                    "optimized_script": optimized_script,
                    "changes": self._get_changes(script, optimized_script)
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
    
    def _optimize_script(self, script: str) -> str:
        """优化脚本（简化版）"""
        # 这里应该调用AI模型
        # 简化版：添加一些优化
        optimized = script
        
        # 移除多余的空格
        optimized = " ".join(optimized.split())
        
        # 添加优化标记
        if not optimized.startswith("[优化后]"):
            optimized = f"[优化后] {optimized}"
        
        return optimized
    
    def _get_changes(self, original: str, optimized: str) -> list:
        """获取修改内容"""
        changes = []
        
        if len(optimized) != len(original):
            changes.append(f"长度变化：{len(original)} → {len(optimized)}")
        
        if "[优化后]" in optimized:
            changes.append("添加了优化标记")
        
        return changes
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """获取参数schema"""
        return {
            "script": {
                "type": "string",
                "required": True,
                "description": "需要优化的脚本内容"
            },
            "focus_areas": {
                "type": "array",
                "required": False,
                "description": "优化重点领域",
                "default": ["语言表达", "结构优化", "流畅度"]
            },
            "creativity_level": {
                "type": "integer",
                "required": False,
                "description": "创意程度（1-10）",
                "default": 5,
                "min": 1,
                "max": 10
            },
            "preserve_original": {
                "type": "boolean",
                "required": False,
                "description": "是否保留原始内容",
                "default": True
            }
        }
