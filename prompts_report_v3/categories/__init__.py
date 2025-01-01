"""
Categories package.
Provides category-specific prompt managers and registry.
"""
from .registry import get_category_manager, get_available_categories

__all__ = ['get_category_manager', 'get_available_categories']
