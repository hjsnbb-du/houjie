"""
Unit tests for report generation functionality.
Tests category manager loading, validation, and basic concurrency.
"""
import pytest
from ..report import load_category_manager, report
from ..categories.base import BasePromptManager


def test_load_valid_manager():
    """Test loading a valid category manager."""
    manager = load_category_manager("bags")
    assert isinstance(manager, BasePromptManager)
    assert manager.get_name() == "箱包"


def test_load_invalid_manager():
    """Test loading an invalid category manager raises ValueError."""
    with pytest.raises(ValueError):
        load_category_manager("invalid_category")


def test_manager_validation():
    """Test prompt validation in category managers."""
    manager = load_category_manager("bags")
    # Test with valid required keys
    assert manager.validate_prompts(["market_analysis"]) is True
    # Test with invalid required keys
    assert manager.validate_prompts(["invalid_key"]) is False


def test_concurrent_report_generation():
    """Test concurrent report generation with multiple sections."""
    output = report(
        topic="测试主题",
        category="bags",
        sections=["market_analysis", "trend_analysis"]
    )
    assert output.endswith(".pdf")
    assert "测试主题" in output
