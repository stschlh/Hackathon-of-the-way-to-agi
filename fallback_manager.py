"""
降级和重试管理模块
实现多级降级策略和智能重试逻辑
"""

import time
from typing import Callable, Any

class FallbackManager:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.retry_delays = [1, 3, 5]  # 指数退避延迟(秒)
        
    def execute_with_fallback(self, 
                            primary_func: Callable, 
                            fallback_funcs: list[Callable], 
                            *args, **kwargs) -> Any:
        """
        执行带降级策略的函数调用
        :param primary_func: 主函数
        :param fallback_funcs: 降级函数列表(按优先级排序)
        :return: 执行结果
        """
        last_error = None
        
        # 先尝试主函数
        for attempt in range(self.max_retries):
            try:
                result = primary_func(*args, **kwargs)
                return result
            except Exception as e:
                last_error = e
                if attempt < len(self.retry_delays):
                    time.sleep(self.retry_delays[attempt])
                continue
        
        # 主函数失败，尝试降级方案
        for fallback in fallback_funcs:
            for attempt in range(self.max_retries):
                try:
                    result = fallback(*args, **kwargs)
                    return result
                except Exception as e:
                    last_error = e
                    if attempt < len(self.retry_delays):
                        time.sleep(self.retry_delays[attempt])
                    continue
        
        # 所有尝试都失败
        raise Exception(f"所有执行尝试均失败。最后错误: {str(last_error)}")
    
    def add_exponential_backoff(self, func: Callable) -> Callable:
        """
        为函数添加指数退避装饰器
        """
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < len(self.retry_delays):
                        time.sleep(self.retry_delays[attempt])
                    continue
            raise Exception(f"函数{func.__name__}执行失败。最后错误: {str(last_error)}")
        return wrapper