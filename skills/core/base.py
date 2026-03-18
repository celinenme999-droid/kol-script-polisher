"""
Skills系统 - 基类和接口
定义所有skills的通用接口和基础功能
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SkillCategory(Enum):
    """Skill分类"""
    SCRIPT_MODIFICATION = "脚本修改"
    INFLUENCER_ANALYSIS = "达人分析"
    CONTENT_GENERATION = "内容生成"
    QUALITY_CHECK = "质量检查"
    DATA_PROCESSING = "数据处理"
    CUSTOM = "自定义"


@dataclass
class SkillConfig:
    """Skill配置"""
    name: str
    description: str
    category: SkillCategory
    version: str = "1.0.0"
    enabled: bool = True
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


@dataclass
class SkillResult:
    """Skill执行结果"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseSkill(ABC):
    """Skill基类 - 所有skills必须继承此类"""
    
    def __init__(self, config: SkillConfig):
        self.config = config
        self._validate_config()
    
    @abstractmethod
    def execute(self, **kwargs) -> SkillResult:
        """
        执行skill
        
        Args:
            **kwargs: skill执行所需的参数
            
        Returns:
            SkillResult: 执行结果
        """
        pass
    
    @abstractmethod
    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        获取参数schema（用于前端生成表单）
        
        Returns:
            Dict: 参数schema
        """
        pass
    
    def _validate_config(self):
        """验证配置"""
        if not self.config.name:
            raise ValueError("Skill name is required")
        if not self.config.description:
            raise ValueError("Skill description is required")
    
    def is_enabled(self) -> bool:
        """检查skill是否启用"""
        return self.config.enabled
    
    def enable(self):
        """启用skill"""
        self.config.enabled = True
    
    def disable(self):
        """禁用skill"""
        self.config.enabled = False
    
    def get_info(self) -> Dict[str, Any]:
        """获取skill信息"""
        return {
            "name": self.config.name,
            "description": self.config.description,
            "category": self.config.category.value,
            "version": self.config.version,
            "enabled": self.config.enabled,
            "parameters": self.config.parameters
        }


class SkillManager:
    """Skill管理器 - 管理所有skills的加载、执行和配置"""
    
    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}
        self._skill_registry: Dict[str, type] = {}
    
    def register_skill(self, skill_class: type):
        """
        注册skill类
        
        Args:
            skill_class: skill类（继承自BaseSkill）
        """
        if not issubclass(skill_class, BaseSkill):
            raise ValueError(f"{skill_class.__name__} must inherit from BaseSkill")
        
        # 创建临时实例获取配置
        temp_config = skill_class._get_default_config()
        self._skill_registry[temp_config.name] = skill_class
    
    def load_skill(self, skill_name: str, config: Optional[SkillConfig] = None) -> BaseSkill:
        """
        加载skill
        
        Args:
            skill_name: skill名称
            config: skill配置（可选）
            
        Returns:
            BaseSkill: skill实例
        """
        if skill_name not in self._skill_registry:
            raise ValueError(f"Skill '{skill_name}' not found in registry")
        
        skill_class = self._skill_registry[skill_name]
        
        if config is None:
            config = skill_class._get_default_config()
        
        skill = skill_class(config)
        self._skills[skill_name] = skill
        
        return skill
    
    def get_skill(self, skill_name: str) -> Optional[BaseSkill]:
        """
        获取已加载的skill
        
        Args:
            skill_name: skill名称
            
        Returns:
            BaseSkill: skill实例，如果不存在返回None
        """
        return self._skills.get(skill_name)
    
    def list_skills(self) -> List[Dict[str, Any]]:
        """
        列出所有已注册的skills
        
        Returns:
            List[Dict]: skills信息列表
        """
        skills_info = []
        for skill_name, skill_class in self._skill_registry.items():
            config = skill_class._get_default_config()
            skills_info.append({
                "name": config.name,
                "description": config.description,
                "category": config.category.value,
                "version": config.version,
                "loaded": skill_name in self._skills
            })
        return skills_info
    
    def execute_skill(self, skill_name: str, **kwargs) -> SkillResult:
        """
        执行skill
        
        Args:
            skill_name: skill名称
            **kwargs: skill执行参数
            
        Returns:
            SkillResult: 执行结果
        """
        skill = self.get_skill(skill_name)
        if skill is None:
            skill = self.load_skill(skill_name)
        
        if not skill.is_enabled():
            return SkillResult(
                success=False,
                error=f"Skill '{skill_name}' is disabled"
            )
        
        return skill.execute(**kwargs)
    
    def enable_skill(self, skill_name: str):
        """启用skill"""
        skill = self.get_skill(skill_name)
        if skill:
            skill.enable()
    
    def disable_skill(self, skill_name: str):
        """禁用skill"""
        skill = self.get_skill(skill_name)
        if skill:
            skill.disable()
    
    def get_skill_parameters_schema(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        获取skill的参数schema
        
        Args:
            skill_name: skill名称
            
        Returns:
            Dict: 参数schema，如果skill不存在返回None
        """
        skill = self.get_skill(skill_name)
        if skill is None:
            skill = self.load_skill(skill_name)
        
        return skill.get_parameters_schema()


# 全局skill管理器实例
skill_manager = SkillManager()
