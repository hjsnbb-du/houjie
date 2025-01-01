"""
Category registry module.
Maps category names to their respective prompt manager classes.
"""
from typing import Dict, Type
import logging
from .base import BasePromptManager
from .bags.prompts import BagPromptManager
from .clothing.prompts import ClothingPromptManager
from .trendy_toys.prompts import ToyPromptManager

logger = logging.getLogger(__name__)

CATEGORY_REGISTRY: Dict[str, Type[BasePromptManager]] = {
    "bags": BagPromptManager,
    "clothing": ClothingPromptManager,
    "trendy_toys": ToyPromptManager
}

def get_category_manager(category: str) -> BasePromptManager:
    """Get an instance of the prompt manager for the specified category.
    
    Args:
        category (str): The category name to get a manager for.
        
    Returns:
        BasePromptManager: An instance of the appropriate prompt manager.
        
    Raises:
        ValueError: If the category is not found in the registry.
    """
    try:
        manager_class = CATEGORY_REGISTRY[category]
        return manager_class()
    except KeyError:
        logger.error(f"Category {category} not found in registry")
        raise ValueError(f"Unsupported category: {category}")

def get_available_categories() -> list[str]:
    """Get a list of all available category names.
    
    Returns:
        list[str]: List of category names that can be used with get_category_manager.
    """
    return list(CATEGORY_REGISTRY.keys())
