"""
Base class for category-specific prompt managers.
This module defines the interface that all category prompt managers must implement.
"""
from typing import Dict


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
