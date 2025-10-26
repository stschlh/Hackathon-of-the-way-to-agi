"""
工业战略洞察与定向模块
实现客户需求挖掘、竞争情报洞察和市场机会研判功能
"""

class StrategyInsight:
    def __init__(self):
        self.client_data = None
        self.competitor_data = None
        self.market_data = None
    
    def process_client_needs(self, client_data):
        """
        工业客户需求挖掘
        输入: 企业工业属性数据
        输出: 工业客户需求清单
        """
        self.client_data = client_data
        
        # 分析硬性需求（明确表达的需求）
        explicit_needs = []
        if "pain_points" in client_data:
            explicit_needs = client_data["pain_points"]
        
        # 挖掘隐性需求（未明确表达但可能存在的需求）
        implicit_needs = []
        if "operational_data" in client_data:
            # 根据运营数据推断潜在需求
            ops_data = client_data["operational_data"]
            if ops_data.get("downtime") > 10:
                implicit_needs.append("提高设备可靠性")
            if ops_data.get("energy_consumption") > industry_average:
                implicit_needs.append("节能优化方案")
        
        # 计算紧急度评级（1-10，10为最紧急）
        urgency_rating = 0
        if explicit_needs:
            urgency_rating = max(5, len(explicit_needs) * 2)
        if "critical_issues" in client_data and client_data["critical_issues"]:
            urgency_rating = 8
        
        return {
            "explicit_needs": explicit_needs,
            "implicit_needs": implicit_needs,
            "urgency_rating": min(10, urgency_rating)
        }
    
    def analyze_competition(self, competitor_data):
        """
        工业竞争情报洞察
        输入: 工业竞品与行业数据
        输出: 工业竞品动态报告
        """
        self.competitor_data = competitor_data
        
        # 分析竞品签单案例
        case_studies = []
        if "win_cases" in competitor_data:
            case_studies = [
                {
                    "client": case["client"],
                    "solution": case["solution"],
                    "value_proposition": case.get("value_prop", "")
                } for case in competitor_data["win_cases"]
            ]
        
        # 提取竞品营销策略
        marketing_strategies = []
        if "marketing_activities" in competitor_data:
            marketing_strategies = [
                {
                    "channel": activity["channel"],
                    "content_type": activity["content_type"],
                    "success_rate": activity.get("success_rate", 0)
                } for activity in competitor_data["marketing_activities"]
            ]
        
        # 生成应对建议
        countermeasures = []
        if case_studies:
            countermeasures.append("强化差异化价值主张")
        if marketing_strategies:
            countermeasures.append("优化渠道组合策略")
        
        return {
            "case_studies": case_studies,
            "marketing_strategies": marketing_strategies,
            "countermeasures": countermeasures
        }
    
    def evaluate_market_opportunities(self, market_data):
        """
        工业市场机会研判
        输入: 工业市场定向数据
        输出: 工业市场机会热力图
        """
        self.market_data = market_data
        
        # 准备大模型提示词
        from modules.prompt_manager import PromptEngineeringManager
        prompt_manager = PromptEngineeringManager()
        
        context = {
            "industry_trends": str(market_data.get("industry_trends", [])),
            "competition_data": str(market_data.get("competition_data", {})),
            "customer_needs": str(market_data.get("customer_segments", []))
        }
        
        prompt = prompt_manager.render_template("strategy_analysis", context)
        
        # 调用大模型API
        from modules.llm_orchestrator import LLMOrchestrator
        orchestrator = LLMOrchestrator()
        
        try:
            response = orchestrator.dispatch_request(
                task_type="strategy_analysis",
                prompt=prompt
            )
            
            # 解析大模型响应
            if prompt_manager.validate_response_format(response["response"], "json"):
                return json.loads(response["response"])
            else:
                raise ValueError("大模型返回格式无效")
                
        except Exception as e:
            print(f"大模型调用失败，使用备用逻辑: {str(e)}")
            # 降级方案：使用原逻辑
            return self._fallback_market_analysis(market_data)
    
    def _fallback_market_analysis(self, market_data):
        """备用市场分析逻辑"""
        customer_profiles = []
        if "customer_segments" in market_data:
            customer_profiles = [
                {
                    "segment": segment["name"],
                    "size": segment["market_size"],
                    "growth": segment["growth_rate"],
                    "priority": "高" if segment["growth_rate"] > 0.1 else "中"
                } for segment in market_data["customer_segments"]
            ]
        
        regional_opportunities = []
        if "regional_data" in market_data:
            regional_opportunities = [
                {
                    "region": region["name"],
                    "demand": region["demand_level"],
                    "competition": region["competition_index"],
                    "opportunity": region["demand_level"] / max(1, region["competition_index"])
                } for region in market_data["regional_data"]
            ]
        
        industry_ratings = []
        if "industry_trends" in market_data:
            industry_ratings = [
                {
                    "industry": trend["industry"],
                    "rating": trend["growth_potential"] * 0.6 + trend["profitability"] * 0.4,
                    "trend": trend["key_trend"]
                } for trend in market_data["industry_trends"]
            ]
            industry_ratings.sort(key=lambda x: x["rating"], reverse=True)
        
        return {
            "customer_profiles": customer_profiles,
            "regional_opportunities": regional_opportunities,
            "industry_ratings": industry_ratings
        }
    
    def generate_strategy_brief(self):
        """
        工业AI策略引擎
        整合前三项分析结果，生成营销作战简报
        """
        if not all([self.client_data, self.competitor_data, self.market_data]):
            raise ValueError("缺少必要的分析数据")
        
        # 确定目标客户
        target_clients = []
        customer_profiles = self.evaluate_market_opportunities(self.market_data)["customer_profiles"]
        if customer_profiles:
            target_clients = [profile["segment"] for profile in customer_profiles 
                            if profile["priority"] == "高" and profile["size"] > 1000]
        
        # 制定核心策略
        core_strategies = []
        client_needs = self.process_client_needs(self.client_data)
        if client_needs["explicit_needs"]:
            core_strategies.append(f"针对明确需求：{', '.join(client_needs['explicit_needs'])}")
        if client_needs["implicit_needs"]:
            core_strategies.append(f"挖掘潜在需求：{', '.join(client_needs['implicit_needs'])}")
        
        # 分析风险与机会
        risks_and_opportunities = []
        competition = self.analyze_competition(self.competitor_data)
        if competition["countermeasures"]:
            risks_and_opportunities.append(f"竞争应对：{', '.join(competition['countermeasures'])}")
        
        market_opps = self.evaluate_market_opportunities(self.market_data)
        if market_opps["regional_opportunities"]:
            best_region = max(market_opps["regional_opportunities"], key=lambda x: x["opportunity"])
            risks_and_opportunities.append(f"最佳区域机会：{best_region['region']} (机会指数:{best_region['opportunity']:.1f})")
        
        return {
            "target_clients": target_clients,
            "core_strategies": core_strategies,
            "risks_and_opportunities": risks_and_opportunities,
            "urgency": client_needs["urgency_rating"]
        }