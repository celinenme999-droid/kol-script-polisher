"""
KOL脚本润色技能 - 使用示例
演示如何使用这个技能
"""

from skills import skill_manager
from skills.custom.kol_polishing import KOLScriptPolishingSkill, knowledge_base


def example_1_quick_polish():
    """示例1：快速润色"""
    print("=" * 50)
    print("示例1：快速润色")
    print("=" * 50)
    
    result = skill_manager.execute_skill(
        "kol_script_polishing",
        script="""
        大家好，今天我给大家推荐一款非常好用的面膜。
        这个面膜含有天然成分，对皮肤很好。
        用了之后皮肤变得很水润。
        希望大家喜欢，谢谢观看。
        """,
        polish_mode="quick"
    )
    
    if result.success:
        print("原始脚本：")
        print(result.data["original_script"])
        print("\n润色后脚本：")
        print(result.data["polished_script"])
    else:
        print(f"错误：{result.error}")


def example_2_add_brief():
    """示例2：添加Brief"""
    print("\n" + "=" * 50)
    print("示例2：添加Brief")
    print("=" * 50)
    
    skill = KOLScriptPolishingSkill(KOLScriptPolishingSkill._get_default_config())
    
    result = skill.add_brief(
        quarter="2024Q1",
        brand="某某护肤品牌",
        product="氨基酸洁面乳",
        content="""
        1. 强调产品的温和配方
        2. 突出氨基酸成分的清洁力
        3. 适合所有肤质使用
        4. 价格亲民，性价比高
        """,
        core_points=["温和配方", "氨基酸成分", "全肤质适用", "性价比高"],
        forbidden_words=["绝对", "最好", "第一", "顶级", "必买"]
    )
    
    if result.success:
        print(f"Brief添加成功！ID: {result.data['brief_id']}")
        print(f"品牌: {result.data['brief']['brand']}")
        print(f"产品: {result.data['brief']['product']}")
    else:
        print(f"错误：{result.error}")


def example_3_add_requirement():
    """示例3：添加软性要求"""
    print("\n" + "=" * 50)
    print("示例3：添加软性要求")
    print("=" * 50)
    
    skill = KOLScriptPolishingSkill(KOLScriptPolishingSkill._get_default_config())
    
    result = skill.add_requirement(
        category="语言风格",
        content="语言要活泼俏皮，像闺蜜聊天一样",
        examples=[
            "姐妹们，这款真的绝了！",
            "我跟你们说，我最近发现一个宝藏产品...",
            "笑死，这个价格也太香了吧！"
        ]
    )
    
    if result.success:
        print(f"软性要求添加成功！ID: {result.data['requirement_id']}")
        print(f"分类: {result.data['requirement']['category']}")
        print(f"内容: {result.data['requirement']['content']}")
    else:
        print(f"错误：{result.error}")


def example_4_add_reference():
    """示例4：添加优秀脚本"""
    print("\n" + "=" * 50)
    print("示例4：添加优秀脚本")
    print("=" * 50)
    
    skill = KOLScriptPolishingSkill(KOLScriptPolishingSkill._get_default_config())
    
    result = skill.add_reference(
        title="敏感肌护肤分享",
        content="""
        姐妹们，作为一个敏感肌患者，我真的太懂那种痛苦了...
        换季脸红、用错产品就过敏，简直是噩梦！
        
        直到我遇到了这款洁面，真的绝了！
        它的氨基酸配方超级温和，洗完脸一点都不紧绷。
        用了一个月，我的泛红真的改善了很多！
        
        而且价格才几十块，学生党也能轻松入手。
        真心推荐给所有敏感肌姐妹们！
        """,
        influencer="小红书达人A",
        platform="小红书",
        style="真诚分享",
        performance={"likes": 5000, "comments": 300, "shares": 150},
        tags=["敏感肌", "护肤", "洁面", "真实体验"]
    )
    
    if result.success:
        print(f"优秀脚本添加成功！ID: {result.data['reference_id']}")
        print(f"标题: {result.data['reference']['title']}")
        print(f"达人: {result.data['reference']['influencer']}")
    else:
        print(f"错误：{result.error}")


def example_5_full_polish():
    """示例5：完整润色"""
    print("\n" + "=" * 50)
    print("示例5：完整润色（使用Brief、软性要求、优秀脚本）")
    print("=" * 50)
    
    result = skill_manager.execute_skill(
        "kol_script_polishing",
        script="""
        大家好，今天给大家推荐一款洁面产品。
        这个产品是氨基酸配方的，很温和。
        用了之后皮肤不紧绷，很舒服。
        价格也不贵，性价比挺高的。
        希望大家喜欢，记得点赞关注哦。
        """,
        polish_mode="full",
        quarter="2024Q1",
        creativity_level=6
    )
    
    if result.success:
        print("原始脚本：")
        print(result.data["original_script"])
        print("\n润色后脚本：")
        print(result.data["polished_script"])
        print("\n使用的Brief：")
        print(result.data["brief_used"][:200] + "...")
    else:
        print(f"错误：{result.error}")


def example_6_multi_version():
    """示例6：多版本生成"""
    print("\n" + "=" * 50)
    print("示例6：多版本生成")
    print("=" * 50)
    
    result = skill_manager.execute_skill(
        "kol_script_polishing",
        script="""
        今天给大家分享一款好用的面膜。
        这个面膜补水效果很好。
        价格也便宜，推荐给大家。
        """,
        polish_mode="multi_version"
    )
    
    if result.success:
        for style, script in result.data["versions"].items():
            print(f"\n【{style}】")
            print(script)
    else:
        print(f"错误：{result.error}")


def example_7_check_stats():
    """示例7：查看知识库统计"""
    print("\n" + "=" * 50)
    print("示例7：知识库统计")
    print("=" * 50)
    
    stats = knowledge_base.get_stats()
    print(f"Brief数量: {stats['briefs_count']}")
    print(f"活跃Brief数量: {stats['active_briefs_count']}")
    print(f"软性要求数量: {stats['requirements_count']}")
    print(f"优秀脚本数量: {stats['references_count']}")
    print(f"平台: {stats['platforms']}")
    print(f"风格: {stats['styles']}")


def main():
    """运行所有示例"""
    print("🎬 KOL脚本润色技能 - 使用示例")
    print("=" * 50)
    
    # 运行示例
    example_1_quick_polish()
    example_2_add_brief()
    example_3_add_requirement()
    example_4_add_reference()
    example_5_full_polish()
    example_6_multi_version()
    example_7_check_stats()
    
    print("\n" + "=" * 50)
    print("✅ 所有示例运行完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
