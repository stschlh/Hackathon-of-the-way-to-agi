"""
提示词工程管理模块
实现动态提示词管理和优化
"""

from typing import Dict, List, Callable
import json
import re

class PromptEngineeringManager:
    def __init__(self):
        self.templates: Dict[str, Dict] = {
            "strategy_analysis": {
                "version": "1.0",
                "template": """作为工业营销专家，请分析以下数据：
行业趋势: {industry_trends}
竞争情报: {competition_data}
客户需求: {customer_needs}

请按照以下步骤思考：
1. 识别3个关键市场机会
2. 评估每个机会的可行性
3. 推荐最佳市场进入策略

输出格式：
```json
{
    "opportunities": [
        {
            "name": "机会名称",
            "feasibility": "高/中/低", 
            "strategy": "推荐策略"
        }
    ]
}```""",
                "variables": ["industry_trends", "competition_data", "customer_needs"]
            },
            "content_creation": {
                "version": "1.1",
                "template": """作为工业内容专家，请为{client_type}客户创建营销内容：
核心价值主张: {value_proposition}
客户痛点: {pain_points}

要求：
1. 突出{key_benefits}
2. 使用{style_preference}风格
3. 包含3个具体案例

输出格式：
```markdown
# 标题

## 核心优势
- 优势1
- 优势2

## 成功案例
1. 案例1
2. 案例2
```""",
                "variables": ["client_type", "value_proposition", "pain_points", 
                             "key_benefits", "style_preference"]
            }
        }
        
        self.evaluation_metrics = {
            "relevance": 0,
            "creativity": 0,
            "clarity": 0
        }

    def render_template(self, template_name: str, context: Dict[str, str]) -> str:
        """渲染提示词模板"""
        if template_name not in self.templates:
            raise ValueError(f"模板'{template_name}'不存在")
        
        template = self.templates[template_name]["template"]
        
        # 简单变量替换
        for var in self.templates[template_name]["variables"]:
            template = template.replace(f"{{{var}}}", context.get(var, ""))
            
        return template
    
    def add_cot_instructions(self, prompt: str, steps: List[str]) -> str:
        """添加思维链(CoT)指令"""
        cot_part = "\n请按照以下步骤思考：\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
        return prompt + cot_part
    
    def validate_response_format(self, response: str, expected_format: str) -> bool:
        """验证响应格式"""
        if expected_format == "json":
            try:
                json.loads(response)
                return True
            except:
                return False
        elif expected_format == "markdown":
            return bool(re.search(r"#.+\n##.+\n-.+", response))
        return True
    
    def evaluate_prompt_quality(self, prompt: str) -> Dict[str, int]:
        """评估提示词质量 (简化版)"""
        # 实际实现应该更复杂
        score = {
            "relevance": min(len(prompt)//100, 10),
            "creativity": min(len(re.findall(r"创新|突破|独特", prompt)), 10),
            "clarity": 10 - min(len(re.findall(r"模糊|不确定|可能", prompt)), 10)
        }
        return score