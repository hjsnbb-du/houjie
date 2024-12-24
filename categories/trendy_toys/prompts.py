"""
Trendy toys-specific prompt manager implementation.
Handles prompts related to toy market analysis and trends.
"""
from typing import Dict
from ..base import BasePromptManager


class ToyPromptManager(BasePromptManager):
    """Prompt manager for trendy toys category analysis."""
    
    def get_prompts(self) -> Dict[str, str]:
        """Return toy-specific analysis prompts.
        
        Returns:
            Dict[str, str]: A dictionary of prompt identifiers to prompt text.
        """
        return {
            "market_analysis": """请分析潮玩市场的以下方面：
1. 市场规模和增长速度
2. 目标用户群特征
3. 主流价位分布
4. IP授权市场现状
5. 市场机遇与风险""",
            
            "trend_analysis": """请分析潮玩行业的流行趋势：
1. 当前热门IP分析
2. 产品形态创新
3. 材质工艺发展
4. 联名合作趋势
5. 未来发展方向""",
            
            "consumer_insight": """请深入分析潮玩消费者的：
1. 收藏与购买动机
2. 社群文化特点
3. 品牌认知度
4. 消费决策因素
5. 二次交易行为""",
            
            "competitive_analysis": """请分析潮玩市场的竞争情况：
1. 头部品牌分析
2. IP运营策略
3. 产品线规划
4. 定价策略对比
5. 渠道布局特点""",
            
            "channel_strategy": """请分析潮玩品类的渠道策略：
1. 线上平台分布
2. 线下店铺形态
3. 盲盒销售模式
4. 社交媒体营销
5. 粉丝运营策略"""
        }
    
    def get_name(self) -> str:
        """Return the display name for the trendy toys category.
        
        Returns:
            str: The human-readable category name in Chinese.
        """
        return "潮玩"
