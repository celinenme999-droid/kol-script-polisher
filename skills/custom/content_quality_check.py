"""
内容质量检查Skill
检查脚本的内容质量、合规性和完整性
"""

from typing import Dict, Any, List
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory


class ContentQualityCheckSkill(BaseSkill):
    """内容质量检查Skill"""
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="content_quality_check",
            description="检查脚本的内容质量、合规性和完整性",
            category=SkillCategory.QUALITY_CHECK,
            version="1.0.0",
            parameters={
                "check_items": ["完整性", "合规性", "语言质量"],
                "strict_mode": False,
                "forbidden_words": []
            }
        )
    
    def execute(self, script: str, brief: str = "", **kwargs) -> SkillResult:
        """
        执行内容质量检查
        
        Args:
            script: 脚本内容
            brief: 产品Brief
            **kwargs: 其他参数
            
        Returns:
            SkillResult: 检查结果
        """
        try:
            # 执行各项检查
            checks = self._perform_checks(script, brief)
            
            # 计算总体评分
            overall_score = self._calculate_score(checks)
            
            return SkillResult(
                success=True,
                data={
                    "script": script,
                    "checks": checks,
                    "overall_score": overall_score,
                    "passed": overall_score >= 70,
                    "suggestions": self._get_suggestions(checks)
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
    
    def _perform_checks(self, script: str, brief: str) -> Dict[str, Any]:
        """执行各项检查"""
        checks = {}
        
        # 1. 完整性检查
        checks["completeness"] = self._check_completeness(script, brief)
        
        # 2. 合规性检查
        checks["compliance"] = self._check_compliance(script)
        
        # 3. 语言质量检查
        checks["language_quality"] = self._check_language_quality(script)
        
        # 4. 长度检查
        checks["length"] = self._check_length(script)
        
        return checks
    
    def _check_completeness(self, script: str, brief: str) -> Dict[str, Any]:
        """检查完整性"""
        issues = []
        score = 100
        
        if not script or len(script.strip()) < 10:
            issues.append("脚本内容过短")
            score -= 50
        
        if brief and len(brief) > 0:
            # 检查是否包含brief中的关键词
            brief_keywords = self._extract_keywords(brief)
            missing_keywords = [kw for kw in brief_keywords if kw not in script]
            if missing_keywords:
                issues.append(f"缺少Brief中的关键词：{', '.join(missing_keywords)}")
                score -= 20
        
        return {
            "score": score,
            "passed": score >= 70,
            "issues": issues
        }
    
    def _check_compliance(self, script: str) -> Dict[str, Any]:
        """检查合规性"""
        issues = []
        score = 100
        
        # 检查禁用词
        forbidden_words = ["绝对", "最好", "第一", "顶级"]
        found_forbidden = [word for word in forbidden_words if word in script]
        if found_forbidden:
            issues.append(f"包含禁用词：{', '.join(found_forbidden)}")
            score -= 30
        
        return {
            "score": score,
            "passed": score >= 70,
            "issues": issues
        }
    
    def _check_language_quality(self, script: str) -> Dict[str, Any]:
        """检查语言质量"""
        issues = []
        score = 100
        
        # 检查标点符号
        if script.count("。") == 0:
            issues.append("缺少句号")
            score -= 20
        
        # 检查重复词
        words = script.split()
        if len(words) > 0:
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            repeated = [word for word, count in word_counts.items() if count > 3]
            if repeated:
                issues.append(f"词语重复过多：{', '.join(repeated[:3])}")
                score -= 15
        
        return {
            "score": score,
            "passed": score >= 70,
            "issues": issues
        }
    
    def _check_length(self, script: str) -> Dict[str, Any]:
        """检查长度"""
        length = len(script)
        issues = []
        score = 100
        
        if length < 50:
            issues.append("脚本过短")
            score -= 30
        elif length > 500:
            issues.append("脚本过长")
            score -= 20
        
        return {
            "score": score,
            "passed": score >= 70,
            "issues": issues,
            "length": length
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简化版：提取长度大于2的词
        words = text.split()
        return [word for word in words if len(word) > 2]
    
    def _calculate_score(self, checks: Dict[str, Any]) -> int:
        """计算总体评分"""
        scores = [check["score"] for check in checks.values()]
        return int(sum(scores) / len(scores))
    
    def _get_suggestions(self, checks: Dict[str, Any]) -> List[str]:
        """获取改进建议"""
        suggestions = []
        
        for check_name, check_result in checks.items():
            if not check_result["passed"]:
                for issue in check_result["issues"]:
                    suggestions.append(f"{check_name}: {issue}")
        
        return suggestions
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """获取参数schema"""
        return {
            "script": {
                "type": "string",
                "required": True,
                "description": "需要检查的脚本内容"
            },
            "brief": {
                "type": "string",
                "required": False,
                "description": "产品Brief（用于完整性检查）",
                "default": ""
            },
            "check_items": {
                "type": "array",
                "required": False,
                "description": "检查项目",
                "default": ["完整性", "合规性", "语言质量"]
            },
            "strict_mode": {
                "type": "boolean",
                "required": False,
                "description": "严格模式",
                "default": False
            },
            "forbidden_words": {
                "type": "array",
                "required": False,
                "description": "禁用词列表",
                "default": []
            }
        }
