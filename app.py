"""
脚本修改工作流 - 主应用文件
功能：根据达人风格和产品Brief修改视频脚本
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from typing import List, Dict
import time

# 导入skills系统
from skills import skill_manager
from skills.custom.kol_polishing.kol_skill import KOLPolishingSkill
from ai_client import get_ai_client
from data_loader import DataLoader

# 页面配置
st.set_page_config(
    page_title="脚本修改工作流",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'modified_scripts' not in st.session_state:
    st.session_state.modified_scripts = []
if 'influencer_analysis' not in st.session_state:
    st.session_state.influencer_analysis = None
if 'history' not in st.session_state:
    st.session_state.history = []

# 侧边栏
with st.sidebar:
    st.markdown("## 📝 脚本修改工作流")
    
    # 页面导航
    st.markdown("### 📄 页面")
    page = st.radio(
        "选择页面",
        ["主页", "Skills管理"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    st.markdown("## ⚙️ 设置")
    
    # API配置
    st.markdown("### API配置")
    api_provider = st.selectbox(
        "选择AI模型提供商",
        ["OpenAI", "通义千问", "Claude"],
        index=0
    )
    
    if api_provider == "OpenAI":
        api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        model = st.selectbox("模型", ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)
    elif api_provider == "通义千问":
        api_key = st.text_input("通义千问 API Key", type="password")
        model = st.selectbox("模型", ["qwen-turbo", "qwen-plus", "qwen-max"], index=0)
    else:
        api_key = st.text_input("Claude API Key", type="password")
        model = st.selectbox("模型", ["claude-3-opus", "claude-3-sonnet"], index=0)
    
    st.markdown("---")
    
    # 历史记录
    st.markdown("### 📜 历史记录")
    if st.session_state.history:
        for i, record in enumerate(st.session_state.history[-5:]):
            with st.expander(f"{record['time']} - {record['influencer'][:20]}..."):
                st.text(f"Brief: {record['brief'][:50]}...")
                st.text(f"修改数量: {record['count']}条")
    else:
        st.info("暂无历史记录")

# 页面路由
if page == "主页":
    # 主界面
    st.markdown('<div class="main-header">📝 脚本修改工作流</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>使用说明：</strong><br>
    1. 上传包含原始脚本的Excel文件<br>
    2. 输入达人账号主页链接<br>
    3. 填写产品植入要求/Brief<br>
    4. 点击"开始修改"按钮<br>
    5. 下载修改后的Excel文件
</div>
""", unsafe_allow_html=True)

# 步骤1：上传Excel
st.markdown('<div class="section-header">📤 步骤1：上传脚本Excel</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "选择Excel文件",
    type=['xlsx', 'xls'],
    help="Excel文件应包含脚本内容列"
)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ 成功读取文件，共 {len(df)} 行数据")
        
        # 显示数据预览
        st.markdown("### 数据预览")
        st.dataframe(df.head(10))
        
        # 选择脚本列
        script_column = st.selectbox(
            "选择包含脚本内容的列",
            df.columns.tolist(),
            help="选择包含原始脚本内容的列"
        )
    except Exception as e:
        st.error(f"❌ 读取文件失败：{str(e)}")
        df = None
else:
    df = None

# 步骤2：选择垂类和达人风格
st.markdown('<div class="section-header">👤 步骤2：垂类与达人风格</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox(
        "选择达人垂类",
        ["parenting", "tech_review", "comparison"],
        format_func=lambda x: {
            "parenting": "亲子好物",
            "tech_review": "科技测评",
            "comparison": "竞对横评"
        }.get(x, str(x)),
        help="不同垂类有不同的语言风格要求"
    )

with col2:
    influencer_url = st.text_input(
        "达人账号主页链接（可选）",
        placeholder="例如：https://www.xiaohongshu.com/user/...",
        help="支持小红书、抖音等平台"
    )

# 历史脚本参考（关键：用于学习达人风格）
st.markdown("#### 📝 历史脚本参考（用于学习达人风格）")
reference_script = st.text_area(
    "粘贴达人历史商单脚本",
    placeholder="粘贴达人之前合作的脚本，系统会学习其语言风格...\n\n例如：\n姐妹们！今天给大家分享一个超级好用的...\n宝妈们举个手🙋，这个真的闭眼入！...",
    height=120,
    help="⚠️ 重要：这是保持达人个人风格的关键！系统会从历史脚本中学习达人的表达习惯"
)

# 自定义风格描述
influencer_style = st.text_input(
    "自定义风格描述（可选）",
    placeholder="例如：这是一个科技测评类博主，但她是以【宝妈视角】来做测评的",
    help="如果达人有特殊风格，可以在这里描述"
)

