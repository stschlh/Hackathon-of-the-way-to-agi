"""
工业内容创造与武装模块
实现方案/内容生成和销售话术提词功能
"""

class ContentCreation:
    def __init__(self):
        self.marketing_plan = None
        self.technical_materials = []
        self.sales_scripts = []
    
    def generate_technical_materials(self, marketing_plan):
        """
        工业方案/内容生成器
        输入: 工业营销行动计划
        输出: 定制化工业技术物料
        """
        self.marketing_plan = marketing_plan
        from modules.llm_orchestrator import LLMOrchestrator
        from modules.prompt_manager import PromptEngineeringManager
        
        orchestrator = LLMOrchestrator()
        prompt_manager = PromptEngineeringManager()
        
        materials = []
        formats = []
        
        # 为每种客户类型生成内容
        for strategy in marketing_plan.get("client_strategies", {}).get("strategies", []):
            context = {
                "client_type": strategy["type"],
                "value_proposition": strategy.get("value_proposition", ""),
                "pain_points": ", ".join(self.marketing_plan.get("client_needs", {}).get("explicit_needs", [])),
                "key_benefits": "技术优势" if strategy["type"] == "国企" else "成本效益",
                "style_preference": "专业严谨" if strategy["type"] == "国企" else "简洁实用"
            }
            
            prompt = prompt_manager.render_template("content_creation", context)
            
            try:
                # 调用大模型生成内容
                response = orchestrator.dispatch_request(
                    task_type="content_creation",
                    prompt=prompt
                )
                
                if prompt_manager.validate_response_format(response["response"], "markdown"):
                    format_type = "PDF" if strategy["type"] == "国企" else "Excel"
                    materials.append({
                        "type": f"{strategy['type']}定制内容",
                        "title": f"{strategy['type']}技术方案",
                        "content": response["response"],
                        "optimized": True
                    })
                    formats.append(format_type)
                else:
                    raise ValueError("响应格式无效")
                    
            except Exception as e:
                print(f"内容生成失败，使用模板内容: {str(e)}")
                # 降级方案：使用模板内容
                materials.append({
                    "type": f"{strategy['type']}基础内容",
                    "title": f"{strategy['type']}技术方案",
                    "content": "标准技术方案内容",
                    "optimized": False
                })
                formats.append("PDF")
        
        self.technical_materials = {
            "materials": materials,
            "formats": list(set(formats))
        }
        
        return self.technical_materials
    
    def generate_sales_scripts(self):
        """
        工业销售话术提词器
        输出: 场景化工业话术库
        """
        if not self.marketing_plan:
            raise ValueError("需要先生成技术物料")
        
        scenarios = []
        scripts = []
        
        # 根据客户类型生成话术
        for strategy in self.marketing_plan.get("client_strategies", {}).get("strategies", []):
            if strategy["type"] == "国企":
                scenarios.append({
                    "type": "技术沟通",
                    "script": "我们的方案完全符合国家标准GB/T XXXXX，已获得XX认证..."
                })
                scenarios.append({
                    "type": "价格谈判",
                    "script": "考虑到长期合作和政府项目特点，我们可以提供..."
                })
            elif strategy["type"] == "民企":
                scenarios.append({
                    "type": "ROI展示",
                    "script": "根据我们的计算，实施后6个月内即可收回成本，年节省XX万元..."
                })
                scenarios.append({
                    "type": "快速实施",
                    "script": "我们承诺30天内完成部署，不影响您的正常生产..."
                })
            elif strategy["type"] == "外企":
                scenarios.append({
                    "type": "全球标准",
                    "script": "我们的技术已通过ISO XXXXX认证，在全球XX个国家成功应用..."
                })
                scenarios.append({
                    "type": "本地支持",
                    "script": "我们在本地有XX名认证工程师，提供7×24小时支持..."
                })
        
        # 根据定价方案补充话术
        for plan in self.marketing_plan.get("pricing_plans", {}).get("plans", []):
            if plan["name"] == "高级方案":
                scenarios.append({
                    "type": "增值服务",
                    "script": "选择高级方案可享受专属客户经理和优先技术支持..."
                })
        
        self.sales_scripts = {
            "scenarios": scenarios,
            "scripts": scripts
        }
        
        return self.sales_scripts
    
    def package_marketing_kit(self):
        """
        整合生成工业"营销弹药包"
        按场景分类封装
        """
        return {
            "technical_materials": self.technical_materials,
            "sales_scripts": self.sales_scripts
        }