"""
Bag-specific prompt manager implementation.
Handles prompts related to bag market analysis and trends.
"""
from typing import Dict
from ..base import BasePromptManager


class BagPromptManager(BasePromptManager):
    """Prompt manager for bag category analysis."""
    
    def get_prompts(self) -> Dict[str, str]:
        """Return bag-specific analysis prompts.
        
        Returns:
            Dict[str, str]: A dictionary of prompt identifiers to prompt text.
        """
        return {
            "market_analysis": """请分析箱包市场的以下方面：
1. 市场规模和增长趋势
2. 主要消费群体画像
3. 价格区间分布
4. 主要销售渠道
5. 市场竞争格局分析""",
            
            "trend_analysis": """请分析箱包行业的流行趋势：
1. 当前流行的箱包款式和特点
2. 材质和工艺趋势
3. 色彩趋势
4. 功能性需求变化
5. 未来发展方向预测""",
            
            "consumer_insight": """请深入分析箱包消费者的：
1. 购买决策因素
2. 使用场景需求
3. 品牌认知和偏好
4. 价格敏感度
5. 重复购买行为""",
            
            "competitive_analysis": """请分析箱包市场的竞争情况：
1. 主要品牌市场份额
2. 各品牌定位和特色
3. 价格策略对比
4. 产品线布局
5. 营销策略分析""",
            
            "channel_strategy": """请分析箱包品类的渠道策略：
1. 线上线下渠道分布
2. 各渠道销售特点
3. 渠道定价策略
4. 新零售模式应用
5. 渠道发展建议"""
        }
    
    def get_name(self) -> str:
        """Return the display name for the bag category.
        
        Returns:
            str: The human-readable category name in Chinese.
        """
        return "箱包"
