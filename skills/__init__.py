"""
Skills包初始化文件
自动加载所有skills
"""

from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory, skill_manager

# 导入自定义skills
from skills.custom.script_optimization import ScriptOptimizationSkill
from skills.custom.influencer_style_adaptation import InfluencerStyleAdaptationSkill
from skills.custom.content_quality_check import ContentQualityCheckSkill
from skills.custom.kol_polishing import KOLScriptPolishingSkill

# 注册所有skills
def register_all_skills():
    """注册所有skills"""
    skill_manager.register_skill(ScriptOptimizationSkill)
    skill_manager.register_skill(InfluencerStyleAdaptationSkill)
    skill_manager.register_skill(ContentQualityCheckSkill)
    skill_manager.register_skill(KOLScriptPolishingSkill)

# 自动注册
register_all_skills()

__all__ = [
    'BaseSkill',
    'SkillConfig',
    'SkillResult',
    'SkillCategory',
    'skill_manager',
    'ScriptOptimizationSkill',
    'InfluencerStyleAdaptationSkill',
    'ContentQualityCheckSkill',
    'KOLScriptPolishingSkill'
]