# 显示当前选择的风格摘要
if reference_script or influencer_style:
    st.markdown("#### 🎯 风格识别")
    style_info = []
    if reference_script:
        style_info.append("✅ 已提供历史脚本 - 将学习达人语言风格")
    if influencer_style:
        style_info.append(f"✅ 自定义风格：{influencer_style}")
    st.info("\n".join(style_info))

# 步骤3：产品Brief
st.markdown('<div class="section-header">📋 步骤3：产品植入要求/Brief</div>', unsafe_allow_html=True)

# 自动加载Brief
auto_brief = DataLoader.get_brief(category)
brief_filename = DataLoader.get_brief_filename(category)

col1, col2 = st.columns([3, 1])
with col1:
    st.caption(f"📄 已加载Brief: {brief_filename}")
with col2:
    if st.button("🔄 刷新Brief", key="refresh_brief"):
        st.rerun()

brief = st.text_area(
    "产品植入要求（已自动加载对应垂类Brief，可编辑补充）",
    value=auto_brief if auto_brief else "",
    placeholder="例如：\n1. 产品需要在视频前30秒出现\n2. 口播词要自然，不要生硬\n3. 需要展示产品使用场景\n4. 强调产品的核心卖点...",
    height=150,
    help="详细描述产品植入的具体要求和限制"
)

# 软性要求
auto_soft_req = DataLoader.get_soft_requirements()
soft_req_filename = DataLoader.get_requirements_filename()

with st.expander("📝 软性要求（点击展开/编辑）", expanded=False):
    st.caption(f"📄 已加载: {soft_req_filename}")
    soft_requirements = st.text_area(
        "软性要求",
        value=auto_soft_req if auto_soft_req else "",
        height=100,
        key="soft_requirements_input"
    )

# 步骤4：修改设置
st.markdown('<div class="section-header">⚙️ 步骤4：修改设置</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    creativity_level = st.slider(
        "创意程度",
        min_value=1,
        max_value=10,
        value=5,
        help="1=保守修改，10=大胆创新"
    )

with col2:
    tone_adjustment = st.selectbox(
        "语气调整",
        ["保持原样", "更活泼", "更正式", "更幽默", "更感性"],
        index=0
    )

with col3:
    length_control = st.selectbox(
        "长度控制",
        ["保持原长度", "适当缩短", "适当延长"],
        index=0
    )

# 步骤5：开始修改
st.markdown('<div class="section-header">🚀 步骤5：开始修改</div>', unsafe_allow_html=True)

if st.button("✨ 开始修改脚本", type="primary", use_container_width=True):
    if df is None:
        st.error("❌ 请先上传Excel文件")
    elif 'script_column' not in dir():
        st.error("❌ 请选择脚本列")
    else:
        skill = KOLPolishingSkill()
        ai_client = get_ai_client(api_provider, api_key if 'api_key' in dir() else None, model)
        
        if not api_key:
            st.warning("⚠️ 未配置API Key，将使用模拟模式运行（结果仅为占位符）")
        
        with st.spinner("正在修改脚本，请稍候..."):
            progress_bar = st.progress(0)
            
            modified_scripts = []
            style_analysis_result = None
            
            for i, row in df.iterrows():
                original_script = str(row[script_column])
                
                result = skill.execute(
                    script=original_script,
                    category=category,
                    influencer_url=influencer_url if influencer_url else None,
                    reference_script=reference_script if reference_script else None,
                    influencer_style=influencer_style if influencer_style else None,
                    brief=brief if brief else None,
                    soft_requirements=soft_requirements if 'soft_requirements' in dir() else None,
                    ai_client=ai_client
                )
                
                if result.success:
                    modified_script = result.data.get("polished_script", original_script)
                    if style_analysis_result is None:
                        style_analysis_result = result.data.get("style_analysis")
                else:
                    modified_script = f"[润色失败] {original_script}"
                
                modified_scripts.append(modified_script)
                progress_bar.progress((i + 1) / len(df))
            
            st.session_state.modified_scripts = modified_scripts
            
            st.session_state.history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "influencer": influencer_url or "未提供链接",
                "brief": brief[:50] if brief else "",
                "count": len(modified_scripts)
            })
            
            st.success(f"✅ 修改完成！共修改 {len(modified_scripts)} 条脚本")
            
            if style_analysis_result:
                st.markdown("### 🎯 达人风格分析")
                st.info(f"**垂类**: {style_analysis_result.get('category_name', '')}\n\n"
                       f"**风格来源**: {style_analysis_result.get('analysis_source', '')}\n\n"
                       f"**识别到的表达**: {', '.join(style_analysis_result.get('extracted_features', {}).get('common_expressions', []))}")
            
            st.markdown("### 📝 修改结果预览")
            for i in range(min(3, len(modified_scripts))):
                with st.expander(f"脚本 {i+1}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**原始脚本：**")
                        st.text(str(df.iloc[i][script_column])[:500])
                    with col2:
                        st.markdown("**修改后脚本：**")
                        st.text(modified_scripts[i][:500])

