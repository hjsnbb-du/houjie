"""
Clothing-specific prompt manager implementation.
Handles prompts related to clothing market analysis and trends.
"""
from typing import Dict
from ..base import BasePromptManager


class ClothingPromptManager(BasePromptManager):
    """Prompt manager for clothing category analysis."""
    
    def get_prompts(self) -> Dict[str, str]:
        """Return clothing-specific analysis prompts.
        
        Returns:
            Dict[str, str]: A dictionary of prompt identifiers to prompt text.
        """
        return {
            "market_analysis": """请分析服装市场的以下方面：
1. 市场规模和增长预测
2. 细分市场占比分析
3. 消费人群画像
4. 区域市场特点
5. 市场机会与挑战""",
            
            "trend_analysis": """请分析服装行业的流行趋势：
1. 当季流行款式和设计元素
2. 面料与材质发展趋势
3. 流行色彩搭配
4. 可持续时尚趋势
5. 未来设计方向预测""",
            
            "consumer_insight": """请深入分析服装消费者的：
1. 购买决策因素
2. 穿着场景需求
3. 品牌忠诚度
4. 消费升级趋势
5. 购买频率与预算""",
            
            "competitive_analysis": """请分析服装市场的竞争情况：
1. 主要品牌市场地位
2. 产品定位对比
3. 价格带分布
4. 设计风格特点
5. 营销策略分析""",
            
            "channel_strategy": """请分析服装品类的渠道策略：
1. 全渠道布局现状
2. 新零售模式创新
3. 社交电商发展
4. 私域流量运营
5. 渠道整合建议"""
        }
    
    def get_name(self) -> str:
        """Return the display name for the clothing category.
        
        Returns:
            str: The human-readable category name in Chinese.
        """
        return "服装"
