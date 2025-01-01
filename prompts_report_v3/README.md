# Market Analysis Report Generator

A modular system for generating market analysis reports across different product categories using AI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
python -m pytest
```

## Project Structure

- `categories/` - Category-specific prompt managers
- `config/` - Configuration files and templates
- `tests/` - Test suite
- `report.py` - Core report generation logic
- `main.py` - Streamlit frontend interface

## Adding New Categories

1. Create a new directory under `categories/`
2. Implement a new PromptManager class extending BasePromptManager
3. Add category-specific prompts
4. Update the category manager registry in `report.py`

## Running Tests

```bash
python -m pytest  # Run all tests
python -m pytest -v  # Verbose output
python -m pytest -k "test_name"  # Run specific test
```