# 步骤6：下载结果
if st.session_state.modified_scripts and df is not None:
    st.markdown('<div class="section-header">📥 步骤6：下载结果</div>', unsafe_allow_html=True)
    
    # 创建结果DataFrame
    result_df = df.copy()
    result_df['修改后脚本'] = st.session_state.modified_scripts
    
    # 生成Excel文件
    output_path = f"output/修改后脚本_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    os.makedirs("output", exist_ok=True)
    result_df.to_excel(output_path, index=False)
    
    # 下载按钮
    with open(output_path, 'rb') as f:
        st.download_button(
            label="📥 下载修改后的Excel",
            data=f,
            file_name=f"修改后脚本_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    # 显示统计信息
    st.markdown("### 📊 修改统计")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总脚本数", len(result_df))
    with col2:
        st.metric("修改成功", len(st.session_state.modified_scripts))
    with col3:
        avg_length = sum(len(s) for s in st.session_state.modified_scripts) / len(st.session_state.modified_scripts)
        st.metric("平均字数", f"{avg_length:.0f}")

elif page == "Skills管理":
    # Skills管理页面
    st.markdown('<div class="main-header">🔧 Skills管理</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>Skills说明：</strong><br>
        Skills是可复用的功能模块，可以扩展工作流的功能。您可以启用/禁用skills，查看skill详情，或创建自定义skills。
    </div>
    """, unsafe_allow_html=True)
    
    # 列出所有skills
    st.markdown("### 📋 已注册的Skills")
    skills_list = skill_manager.list_skills()
    
    if skills_list:
        for skill_info in skills_list:
            with st.expander(f"🔹 {skill_info['name']} - {skill_info['description']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("分类", skill_info['category'])
                with col2:
                    st.metric("版本", skill_info['version'])
                with col3:
                    status = "✅ 已加载" if skill_info['loaded'] else "⭕ 未加载"
                    st.metric("状态", status)
                
                # 启用/禁用按钮
                skill = skill_manager.get_skill(skill_info['name'])
                if skill:
                    if skill.is_enabled():
                        if st.button(f"禁用 {skill_info['name']}", key=f"disable_{skill_info['name']}"):
                            skill_manager.disable_skill(skill_info['name'])
                            st.rerun()
                    else:
                        if st.button(f"启用 {skill_info['name']}", key=f"enable_{skill_info['name']}"):
                            skill_manager.enable_skill(skill_info['name'])
                            st.rerun()
                
                # 查看参数schema
                if st.button(f"查看参数schema", key=f"schema_{skill_info['name']}"):
                    schema = skill_manager.get_skill_parameters_schema(skill_info['name'])
                    st.json(schema)
                
                # 测试skill
                st.markdown("#### 🧪 测试Skill")
                test_script = st.text_area(
                    "测试脚本",
                    value="这是一个测试脚本，用于测试skill的功能。",
                    key=f"test_script_{skill_info['name']}"
                )
                if st.button(f"运行测试", key=f"test_{skill_info['name']}"):
                    with st.spinner("正在测试..."):
                        result = skill_manager.execute_skill(skill_info['name'], script=test_script)
                        if result.success:
                            st.success("✅ 测试成功")
                            st.json(result.data)
                        else:
                            st.error(f"❌ 测试失败：{result.error}")
    else:
        st.info("暂无已注册的skills")
    
    # 创建自定义skill
    st.markdown("---")
    st.markdown("### ➕ 创建自定义Skill")
    
    with st.expander("查看Skill模板"):
        st.code("""
from skills.core.base import BaseSkill, SkillConfig, SkillResult, SkillCategory

class MyCustomSkill(BaseSkill):
    \"\"\"自定义Skill\"\"\"
    
    @classmethod
    def _get_default_config(cls) -> SkillConfig:
        return SkillConfig(
            name="my_custom_skill",
            description="我的自定义skill描述",
            category=SkillCategory.CUSTOM,
            version="1.0.0"
        )
    
    def execute(self, **kwargs) -> SkillResult:
        # 实现你的逻辑
        return SkillResult(
            success=True,
            data={"result": "执行成功"}
        )
    
    def get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "param1": {
                "type": "string",
                "required": True,
                "description": "参数1"
            }
        }
        """, language="python")
    
    st.info("💡 提示：将自定义skill文件保存到 `skills/custom/` 目录下，系统会自动加载")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    💡 提示：首次使用建议先测试1-2条脚本，确认效果后再批量处理
</div>
""", unsafe_allow_html=True)
