"""
Clothing-specific prompt manager implementation.
Handles prompts related to clothing market analysis and trends.
"""
import logging
from typing import Dict
from ..base import BasePromptManager

logger = logging.getLogger(__name__)


class ClothingPromptManager(BasePromptManager):
    """Prompt manager for clothing category analysis."""
    
    def get_prompts(self) -> Dict[str, str]:
        """Return clothing-specific analysis prompts.
        
        Returns:
            Dict[str, str]: A dictionary of prompt identifiers to prompt text.
        """
        logger.debug("Getting clothing-specific prompts")
        return {
            "hot_trends": """任务：请通过互联网搜索，收集最新的关于「{topic}」的服装设计趋势和话题：

- **流行元素Top10**：
  - 收集与「{topic}」风格相关的服装设计元素，列出前10名。
  - 分析每个元素在当季服装中的应用效果。

- **设计灵感来源**：
  - 识别「{topic}」中可用于服装设计的视觉元素和文化符号。
  - 分析这些元素如何融入现代服装设计。""",

            "emotional_analysis": """任务：分析用户对「{topic}」风格服装的情感共鸣：

- **风格认知分析**：
  - 收集社交媒体上关于类似风格服装的用户评论。
  - 提取用户对服装审美和穿着体验的情感表达。

- **文化价值转化**：
  - 分析「{topic}」的文化内涵如何转化为服装设计语言。
  - 探讨提升用户文化认同感的设计方向。""",

            "trend_prediction": """任务：预测「{topic}」风格在服装设计中的发展趋势：

- **季节性趋势**：
  - 预测春夏秋冬各季节的设计重点。
  - 分析色彩、面料、剪裁的季节性变化。

- **创新方向**：
  - 预测服装设计的创新可能性。
  - 提出融合传统与现代的设计思路。""",

            "audience_analysis": """任务：分析「{topic}」风格服装的目标用户：

- **穿着场景**：
  - 分析目标用户的日常、社交、职业等场景需求。
  - 研究不同场景下的着装偏好。

- **消费特征**：
  - 描述目标用户的年龄、职业、生活方式等特征。
  - 分析消费能力和购买习惯。""",

            "user_segmentation": """任务：细分「{topic}」风格服装的用户群体：

- **群体划分**：
  - 按着装风格划分（如正装、休闲、时尚等）。
  - 按消费层级和审美偏好划分。

- **系列规划**：
  - 针对不同群体规划产品系列。
  - 制定差异化的营销策略。""",

            "market_data": """任务：分析服装市场的竞品数据：

- **竞品分析**：
  - 调研同类风格服装品牌的市场表现。
  - 分析竞品的设计特色和价格策略。

- **市场机会**：
  - 发现细分市场的机会点。
  - 评估市场潜力和竞争风险。""",

            "differentiation": """任务：制定「{topic}」风格服装的差异化策略：

- **设计差异化**：
  - 在款式、面料、工艺上的创新点。
  - 独特的品牌设计语言。

- **品牌策略**：
  - 品牌调性和市场定位。
  - 产品价格带规划。""",

            "design_prompt": """任务：为「{topic}」风格服装生成设计提示：

- **设计要点**：
  - 关键设计元素的提取和应用。
  - 面料、色彩、剪裁的建议。

- **系列构成**：
  - 不同场景的搭配组合。
  - 核心单品和配套单品的设计思路。"""
        }
    
    def get_name(self) -> str:
        """Return the display name for the clothing category.
        
        Returns:
            str: The human-readable category name in Chinese.
        """
        return "服装"
