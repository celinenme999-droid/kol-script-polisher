# KOL脚本润色技能包

## 项目说明

本项目包含三个垂类的KOL达人脚本润色技能：
- **亲子好物** (`parenting`) - 轻松活泼、温馨有爱
- **科技测评** (`tech_review`) - 专业严谨、有技术感
- **竞对横评** (`comparison`) - 客观专业、对比分析

## 目录结构

```
skills/custom/kol_polishing/
├── parenting/
│   └── skill.py          # 亲子好物润色技能
├── tech_review/
│   └── skill.py          # 科技测评润色技能
├── comparison/
│   └── skill.py          # 竞对横评润色技能
├── knowledge_base.py     # 知识库管理
└── prompts.py            # Prompt模板

data/kol_polishing/
├── briefs/
│   ├── parenting/         # 亲子好物Brief
│   ├── tech_review/       # 科技测评Brief
│   └── comparison/        # 竞对横评Brief
├── references/
│   ├── parenting/         # 亲子好物参考脚本
│   ├── tech_review/       # 科技测评参考脚本
│   └── comparison/        # 竞对横评参考脚本
└── requirements/
    └── requirements.json   # 通用软性要求
```

## 数据文件说明

### Brief文件
- **来源**: `~/Desktop/try/knowledge_base/Brief-*.pdf`
- **分类**: 
  - 亲子教育&好物推荐&科技测评 → `parenting`
  - 竞对横评 -> `comparison`

### 叺参考脚本
- **来源**: `~/Desktop/try/knowledge_base/参考脚本-*.xlsx`
- **分类**:
  - 亲子教育KOL -> `parenting`
  - 好物推荐KOL -> `parenting`
  - 科技测评KOL -> `tech_review`
  - 竞对横评KOL -> `comparison`

### 软性要求
- **来源**: `~/Desktop/try/knowledge_base/通用软性要求.docx`
- **位置**: `data/kol_polishing/requirements/requirements.json`

## 使用方法

### 1. 亲子好物润色

```python
from skills.custom.kol_polishing.parenting.skill import ParentingPolishingSkill
from skills.core.base import skill_manager

# 方式1: 直接使用技能类
skill = ParentingPolishingSkill(ParentingPolishingSkill._get_default_config())
result = skill.execute(script="原始脚本内容")

# 方式2: 通过skill_manager
result = skill_manager.execute_skill(
    "parenting_polishing",
    script="原始脚本内容"
)
```

### 2. 科技测评润色

```python
from skills.custom.kol_polishing.tech_review.skill import TechReviewPolishingSkill

skill = TechReviewPolishingSkill(TechReviewPolishingSkill._get_default_config())
result = skill.execute(script="原始脚本内容")
```

### 3. 竞对横评润色

```python
from skills.custom.kol_polishing.comparison.skill import ComparisonPolishingSkill

skill = ComparisonPolishingSkill(ComparisonPolishingSkill._get_default_config())
result = skill.execute(script="原始脚本内容")
```

## 三种垂类风格对比

| 特征 | 亲子好物 | 科技测评 | 竞对横评 |
|------|----------|----------|----------|
| **语言基调** | 活泼俏皮 | 专业严谨 | 客观专业 |
| **适合场景** | 家庭日常、亲子互动 | 产品评测、技术解析 | 产品对比、优缺点分析 |
| **称呼方式** | 宝妈们/姐妹们 | 各位/大家 | 大家/咱们 |
| **情绪表达** | 温馨有爱 | 理性客观 | 理性分析 |
| **结尾风格** | 真诚推荐 | 专业结论 | 对比总结 |

## 润色要求

### 通用要求
1. 口语化表达，自然无AI感
2. 语序通顺，无语病
3. 符合Brief要求
4. 避免禁用词

5. 保留核心信息

### 各垂类特殊要求
- **亲子好物**: 增加亲子互动场景、使用语气词
- **科技测评**: 专业术语准确、技术点清晰
- **竞对横评**: 对比客观、优缺点分明

