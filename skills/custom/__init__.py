"""
Custom skills包初始化文件
"""

from skills.custom.script_optimization import ScriptOptimizationSkill
from skills.custom.influencer_style_adaptation import InfluencerStyleAdaptationSkill
from skills.custom.content_quality_check import ContentQualityCheckSkill
from skills.custom.kol_polishing.parenting.skill import ParentingPolishingSkill
from skills.custom.kol_polishing.tech_review.skill import TechReviewPolishingSkill
from skills.custom.kol_polishing.comparison.skill import ComparisonPolishingSkill

__all__ = [
    'ScriptOptimizationSkill',
    'InfluencerStyleAdaptationSkill',
    'ContentQualityCheckSkill',
    'ParentingPolishingSkill',
    'TechReviewPolishingSkill',
    'ComparisonPolishingSkill'
]
