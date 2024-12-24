import os
from typing import List, Optional, Dict, Any
from concurrent import futures
import time
import random
from kimi import chat

from categories.bags.prompts import BagPromptManager
from categories.clothing.prompts import ClothingPromptManager
from categories.trendy_toys.prompts import ToyPromptManager

def load_category_manager(category_name: str):
    """Load the appropriate prompt manager based on category name.
    
    Args:
        category_name (str): Name of the category to load
        
    Returns:
        BasePromptManager: The category-specific prompt manager
        
    Raises:
        ValueError: If an unsupported category is provided
    """
    managers = {
        "bags": BagPromptManager,
        "clothing": ClothingPromptManager,
        "trendy_toys": ToyPromptManager
    }
    
    if category_name not in managers:
        raise ValueError(f"Unsupported category: {category_name}")
    
    return managers[category_name]()

# Report template
report_template = """
# AI市场洞察报告

## 主题：{topic}
## 类目：{category_name}

---
"""

# Conclusion template
conclusion_template = """
## 结论与建议

根据以上分析，我们为{category_name}设计团队提供以下立意方向和策略建议：

- **设计灵感**：基于用户关注的热门元素和情感诉求，融入设计中。
- **市场定位**：针对核心受众，制定符合其需求的产品策略。
- **差异化竞争**：突出产品独特性，避免同质化，提升竞争优势。
- **联动策略**：探索与「{topic}」相关的跨界合作机会，扩大品牌影响力。
- **形象设计**：生成一条「{topic}」Midjourney形象设计的提示词，概括关键设计要素和创意亮点。
"""

# Section templates for different analysis aspects
section_templates = {
    "market_analysis": '\n## {level}市场分析\n\n{response}\n\n---\n',
    "trend_analysis": '\n## {level}趋势分析\n\n{response}\n\n---\n',
    "consumer_insight": '\n## {level}消费者洞察\n\n{response}\n\n---\n',
    "competitive_analysis": '\n## {level}竞品分析\n\n{response}\n\n---\n',
    "channel_strategy": '\n## {level}渠道策略\n\n{response}\n\n---\n'
}

def coro_chat(params: Dict[str, Any]) -> str:
    """Generate response for a specific prompt using chat API.
    
    Args:
        params (Dict[str, Any]): Dictionary containing topic and prompt
        
    Returns:
        str: Generated response from chat API
    """
    return chat(params["prompt"].format(topic=params["topic"]))

def report(topic: str, category: str, sections: Optional[List[str]] = None) -> str:
    """Generate a market analysis report for the specified topic and category.
    
    Args:
        topic (str): Analysis topic
        category (str): Product category (bags/clothing/trendy_toys)
        sections (List[str], optional): List of section keys to include
        
    Returns:
        str: Path to the generated PDF report
    """
    # Load category manager
    manager = load_category_manager(category)
    category_name = manager.get_name()
    prompts = manager.get_prompts()
    
    # Generate output filenames
    file_name = f"「{topic}」{category_name}市场分析报告.md"
    output = f"「{topic}」{category_name}市场分析报告.pdf"
    
    # Check if report already exists
    if os.path.exists(output):
        time.sleep(random.randint(20, 30))
        return output
    
    # Use all sections if none specified
    if sections is None:
        sections = list(prompts.keys())
    
    # Prepare parameters for concurrent execution
    params_list = [
        {"topic": topic, "prompt": prompts[section]}
        for section in sections
        if section in prompts
    ]
    
    # Generate responses concurrently
    with futures.ThreadPoolExecutor(7) as executor:
        result_list = executor.map(coro_chat, params_list)
    
    # Compose markdown content
    markdown_content = report_template.format(topic=topic, category_name=category_name)
    level_list = ['一、', '二、', '三、', '四、', '五、']
    
    for response, section in zip(result_list, sections):
        if section in section_templates:
            content = section_templates[section].format(
                level=level_list.pop(0) if level_list else '',
                response=response
            )
            markdown_content += content
    
    
    # Add conclusions
    markdown_content += conclusion_template.format(
        topic=topic,
        category_name=category_name
    )
    
    # Write markdown and convert to PDF
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    os.system(f'pandoc {file_name} -o {output} --css=base.css --pdf-engine=wkhtmltopdf --filter pandoc-mermaid')
    return output

if __name__ == "__main__":
    # Example usage
    report("新国潮", "trendy_toys")
