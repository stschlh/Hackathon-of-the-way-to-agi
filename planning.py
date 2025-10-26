"""
工业策略与计划制定模块
实现客户策略匹配、定价策略计算和渠道策略制定功能
"""

class Planning:
    def __init__(self):
        self.strategy_brief = None
        self.client_strategies = {}
        self.pricing_plans = []
        self.channel_strategies = []
    
    def match_client_strategies(self, strategy_brief):
        """
        工业客户策略匹配
        输入: 工业营销作战简报
        输出: 定制化沟通策略与价值主张
        """
        self.strategy_brief = strategy_brief
        strategies = []
        value_propositions = []
        
        # 根据客户类型匹配策略
        for client_type in strategy_brief.get("target_clients", []):
            if "国企" in client_type:
                strategies.append({
                    "type": "国企",
                    "approach": "技术合规导向",
                    "focus": "长期合作关系"
                })
                value_propositions.append({
                    "type": "国企",
                    "value": "符合国家标准的解决方案",
                    "differentiator": "政府认证资质"
                })
            elif "民企" in client_type:
                strategies.append({
                    "type": "民企",
                    "approach": "ROI导向",
                    "focus": "快速见效"
                })
                value_propositions.append({
                    "type": "民企",
                    "value": "成本效益优化方案",
                    "differentiator": "快速实施能力"
                })
            elif "外企" in client_type:
                strategies.append({
                    "type": "外企",
                    "approach": "全球化标准",
                    "focus": "技术创新"
                })
                value_propositions.append({
                    "type": "外企",
                    "value": "国际认证的技术方案",
                    "differentiator": "全球服务网络"
                })
        
        # 根据紧急度调整策略
        urgency = strategy_brief.get("urgency", 5)
        if urgency > 7:
            for strategy in strategies:
                strategy["priority"] = "高"
                strategy["timeline"] = "30天内"
        
        self.client_strategies = {
            "strategies": strategies,
            "value_propositions": value_propositions
        }
        
        return self.client_strategies
    
    def calculate_pricing_strategies(self):
        """
        工业定价策略计算
        输出: 工业多版本报价方案与推荐理由
        """
        if not self.strategy_brief:
            raise ValueError("需要先执行客户策略匹配")
        
        plans = []
        recommendations = []
        
        # 基础定价方案
        base_plan = {
            "name": "标准方案",
            "price": "$$",
            "features": ["核心功能"],
            "target": "预算有限客户"
        }
        plans.append(base_plan)
        
        # 高级定价方案
        premium_plan = {
            "name": "高级方案",
            "price": "$$$",
            "features": ["核心功能", "增值服务", "优先支持"],
            "target": "重视服务质量的客户"
        }
        plans.append(premium_plan)
        
        # 定制化定价方案
        custom_plan = {
            "name": "定制方案",
            "price": "协商定价",
            "features": ["完全定制", "专属团队", "长期合作"],
            "target": "大型企业客户"
        }
        plans.append(custom_plan)
        
        # 根据客户需求调整推荐
        client_needs = self.strategy_brief.get("core_strategies", [])
        if "ROI导向" in str(client_needs):
            recommendations.append("推荐标准方案，强调成本效益")
        if "技术合规导向" in str(client_needs):
            recommendations.append("推荐高级方案，强调质量保证")
        if "全球化标准" in str(client_needs):
            recommendations.append("推荐定制方案，强调全球服务能力")
        
        self.pricing_plans = {
            "plans": plans,
            "recommendations": recommendations
        }
        
        return self.pricing_plans
    
    def develop_channel_strategies(self):
        """
        工业渠道策略制定
        输出: 工业渠道组合建议与内容形式
        """
        if not self.strategy_brief:
            raise ValueError("需要先执行客户策略匹配")
        
        channel_mix = []
        content_types = []
        
        # 根据客户类型推荐渠道
        for strategy in self.client_strategies.get("strategies", []):
            if strategy["type"] == "国企":
                channel_mix.append({
                    "type": "国企",
                    "channels": ["行业展会", "政府对接会", "行业协会"],
                    "priority": "高" if strategy.get("priority") == "高" else "中"
                })
                content_types.append({
                    "type": "国企",
                    "formats": ["白皮书", "技术标准文档", "合规报告"]
                })
            elif strategy["type"] == "民企":
                channel_mix.append({
                    "type": "民企",
                    "channels": ["垂直平台", "私域社群", "线上研讨会"],
                    "priority": "高" if strategy.get("priority") == "高" else "中"
                })
                content_types.append({
                    "type": "民企",
                    "formats": ["案例研究", "ROI计算器", "快速实施指南"]
                })
            elif strategy["type"] == "外企":
                channel_mix.append({
                    "type": "外企",
                    "channels": ["国际展会", "英文技术社区", "全球合作伙伴网络"],
                    "priority": "高" if strategy.get("priority") == "高" else "中"
                })
                content_types.append({
                    "type": "外企",
                    "formats": ["英文技术文档", "全球案例库", "多语言视频"]
                })
        
        self.channel_strategies = {
            "channel_mix": channel_mix,
            "content_types": content_types
        }
        
        return self.channel_strategies
    
    def generate_marketing_plan(self):
        """
        整合生成工业客户专属营销行动计划
        """
        return {
            "client_strategies": self.client_strategies,
            "pricing_plans": self.pricing_plans,
            "channel_strategies": self.channel_strategies
        }