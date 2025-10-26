"""
工业复盘、归因与进化模块
实现数据分析、成功要素提取和失败原因诊断功能
"""

class Analysis:
    def __init__(self):
        self.sales_data = None
        self.success_factors = []
        self.failure_causes = []
    
    def analyze_performance(self, sales_data):
        """
        工业数据汇总与归因分析
        输入: 工业营销全流程数据
        输出: 成功或失败判断
        """
        self.sales_data = sales_data
        success = False
        key_metrics = {}
        
        # 计算关键指标
        total_clients = len(sales_data.get("potential_clients", []))
        converted_clients = sum(1 for p in sales_data.get("sales_progress", {}).get("stage_progress", []) 
                              if p["current_stage"] == "方案确认")
        conversion_rate = converted_clients / max(1, total_clients)
        
        # 判断成功标准 (假设转化率>30%为成功)
        success = conversion_rate > 0.3
        
        # 收集渠道效果数据
        channel_performance = {}
        for feedback in sales_data.get("channel_feedbacks", []):
            channel = feedback["channel"]
            if channel not in channel_performance:
                channel_performance[channel] = {"leads": 0, "conversions": 0}
            channel_performance[channel]["leads"] += 1
        
        # 更新渠道转化数据
        for progress in sales_data.get("sales_progress", {}).get("stage_progress", []):
            if progress["current_stage"] == "方案确认":
                for channel in channel_performance:
                    if channel in progress["client"]:  # 简化匹配逻辑
                        channel_performance[channel]["conversions"] += 1
        
        key_metrics = {
            "total_clients": total_clients,
            "converted_clients": converted_clients,
            "conversion_rate": round(conversion_rate, 2),
            "channel_performance": channel_performance,
            "success": success
        }
        
        return key_metrics
    
    def identify_success_factors(self):
        """
        工业成功要素分析
        输出: 成功关键因素
        """
        if not self.sales_data:
            raise ValueError("需要先执行数据分析")
        
        factors = []
        recommendations = []
        
        # 分析渠道表现
        channel_performance = self.sales_data.get("channel_performance", {})
        if channel_performance:
            best_channel = max(channel_performance.items(), 
                             key=lambda x: x[1]["conversions"]/max(1, x[1]["leads"]))
            factors.append({
                "factor": f"高效渠道: {best_channel[0]}",
                "impact": f"转化率{best_channel[1]['conversions']/max(1, best_channel[1]['leads']):.0%}"
            })
            recommendations.append(f"增加{best_channel[0]}渠道的投入")
        
        # 分析客户类型表现
        client_strategies = self.sales_data.get("client_strategies", [])
        if client_strategies:
            factors.append({
                "factor": "精准客户定位",
                "impact": "提高目标客户匹配度"
            })
            recommendations.append("优化客户细分策略")
        
        # 分析内容效果
        content_types = self.sales_data.get("content_types", [])
        if content_types:
            factors.append({
                "factor": "定制化内容",
                "impact": "提升客户参与度"
            })
            recommendations.append("扩展高互动内容类型")
        
        self.success_factors = {
            "factors": factors,
            "recommendations": recommendations
        }
        
        return self.success_factors
    
    def diagnose_failure_causes(self):
        """
        工业失败根因分析
        输出: 失败根本原因
        """
        if not self.sales_data:
            raise ValueError("需要先执行数据分析")
        
        from modules.llm_orchestrator import LLMOrchestrator
        from modules.prompt_manager import PromptEngineeringManager
        
        orchestrator = LLMOrchestrator()
        prompt_manager = PromptEngineeringManager()
        
        # 准备分析数据
        analysis_data = {
            "channel_performance": self.sales_data.get("channel_performance", {}),
            "sales_progress": self.sales_data.get("sales_progress", {}).get("stage_progress", []),
            "content_feedback": [f for f in self.sales_data.get("channel_feedbacks", []) 
                                if f.get("effectiveness") == "低"]
        }
        
        # 构建提示词
        prompt = f"""作为工业营销分析专家，请分析以下销售数据并找出根本原因：
        
销售数据概览：
- 总客户数: {self.sales_data.get('total_clients', 0)}
- 转化率: {self.sales_data.get('conversion_rate', 0):.0%}
- 渠道表现: {json.dumps(analysis_data['channel_performance'], indent=2)}
- 销售阶段阻塞情况: {len(analysis_data['sales_progress'])}个客户在销售流程中

请按照以下步骤分析：
1. 识别3个最关键的问题
2. 分析每个问题的根本原因
3. 为每个问题提供具体改进建议

输出格式：
```json
{
    "root_causes": [
        {
            "cause": "问题描述",
            "evidence": "数据支持", 
            "improvement": "改进建议"
        }
    ]
}```"""
        
        try:
            # 调用大模型分析
            response = orchestrator.dispatch_request(
                task_type="failure_analysis",
                prompt=prompt
            )
            
            if prompt_manager.validate_response_format(response["response"], "json"):
                result = json.loads(response["response"])
                self.failure_causes = result
                return result
            else:
                raise ValueError("大模型返回格式无效")
                
        except Exception as e:
            print(f"大模型分析失败，使用备用逻辑: {str(e)}")
            # 降级方案：使用原逻辑
            return self._fallback_failure_analysis()
    
    def _fallback_failure_analysis(self):
        """备用失败分析逻辑"""
        root_causes = []
        improvements = []
        
        channel_performance = self.sales_data.get("channel_performance", {})
        if channel_performance:
            worst_channel = min(channel_performance.items(),
                              key=lambda x: x[1]["conversions"]/max(1, x[1]["leads"]))
            if worst_channel[1]["conversions"]/max(1, worst_channel[1]["leads"]) < 0.1:
                root_causes.append({
                    "cause": f"低效渠道: {worst_channel[0]}",
                    "evidence": f"转化率仅{worst_channel[1]['conversions']/max(1, worst_channel[1]['leads']):.0%}"
                })
                improvements.append(f"优化或淘汰{worst_channel[0]}渠道")
        
        sales_progress = self.sales_data.get("sales_progress", {}).get("stage_progress", [])
        if sales_progress:
            stuck_stages = {}
            for progress in sales_progress:
                stage = progress["current_stage"]
                if stage not in ["方案确认", "签订合同"]:
                    if stage not in stuck_stages:
                        stuck_stages[stage] = 0
                    stuck_stages[stage] += 1
            
            if stuck_stages:
                main_stuck_stage = max(stuck_stages.items(), key=lambda x: x[1])
                root_causes.append({
                    "cause": f"销售漏斗阻塞: {main_stuck_stage[0]}阶段",
                    "evidence": f"{main_stuck_stage[1]}个客户在此阶段停滞"
                })
                improvements.append(f"加强{main_stuck_stage[0]}阶段的销售支持")
        
        content_issues = []
        for feedback in self.sales_data.get("channel_feedbacks", []):
            if feedback.get("effectiveness") == "低":
                content_issues.append(feedback["channel"])
        
        if content_issues:
            root_causes.append({
                "cause": "内容效果不佳",
                "evidence": f"在{', '.join(content_issues)}渠道表现差"
            })
            improvements.append("重新设计低效渠道的内容策略")
        
        self.failure_causes = {
            "root_causes": root_causes,
            "improvements": improvements
        }
        
        return self.failure_causes
    
    def optimize_knowledge_base(self):
        """
        工业策略与知识库优化
        输出: 迭代成果
        """
        updated_strategies = []
        new_templates = []
        experience_entries = []
        
        # 更新策略
        for factor in self.success_factors.get("factors", []):
            updated_strategies.append({
                "strategy": factor["factor"],
                "update": f"强化{factor['factor']}的应用",
                "reason": factor["impact"]
            })
        
        # 创建新模板
        for cause in self.failure_causes.get("root_causes", []):
            new_templates.append({
                "template": f"{cause['cause']}应对方案",
                "content": f"针对{cause['cause']}的标准处理流程",
                "based_on": cause["evidence"]
            })
        
        # 添加经验条目
        if self.sales_data.get("success"):
            experience_entries.append({
                "title": "成功案例",
                "content": "详细记录本次营销活动的成功实践",
                "tags": ["高效渠道", "精准定位"]
            })
        else:
            experience_entries.append({
                "title": "改进案例",
                "content": "记录本次营销活动的教训和改进措施",
                "tags": ["渠道优化", "流程改进"]
            })
        
        return {
            "updated_strategies": updated_strategies,
            "new_templates": new_templates,
            "experience_entries": experience_entries
        }