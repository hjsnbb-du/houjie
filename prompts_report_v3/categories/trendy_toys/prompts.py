"""
Trendy toys-specific prompt manager implementation.
Handles prompts related to toy market analysis and trends.
"""
import logging
from typing import Dict
from ..base import BasePromptManager

logger = logging.getLogger(__name__)


class ToyPromptManager(BasePromptManager):
    """Prompt manager for trendy toys category analysis."""
    
    def get_prompts(self) -> Dict[str, str]:
        """Return toy-specific analysis prompts.
        
        Returns:
            Dict[str, str]: A dictionary of prompt identifiers to prompt text.
        """
        logger.debug("Getting trendy toys-specific prompts")
        return {
            "hot_trends": """任务：请通过互联网搜索，收集最新的关于「{topic}」的热点趋势和话题，完成以下内容：

- **关键热词Top10**：
  - 收集与「{topic}」相关的在社交媒体、搜索引擎等平台上的热门关键词，列出前10名。
  - 提供每个关键词的热度指数或搜索量。

- **热门元素和符号**：
  - 识别「{topic}」中最受欢迎的元素、符号、角色形象等。
  - 分析这些元素在潮玩产品中的应用潜力。

回答要求：
- 列出具体的关键词和元素，提供数据支持。
- 分析逻辑清晰，条理分明。
- 提供数据来源和链接。""",

            "emotional_analysis": """任务：请通过互联网搜索，收集最新的社交媒体平台上用户对「{topic}」的评论和反馈，完成以下内容：

- **用户情感倾向**：
  - 总结用户对「{topic}」的主要情感表达（如怀旧、崇拜、共鸣）。
  - 提取常见的情感关键词，列出Top10。

- **情感关键词提取**：
  - 引用具体的用户评论示例（匿名处理个人信息）。
  - 分析这些情感关键词如何转化为潮玩产品设计元素。""",

            "trend_prediction": """任务：基于当前对「{topic}」的讨论热度和用户兴趣，预测未来与「{topic}」相关的潮玩设计趋势：

- **设计元素预测**：
  - 预测哪些「{topic}」中的元素或角色将在潮玩设计中受到欢迎。
  - 考虑社会文化、流行趋势等影响因素。

- **联动机会**：
  - 分析「{topic}」与潮玩联动的可行性，提出可能的合作形式（如手办、公仔、盲盒）。
  - 引用行业专家的观点或成功案例。""",

            "audience_analysis": """任务：描绘对「{topic}」感兴趣的受众画像，分析他们的兴趣圈层：


- **受众特征**：
  - 收集数据，描述「{topic}」粉丝的年龄、性别、职业、地域分布等。
  - 分析潮玩收藏爱好者的特征。

- **兴趣圈层**：
  - 分析这些受众的兴趣爱好和社交媒体行为。
  - 探讨他们对潮玩产品的收藏和互动方式。""",

            "user_segmentation": """任务：对「{topic}」感兴趣的潮玩用户进行细分，寻找联动机会：

- **用户群体划分**：
  - 将受众划分为不同的群体（如深度粉丝、收藏家、普通消费者）。
  - 描述每个群体的特征和需求。

- **联动策略**：
  - 针对不同的用户群体，提出具体的潮玩设计和营销策略。
  - 例如，针对收藏家设计限量版手办，针对普通消费者推出亲民款式等。""",

            "market_data": """任务：分析市场上与「{topic}」相关的潮玩产品或类似IP的成功案例：

- **成功案例分析**：
  - 列出市场上3-5个成功的IP潮玩联动案例。
  - 分析它们的成功因素（如设计特色、情感共鸣、营销策略）。

- **市场表现数据**：
  - 收集这些产品的销售数据、用户评价、社交媒体反响等。
  - 分析定价策略和市场接受度。""",

            "differentiation": """任务：针对拟设计的与「{topic}」相关的潮玩产品，提出差异化策略：

- **独特卖点**：
  - 突出拟设计产品的独特性（如创新的设计风格、互动性、收藏价值）。
  - 对比竞品，指出差异点和优势。

- **差异化策略**：
  - 提出避免同质化竞争的策略。
  - 建议在设计元素、材料工艺、用户体验等方面的创新措施。""",

            "design_prompt": """任务：基于以上分析，为「{topic}」潮玩产品生成设计提示：

- **关键设计要素**：
  - 提取「{topic}」中最具潜力的视觉元素。
  - 建议产品形态（如手办、盲盒、装饰品等）。

- **设计风格指导**：
  - 描述产品的整体风格定位。
  - 提供具体的设计建议和注意事项。"""
        }
    
    def get_name(self) -> str:
        """Return the display name for the trendy toys category.
        
        Returns:
            str: The human-readable category name in Chinese.
        """
        return "潮玩"
