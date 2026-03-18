"""
KOL脚本润色技能包
"""

from skills.custom.kol_polishing.skill import KOLScriptPolishingSkill
from skills.custom.kol_polishing.knowledge_base import (
    KnowledgeBase, Brief, SoftRequirement, ReferenceScript, knowledge_base
)
from skills.custom.kol_polishing.prompts import PROMPT_TEMPLATES

__all__ = [
    'KOLScriptPolishingSkill',
    'KnowledgeBase',
    'Brief',
    'SoftRequirement',
    'ReferenceScript',
    'knowledge_base',
    'PROMPT_TEMPLATES'
]
