"""
工业营销自动化系统集成测试脚本
"""

from modules.strategy_insight import StrategyInsight
from modules.planning import Planning
from modules.content_creation import ContentCreation
from modules.execution import Execution
from modules.analysis import Analysis

def test_full_workflow():
    print("=== 工业营销自动化系统集成测试开始 ===")
    
    # 模拟输入数据
    client_data = {
        "pain_points": ["设备维护成本高", "生产效率低"],
        "operational_data": {"downtime": 15, "energy_consumption": 1200},
        "critical_issues": ["安全合规"]
    }
    
    competitor_data = {
        "win_cases": [
            {"client": "A公司", "solution": "智能维护系统", "value_prop": "降低维护成本30%"}
        ],
        "marketing_activities": [
            {"channel": "行业展会", "content_type": "技术演示", "success_rate": 0.4}
        ]
    }
    
    market_data = {
        "customer_segments": [
            {"name": "制造业国企", "market_size": 500, "growth_rate": 0.15}
        ],
        "regional_data": [
            {"name": "华东", "demand_level": 8, "competition_index": 3}
        ]
    }
    
    # 第一步：战略洞察
    print("\n1. 执行战略洞察...")
    insight = StrategyInsight()
    insight.process_client_needs(client_data)
    insight.analyze_competition(competitor_data)
    insight.evaluate_market_opportunities(market_data)
    strategy_brief = insight.generate_strategy_brief()
    print("战略简报生成成功:", strategy_brief.keys())
    
    # 第二步：策略计划
    print("\n2. 制定营销计划...")
    planning = Planning()
    planning.match_client_strategies(strategy_brief)
    planning.calculate_pricing_strategies()
    planning.develop_channel_strategies()
    marketing_plan = planning.generate_marketing_plan()
    print("营销计划生成成功:", marketing_plan.keys())
    
    # 第三步：内容创造
    print("\n3. 创建营销内容...")
    content = ContentCreation()
    content.generate_technical_materials(marketing_plan)
    content.generate_sales_scripts()
    marketing_kit = content.package_marketing_kit()
    print("营销弹药包生成成功:", marketing_kit.keys())
    
    # 第四步：执行追踪
    print("\n4. 执行营销活动...")
    execution = Execution()
    execution.publish_to_channels(marketing_kit)
    potential_clients = execution.channel_feedbacks["potential_clients"]
    execution.interact_and_follow_up(potential_clients)
    execution.track_sales_progress(execution.interaction_records)
    print("销售进展跟踪成功:", execution.sales_progress.keys())
    
    # 第五步：复盘分析
    print("\n5. 复盘分析结果...")
    analysis = Analysis()
    sales_data = {
        "potential_clients": potential_clients,
        "channel_feedbacks": execution.channel_feedbacks["feedbacks"],
        "sales_progress": execution.sales_progress,
        "client_strategies": marketing_plan["client_strategies"]
    }
    analysis.analyze_performance(sales_data)
    analysis.identify_success_factors()
    analysis.diagnose_failure_causes()
    knowledge_update = analysis.optimize_knowledge_base()
    print("知识库更新成功:", knowledge_update.keys())
    
    print("\n=== 工业营销自动化系统集成测试完成 ===")

if __name__ == "__main__":
    test_full_workflow()