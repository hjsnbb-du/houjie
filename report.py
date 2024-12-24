import os
import logging
from typing import List, Optional, Dict, Any
from concurrent import futures
import time
import random
from kimi import chat

from categories.bags.prompts import BagPromptManager
from categories.clothing.prompts import ClothingPromptManager
from categories.trendy_toys.prompts import ToyPromptManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('market_analysis.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

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
        logger.error(f"Attempted to load unsupported category: {category_name}")
        raise ValueError(f"Unsupported category: {category_name}")
    
    logger.debug(f"Loading category manager for: {category_name}")
    return managers[category_name]()

import yaml
import os.path

# Load templates from YAML configuration
config_dir = os.path.join(os.path.dirname(__file__), "config")
config_file = os.path.join(config_dir, "report_templates.yaml")

# Create config directory if it doesn't exist
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

try:
    with open(config_file, "r", encoding="utf-8") as f:
        templates = yaml.safe_load(f)
        report_template = templates["report_template"]
        conclusion_template = templates["conclusion_template"]
        section_templates = templates["section_templates"]
except Exception as e:
    logger.error(f"Failed to load templates from {config_file}: {str(e)}")
    # Fallback to default templates if loading fails
    report_template = """
    # AI市场洞察报告

    ## 主题：{topic}
    ## 类目：{category_name}

    ---
    """
    conclusion_template = """
    ## 结论与建议

    根据以上分析，我们为{category_name}设计团队提供以下立意方向和策略建议：

    - **设计灵感**：基于用户关注的热门元素和情感诉求，融入设计中。
    - **市场定位**：针对核心受众，制定符合其需求的产品策略。
    - **差异化竞争**：突出产品独特性，避免同质化，提升竞争优势。
    - **联动策略**：探索与「{topic}」相关的跨界合作机会，扩大品牌影响力。
    - **形象设计**：生成一条「{topic}」Midjourney形象设计的提示词，概括关键设计要素和创意亮点。
    """
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
    try:
        logger.debug(f"Making chat API call for topic: {params['topic']}")
        response = chat(params["prompt"].format(topic=params["topic"]))
        logger.debug(f"Successfully received response for topic: {params['topic']}")
        return response
    except Exception as e:
        logger.error(f"Chat API call failed for topic: {params['topic']}, error: {str(e)}")
        return "【Error: Failed to generate response】"

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
    logger.info(f"Loading category manager for: {category}")
    manager = load_category_manager(category)
    category_name = manager.get_name()
    
    # Validate required prompts
    required_sections = sections if sections else list(section_templates.keys())
    if not manager.validate_prompts(required_sections):
        logger.warning(f"Some required prompts are missing for category: {category}")
    
    prompts = manager.get_prompts()
    logger.info(f"Successfully loaded {category_name} manager with {len(prompts)} prompts")
    
    # Generate output filenames
    file_name = f"「{topic}」{category_name}市场分析报告.md"
    output = f"「{topic}」{category_name}市场分析报告.pdf"
    cache_dir = "cache"
    cache_file = os.path.join(cache_dir, f"{topic}_{category_name}_cache.md")
    
    # Create cache directory if it doesn't exist
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Check cache first
    if os.path.exists(cache_file):
        logger.info(f"Cache hit: Using cached content for {topic} {category_name}")
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                markdown_content = f.read()
            
            # Convert cached markdown to PDF if needed
            if not os.path.exists(output):
                logger.info("Converting cached markdown to PDF")
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                result = os.system(f'pandoc {file_name} -o {output} --css=base.css --pdf-engine=wkhtmltopdf --filter pandoc-mermaid')
                if result != 0:
                    raise RuntimeError("PDF conversion failed")
            return output
        except Exception as e:
            logger.error(f"Failed to use cached content: {str(e)}")
            # Continue with normal generation if cache fails
    
    # Check if final report already exists
    if os.path.exists(output):
        logger.info(f"Report already exists: {output}. Skipping generation.")
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
    try:
        with futures.ThreadPoolExecutor(7) as executor:
            futures_list = [executor.submit(coro_chat, params) for params in params_list]
            result_list = []
            for future in futures.as_completed(futures_list):
                try:
                    result = future.result()
                    result_list.append(result)
                except Exception as e:
                    logger.error(f"Failed to get result from future: {str(e)}")
                    result_list.append("【Error: Failed to generate section】")
    except Exception as e:
        logger.error(f"Thread pool execution failed: {str(e)}")
        result_list = ["【Error: Failed to generate responses】"] * len(params_list)
    
    # Compose markdown content
    markdown_content = ""
    try:
        markdown_content = report_template.format(topic=topic, category_name=category_name)
        level_list = ['一、', '二、', '三、', '四、', '五、']
        
        # Generate sections with error handling
        for response, section in zip(result_list, sections):
            try:
                if section in section_templates:
                    content = section_templates[section].format(
                        level=level_list.pop(0) if level_list else '',
                        response=response
                    )
                    markdown_content += content
            except Exception as e:
                logger.error(f"Failed to format section {section}: {str(e)}")
                markdown_content += f"\n## Error: Failed to generate {section} section\n\n---\n"
        
        # Add conclusions with error handling
        try:
            markdown_content += conclusion_template.format(
                topic=topic,
                category_name=category_name
            )
        except Exception as e:
            logger.error(f"Failed to format conclusion: {str(e)}")
            markdown_content += "\n## Error: Failed to generate conclusion section\n"
    except Exception as e:
        logger.error(f"Failed to generate markdown content: {str(e)}")
        markdown_content = f"""# Error Report
## Topic: {topic}
## Category: {category_name}

Failed to generate report content. Please try again later.
Error: {str(e)}
"""
    
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
    
    # Cache the markdown content and convert to PDF
    try:
        # Cache the markdown content
        logger.info(f"Caching markdown content to {cache_file}")
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        # Write markdown and convert to PDF
        logger.info(f"Writing markdown content to {file_name}")
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        logger.info(f"Converting markdown to PDF: {output}")
        result = os.system(f'pandoc {file_name} -o {output} --css=base.css --pdf-engine=wkhtmltopdf --filter pandoc-mermaid')
        if result != 0:
            logger.error(f"PDF conversion failed with exit code: {result}")
            raise RuntimeError("PDF conversion failed")
            
        logger.info(f"Successfully generated PDF report: {output}")
        return output
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {str(e)}")
        # Clean up cache file if report generation fails
        if os.path.exists(cache_file):
            try:
                os.remove(cache_file)
                logger.info(f"Removed failed cache file: {cache_file}")
            except Exception as cache_e:
                logger.error(f"Failed to remove cache file: {str(cache_e)}")
        raise RuntimeError(f"Report generation failed: {str(e)}")

if __name__ == "__main__":
    # Example usage
    report("新国潮", "trendy_toys")
