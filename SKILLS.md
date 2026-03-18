# 🔧 Skills系统文档

## 📖 什么是Skills？

Skills是脚本修改工作流的可扩展功能模块。通过Skills系统，您可以：

- ✅ 扩展工作流功能
- ✅ 复用代码逻辑
- ✅ 自定义处理流程
- ✅ 灵活启用/禁用功能

---

## 🏗️ Skills架构

### 核心组件

```
skills/
├── __init__.py              # Skills包初始化
├── core/                    # 核心模块
│   ├── __init__.py
│   └── base.py             # Skill基类和管理器
└── custom/                  # 自定义skills
    ├── __init__.py
    ├── script_optimization.py
    ├── influencer_style_adaptation.py
    └── content_quality_check.py
```

### Skill基类

所有Skills必须继承自 `BaseSkill`：

```python
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory

class MySkill(BaseSkill):
    """自定义Skill"""
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="my_skill",
            description="Skill描述",
            category=SkillCategory.CUSTOM,
            version="1.0.0"
        )
    
    def execute(self, **kwargs) -> SkillResult:
        # 实现你的逻辑
        return SkillResult(success=True, data={})
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        # 定义参数schema
        return {}
```

---

## 📦 内置Skills

### 1. ScriptOptimizationSkill（脚本优化）

**功能：** 优化脚本的语言表达、结构和流畅度

**参数：**
- `script` (string, required): 需要优化的脚本内容
- `focus_areas` (array, optional): 优化重点领域
- `creativity_level` (integer, optional): 创意程度（1-10）
- `preserve_original` (boolean, optional): 是否保留原始内容

**使用示例：**
```python
from skills import skill_manager

result = skill_manager.execute_skill(
    "script_optimization",
    script="这是原始脚本"
)

if result.success:
    print(result.data["optimized_script"])
```

---

### 2. InfluencerStyleAdaptationSkill（达人风格适配）

**功能：** 根据达人风格调整脚本的语言风格

**参数：**
- `script` (string, required): 需要适配的脚本内容
- `influencer_style` (object, required): 达人风格分析结果
- `style_keywords` (array, optional): 风格关键词
- `tone` (string, optional): 语气调整
- `adaptation_level` (integer, optional): 适配程度（1-10）

**使用示例：**
```python
result = skill_manager.execute_skill(
    "influencer_style_adaptation",
    script="这是原始脚本",
    influencer_style={
        "tone": "活泼",
        "style": "幽默风趣",
        "type": "生活类博主"
    }
)
```

---

### 3. ContentQualityCheckSkill（内容质量检查）

**功能：** 检查脚本的内容质量、合规性和完整性

**参数：**
- `script` (string, required): 需要检查的脚本内容
- `brief` (string, optional): 产品Brief
- `check_items` (array, optional): 检查项目
- `strict_mode` (boolean, optional): 严格模式
- `forbidden_words` (array, optional): 禁用词列表

**使用示例：**
```python
result = skill_manager.execute_skill(
    "content_quality_check",
    script="这是需要检查的脚本",
    brief="产品植入要求"
)

if result.success:
    print(f"评分: {result.data['overall_score']}")
    print(f"建议: {result.data['suggestions']}")
```

---

## 🚀 创建自定义Skill

### 步骤1：创建Skill文件

在 `skills/custom/` 目录下创建新的Python文件，例如 `my_skill.py`：

```python
from typing import Dict, Any
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory

class MyCustomSkill(BaseSkill):
    """我的自定义Skill"""
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="my_custom_skill",
            description="这是一个自定义skill",
            category=SkillCategory.CUSTOM,
            version="1.0.0",
            parameters={
                "param1": "value1",
                "param2": "value2"
            }
        )
    
    def execute(self, **kwargs) -> SkillResult:
        """
        执行skill逻辑
        
        Args:
            **kwargs: skill执行所需的参数
            
        Returns:
            SkillResult: 执行结果
        """
        try:
            # 获取参数
            param1 = kwargs.get("param1", "")
            param2 = kwargs.get("param2", "")
            
            # 实现你的逻辑
            result = self._process_data(param1, param2)
            
            return SkillResult(
                success=True,
                data={
                    "result": result,
                    "processed": True
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
    
    def _process_data(self, param1: str, param2: str) -> str:
        """处理数据"""
        # 实现你的处理逻辑
        return f"处理结果: {param1} + {param2}"
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        """
        获取参数schema（用于前端生成表单）
        
        Returns:
            Dict: 参数schema
        """
        return {
            "param1": {
                "type": "string",
                "required": True,
                "description": "参数1的描述",
                "default": ""
            },
            "param2": {
                "type": "string",
                "required": False,
                "description": "参数2的描述",
                "default": ""
            }
        }
```

### 步骤2：注册Skill

在 `skills/custom/__init__.py` 中导入并注册：

```python
from skills.custom.my_skill import MyCustomSkill

# 在register_all_skills函数中添加
skill_manager.register_skill(MyCustomSkill)
```

### 步骤3：使用Skill

