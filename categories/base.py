"""
Base class for category-specific prompt managers.
This module defines the interface that all category prompt managers must implement.
"""
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class BasePromptManager:
    """Base class for managing category-specific prompts and templates."""
    
    def get_prompts(self) -> Dict[str, str]:
        """Return a dictionary mapping prompt names to their content.
        
        Returns:
            Dict[str, str]: A dictionary where keys are prompt identifiers and
                           values are the actual prompt text.
        
        Raises:
            NotImplementedError: This is an abstract method that must be implemented
                               by concrete category managers.
        """
        logger.debug("Base get_prompts called - should be implemented by subclass")
        raise NotImplementedError("Subclasses must implement get_prompts()")
    
    def get_name(self) -> str:
        """Return a human-readable name for this category.
        
        Returns:
            str: The display name for this category (e.g., "箱包", "服装", etc.)
        
        Raises:
            NotImplementedError: This is an abstract method that must be implemented
                               by concrete category managers.
        """
        raise NotImplementedError("Subclasses must implement get_name()")

    def validate_prompts(self, required_keys: List[str]) -> bool:
        """Validate that all required prompt keys are present.
        
        Args:
            required_keys (List[str]): List of required prompt keys
            
        Returns:
            bool: True if all required keys are present, False otherwise
        """
        try:
            prompts = self.get_prompts()
            missing_keys = [key for key in required_keys if key not in prompts]
            
            if missing_keys:
                logger.warning(f"Missing required prompt keys in {self.__class__.__name__}: {missing_keys}")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Failed to validate prompts for {self.__class__.__name__}: {str(e)}")
            return False
