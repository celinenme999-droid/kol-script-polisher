"""
KOL脚本润色技能 - 统一入口
支持3种垂类：亲子好物、科技测评、竞对横评
支持达人风格分析和参考
"""

from typing import Dict, Any, Optional
from datetime import datetime
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory


class KOLPolishingSkill(BaseSkill):
    """KOL脚本润色技能 - 支持达人风格分析和参考"""
    
    # 三种垂类的默认风格
    CATEGORY_STYLES = {
        "parenting": {
            "name": "亲子好物",
            "default_tone": "轻松活泼、温馨有爱",
            "default_expressions": ["姐妹们", "宝妈们", "真心推荐", "赶紧冲"],
            "forbidden": ["绝对", "最好", "第一", "顶级"]
        },
        "tech_review": {
            "name": "科技测评",
            "default_tone": "专业严谨、客观详实",
            "default_expressions": ["各位", "大家", "实测", "数据显示"],
            "forbidden": ["绝对", "最好", "第一", "顶级"]
        },
        "comparison": {
            "name": "竞对横评",
            "default_tone": "客观对比、专业分析",
            "default_expressions": ["大家", "咱们", "对比来看", "综合来看"],
            "forbidden": ["绝对", "最好", "第一", "顶级"]
        }
    }
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="kol_polishing",
            description="KOL脚本润色 - 支持达人风格分析，保持原稿特色",
            category=SkillCategory.SCRIPT_MODIFICATION,
            version="2.0.0",
        )
    
    def __init__(self, config: SkillConfig = None):  # type: ignore
        if config is None:
            config = self._get_default_config()
        super().__init__(config)
    
    def execute(self, **kwargs) -> SkillResult:
        """执行润色"""
        script = kwargs.get("script", "")
        category = kwargs.get("category", "parenting")
        
        # 达人风格参考（可选）
        influencer_url = kwargs.get("influencer_url")
        reference_script = kwargs.get("reference_script")
        influencer_style = kwargs.get("influencer_style")
        
        # Brief和软性要求
        brief = kwargs.get("brief", "")
        soft_requirements = kwargs.get("soft_requirements", "")
        
        # AI客户端（可选，如果不提供则使用模拟模式）
        ai_client = kwargs.get("ai_client")
        
        if not script:
            return SkillResult(success=False, error="缺少script参数")
        
        # 分析达人风格
        style_analysis = self._analyze_influencer_style(
            influencer_url=influencer_url,
            reference_script=reference_script,
            influencer_style=influencer_style,
            category=category
        )
        
        # 生成润色提示词
        prompt = self._generate_prompt(
            script=script,
            category=category,
            style_analysis=style_analysis,
            brief=brief,
            soft_requirements=soft_requirements
        )
        
        # 执行润色
        if ai_client is not None:
            polished = ai_client.generate(prompt)
        else:
            polished = self._mock_polish(script, style_analysis)
        
        return SkillResult(
            success=True,
            data={
                "original_script": script,
                "polished_script": polished,
                "category": category,
                "style_analysis": style_analysis,
                "prompt": prompt
            },
            metadata={
                "skill": self.config.name,
                "version": self.config.version,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def _analyze_influencer_style(
        self,
        influencer_url: Optional[str],
        reference_script: Optional[str],
        influencer_style: Optional[str],
        category: str
    ) -> Dict[str, Any]:
        """分析达人风格"""
        
        # 获取该垂类的默认风格
        default_style = self.CATEGORY_STYLES.get(category, self.CATEGORY_STYLES["parenting"])
        
        style = {
            "category": category,
            "category_name": default_style["name"],
            "tone": default_style["default_tone"],
            "expressions": list(default_style["default_expressions"]),
            "forbidden": list(default_style["forbidden"]),
            "analysis_source": "默认风格"
        }
        
        # 如果提供了预设风格描述
        if influencer_style:
            style["custom_style"] = influencer_style
            style["analysis_source"] = "用户预设"
        
        # 如果提供了达人主页链接
        if influencer_url:
            style["influencer_url"] = influencer_url
            style["analysis_source"] = "主页分析（需要MCP支持）"
        
        # 如果提供了历史商单脚本
        if reference_script:
            ref_preview = reference_script[:500] + "..." if len(reference_script) > 500 else reference_script
            style["reference_script"] = ref_preview
            style["analysis_source"] = "历史脚本参考"
            
            # 从历史脚本中提取风格特征
            style["extracted_features"] = self._extract_style_features(reference_script)
        
        return style
    
    def _extract_style_features(self, script: str) -> Dict[str, Any]:
        """从历史脚本中提取风格特征"""
        features = {
            "common_expressions": [],
            "tone_markers": [],
            "sentence_patterns": []
        }
        
        # 检测常见表达
        expressions_to_check = [
            "姐妹们", "宝妈们", "各位", "大家", "咱们",
            "真心推荐", "赶紧冲", "闭眼入", "强烈安利",
            "实测", "数据显示", "对比来看", "综合来看"
        ]
        
        for expr in expressions_to_check:
            if expr in script:
                features["common_expressions"].append(expr)
        
        # 检测语气标记
        tone_markers = ["！", "？", "～", "哈", "嘛", "呢", "啦"]
        for marker in tone_markers:
            count = script.count(marker)
            if count > 0:
                features["tone_markers"].append(f"{marker}({count}次)")
        
        return features
    
    def _generate_prompt(
        self,
        script: str,
        category: str,
        style_analysis: Dict,
        brief: str,
        soft_requirements: str
    ) -> str:
        """生成润色提示词"""
        
        # 预处理变量，避免在f-string中使用复杂表达式
        category_name = style_analysis.get("category_name", "")
        tone = style_analysis.get("tone", "")
        expressions = style_analysis.get("expressions", [])
        expressions_str = "、".join(expressions) if expressions else "无"
        analysis_source = style_analysis.get("analysis_source", "")
        forbidden = style_analysis.get("forbidden", [])
        forbidden_str = "、".join(forbidden) if forbidden else "无"
        
        brief_text = brief if brief else "暂无Brief"
        soft_text = soft_requirements if soft_requirements else "暂无软性要求"
        
        # 参考脚本部分
        ref_script_part = ""
        if style_analysis.get("reference_script"):
            ref_script_part = f"""
## 达人历史脚本参考（学习风格）
{style_analysis.get('reference_script', '无')}
"""
        
        # 自定义风格部分
        custom_style_part = ""
        if style_analysis.get("custom_style"):
            custom_style_part = f"""
## 自定义风格要求
{style_analysis.get('custom_style', '')}
"""
        
        prompt = f"""
你是一位专业的短视频脚本润色专家。请润色以下达人脚本。

## 重要原则
1. **保持达人原稿的风格和特色** - 不要改变达人的个人风格
2. **只做语言优化** - 让表达更口语化、自然流畅
3. **保留核心信息和卖点** - 不要遗漏重要内容
4. **符合Brief要求** - 确保产品植入要点完整

## 达人风格分析
- 垂类：{category_name}
- 语言基调：{tone}
- 常用表达：{expressions_str}
- 风格来源：{analysis_source}

{ref_script_part}
{custom_style_part}
## Brief要求
{brief_text}

## 软性要求
{soft_text}

## 待润色脚本
{script}

## 润色要求
1. 保持达人原有的语言风格和个人特色
2. 确保口语化、自然流畅、无语病
3. 保留所有核心信息和产品卖点
4. 不要过度改变原文的表达方式
5. 避免使用禁用词：{forbidden_str}

请直接输出润色后的脚本，不需要额外解释。
"""
        return prompt
    
    def _mock_polish(self, script: str, style_analysis: Dict) -> str:
        """模拟润色（实际应调用AI模型）"""
        category_name = style_analysis.get("category_name", "")
        return f"[{category_name}润色-保持达人风格]\n\n{script}"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "script": {
                "type": "string",
                "required": True,
                "description": "待润色的达人脚本内容"
            },
            "category": {
                "type": "string",
                "required": False,
                "description": "达人垂类",
                "default": "parenting",
                "enum": ["parenting", "tech_review", "comparison"]
            },
            "influencer_url": {
                "type": "string",
                "required": False,
                "description": "达人社交媒体主页链接（用于分析风格）"
            },
            "reference_script": {
                "type": "string",
                "required": False,
                "description": "达人历史商单脚本（用于学习风格）"
            },
            "influencer_style": {
                "type": "string",
                "required": False,
                "description": "达人风格描述（如：宝妈视角、科技宅、幽默风趣等）"
            },
            "brief": {
                "type": "string",
                "required": False,
                "description": "本季Brief要求"
            },
            "soft_requirements": {
                "type": "string",
                "required": False,
                "description": "软性要求"
            },
            "ai_client": {
                "type": "object",
                "required": False,
                "description": "AI客户端实例（可选，如不提供则使用模拟模式）"
            }
        }