```python
from skills import skill_manager

# 执行skill
result = skill_manager.execute_skill(
    "my_custom_skill",
    param1="值1",
    param2="值2"
)

if result.success:
    print(result.data)
else:
    print(f"错误: {result.error}")
```

---

## 🎯 Skill分类

| 分类 | 说明 | 示例 |
|------|------|------|
| SCRIPT_MODIFICATION | 脚本修改 | 脚本优化、风格适配 |
| INFLUENCER_ANALYSIS | 达人分析 | 风格分析、受众分析 |
| CONTENT_GENERATION | 内容生成 | 标题生成、描述生成 |
| QUALITY_CHECK | 质量检查 | 合规检查、完整性检查 |
| DATA_PROCESSING | 数据处理 | 数据清洗、格式转换 |
| CUSTOM | 自定义 | 用户自定义功能 |

---

## 📊 SkillResult结构

```python
@dataclass
class SkillResult:
    """Skill执行结果"""
    success: bool              # 是否成功
    data: Any = None           # 返回数据
    error: Optional[str] = None # 错误信息
    metadata: Dict[str, Any] = None  # 元数据
```

---

## 🔧 SkillManager API

### 注册Skill

```python
skill_manager.register_skill(MySkillClass)
```

### 加载Skill

```python
skill = skill_manager.load_skill("skill_name")
```

### 执行Skill

```python
result = skill_manager.execute_skill("skill_name", **kwargs)
```

### 列出所有Skills

```python
skills = skill_manager.list_skills()
```

### 启用/禁用Skill

```python
skill_manager.enable_skill("skill_name")
skill_manager.disable_skill("skill_name")
```

### 获取Skill参数Schema

```python
schema = skill_manager.get_skill_parameters_schema("skill_name")
```

---

## 💡 最佳实践

### 1. 错误处理

```python
def execute(self, **kwargs) -> SkillResult:
    try:
        # 你的逻辑
        return SkillResult(success=True, data={})
    except Exception as e:
        return SkillResult(success=False, error=str(e))
```

### 2. 参数验证

```python
def execute(self, **kwargs) -> SkillResult:
    # 验证必需参数
    if "required_param" not in kwargs:
        return SkillResult(
            success=False,
            error="缺少必需参数: required_param"
        )
    
    # 继续处理
    return SkillResult(success=True, data={})
```

### 3. 元数据

```python
return SkillResult(
    success=True,
    data={},
    metadata={
        "skill": self.config.name,
        "version": self.config.version,
        "execution_time": time.time(),
        "parameters": kwargs
    }
)
```

### 4. 日志记录

```python
import logging

logger = logging.getLogger(__name__)

def execute(self, **kwargs) -> SkillResult:
    logger.info(f"执行skill: {self.config.name}")
    logger.debug(f"参数: {kwargs}")
    
    # 你的逻辑
    
    logger.info(f"skill执行完成")
    return SkillResult(success=True, data={})
```

---

## 📚 示例：创建关键词提取Skill

```python
from typing import Dict, Any, List
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory

class KeywordExtractionSkill(BaseSkill):
    """关键词提取Skill"""
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="keyword_extraction",
            description="从脚本中提取关键词",
            category=SkillCategory.DATA_PROCESSING,
            version="1.0.0",
            parameters={
                "max_keywords": 10,
                "min_length": 2
            }
        )
    
    def execute(self, script: str, **kwargs) -> SkillResult:
        try:
            # 提取关键词
            keywords = self._extract_keywords(script)
            
            return SkillResult(
                success=True,
                data={
                    "keywords": keywords,
                    "count": len(keywords)
                }
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))
    
    def _extract_keywords(self, script: str) -> List[str]:
        """提取关键词"""
        import jieba
        words = jieba.cut(script)
        
        # 过滤停用词
        stopwords = {"的", "了", "是", "在", "我", "你", "他"}
        keywords = [
            word for word in words 
            if len(word) >= self.config.parameters["min_length"] 
            and word not in stopwords
        ]
        
        # 统计词频
        from collections import Counter
        word_counts = Counter(keywords)
        
        # 返回前N个关键词
        max_keywords = self.config.parameters["max_keywords"]
        return [word for word, count in word_counts.most_common(max_keywords)]
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "script": {
                "type": "string",
                "required": True,
                "description": "需要提取关键词的脚本"
            },
            "max_keywords": {
                "type": "integer",
                "required": False,
                "description": "最大关键词数量",
                "default": 10
            },
            "min_length": {
                "type": "integer",
                "required": False,
                "description": "关键词最小长度",
                "default": 2
            }
        }
```

---

## ❓ 常见问题

**Q: 如何调试Skill？**
A: 在Skills管理页面中，每个skill都有测试功能，可以直接测试skill的执行。

**Q: Skill可以调用AI模型吗？**
A: 可以！在skill的execute方法中，你可以调用任何AI模型API。

**Q: 如何共享自定义Skill？**
A: 将skill文件分享给其他用户，他们将其放入 `skills/custom/` 目录即可使用。

**Q: Skill的性能如何？**
A: Skill的性能取决于你的实现逻辑。建议在skill中添加性能监控和日志记录。

---

**祝您创建出强大的Skills！** 🎉
