"""
Bag-specific prompt manager implementation.
Handles prompts related to bag market analysis and trends.
"""
import logging
from typing import Dict
from ..base import BasePromptManager

logger = logging.getLogger(__name__)


class BagPromptManager(BasePromptManager):
    """Prompt manager for bag category analysis."""
    
    def get_prompts(self) -> Dict[str, str]:
        """Return bag-specific analysis prompts.
        
        Returns:
            Dict[str, str]: A dictionary of prompt identifiers to prompt text.
        """
        logger.debug("Getting bag-specific prompts")
        return {
            "hot_trends": """任务：请通过互联网搜索，收集最新的关于「{topic}」的箱包设计趋势和话题：

- **流行款式Top10**：
  - 收集与「{topic}」风格相关的热门箱包款式，列出前10名。
  - 分析每种款式的特点和市场表现。

- **设计元素分析**：
  - 识别「{topic}」中可用于箱包设计的视觉元素。
  - 分析这些元素在箱包产品中的应用方式。""",

            "emotional_analysis": """任务：分析用户对「{topic}」风格箱包的情感需求：

- **用户评价分析**：
  - 收集社交媒体上关于类似风格箱包的用户评论。
  - 提取用户对箱包功能和审美的情感诉求。

- **情感价值转化**：
  - 分析如何将「{topic}」的情感价值转化为箱包设计元素。
  - 探讨提升用户情感共鸣的设计方向。""",

            "trend_prediction": """任务：预测「{topic}」风格在箱包设计中的发展趋势：

- **材质工艺趋势**：
  - 预测适合「{topic}」风格的新材质和工艺。
  - 分析创新材质对产品价值的提升。

- **功能创新方向**：
  - 预测箱包功能需求的变化趋势。
  - 提出创新的功能设计建议。""",

            "audience_analysis": """任务：分析「{topic}」风格箱包的目标用户：

- **用户画像**：
  - 描述目标用户的年龄、职业、生活方式等特征。
  - 分析用户的使用场景和需求。

- **消费行为**：
  - 研究用户的购买决策因素。
  - 分析价格敏感度和品牌偏好。""",

            "user_segmentation": """任务：细分「{topic}」风格箱包的用户群体：

- **群体划分**：
  - 按使用场景划分（如商务、休闲、旅行）。
  - 按消费能力和品味偏好划分。

- **差异化策略**：
  - 针对不同群体提出产品系列规划。
  - 制定差异化的营销策略。""",

            "market_data": """任务：分析箱包市场的竞品数据：

- **竞品分析**：
  - 调研同类风格箱包的市场表现。
  - 分析竞品的优劣势和定价策略。

- **市场机会**：
  - 发现市场空白和机会点。
  - 预测产品潜在市场规模。""",

            "differentiation": """任务：制定「{topic}」风格箱包的差异化策略：

- **产品差异化**：
  - 在设计、材质、功能方面的创新点。
  - 独特的品牌价值主张。

- **竞争策略**：
  - 产品定位和价格策略。
  - 品牌传播和营销特色。""",

            "design_prompt": """任务：为「{topic}」风格箱包生成设计提示：

- **设计要点**：
  - 关键视觉元素的提取和应用。
  - 材质和工艺的选择建议。

- **系列规划**：
  - 不同场景的产品组合。
  - 核心产品和延伸产品的设计思路。"""
        }
    
    def get_name(self) -> str:
        """Return the display name for the bag category.
        
        Returns:
            str: The human-readable category name in Chinese.
        """
        return "箱包"
