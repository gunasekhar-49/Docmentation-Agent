# Contributing to AI Agents Documentation

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on what's best for the community
- Report unacceptable behavior

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find one already exists.

**When reporting bugs, include:**
- Clear, descriptive title
- Detailed description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Code samples if applicable
- Python version and OS
- Error messages and stack traces

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**When suggesting enhancements, provide:**
- Clear, descriptive title
- Detailed description of the enhancement
- Why this would be useful
- Possible implementation approach
- Examples if applicable

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/ai-agents-documentation.git
   cd ai-agents-documentation
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Make your changes**
   - Write clean, readable code
   - Follow PEP 8 style guide
   - Add comments for complex logic
   - Include docstrings for all functions/classes

5. **Test your changes**
   ```bash
   # Run unit tests
   pytest tests/
   
   # Check code style
   flake8 .
   black --check .
   
   # Type checking
   mypy .
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of changes"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**
   - Describe what changes you've made
   - Explain why these changes are needed
   - Link any related issues
   - Make sure CI passes

## Development Setup

### Requirements

- Python 3.8 or higher
- pip or conda
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ai-agents-documentation.git
cd ai-agents-documentation

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up API key
export ANTHROPIC_API_KEY="your_key_here"
```

## Code Style Guidelines

### Python Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```python
# Good
def calculate_total(items: list, tax_rate: float = 0.1) -> float:
    """Calculate total with tax.
    
    Args:
        items: List of item dictionaries
        tax_rate: Tax rate as decimal (default 0.1)
        
    Returns:
        Total amount including tax
    """
    subtotal = sum(item['price'] for item in items)
    return subtotal * (1 + tax_rate)


# Avoid
def calcTotal(items,taxrate=0.1):
    s=sum([i['price'] for i in items])
    return s*(1+taxrate)
```

### Naming Conventions

- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

### Documentation

All public functions and classes must have docstrings:

```python
def process_data(data: dict) -> dict:
    """
    Process input data and return results.
    
    Args:
        data: Dictionary containing raw data
        
    Returns:
        Dictionary with processed data
        
    Raises:
        ValueError: If data is empty
        TypeError: If data is not a dict
    """
    if not data:
        raise ValueError("Data cannot be empty")
    # Implementation here
```

## Testing Guidelines

### Writing Tests

```python
import unittest
from your_module import function_to_test

class TestFunctionName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.test_data = {"key": "value"}
    
    def test_normal_case(self):
        """Test normal operation"""
        result = function_to_test(self.test_data)
        self.assertEqual(result, expected_value)
    
    def test_edge_case(self):
        """Test edge case"""
        result = function_to_test({})
        self.assertIsNotNone(result)
    
    def test_error_case(self):
        """Test error handling"""
        with self.assertRaises(ValueError):
            function_to_test(None)
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_docstring_agent.py

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_docstring_agent.py::TestDocstringAgent::test_empty_file_handling
```

## Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep commits focused on a single change
- Reference issues when applicable

### Example Commits

```
Add support for NumPy docstring format
Fix handling of empty files in batch processing
Update README with installation instructions
Refactor context size management in ReadmeAgent
```

## Areas for Contribution

### High Priority

- [ ] Support for NumPy and Sphinx docstring formats
- [ ] Better async function handling
- [ ] Performance optimizations
- [ ] Enhanced error messages

### Medium Priority

- [ ] Support for other programming languages
- [ ] Custom docstring templates
- [ ] Configuration file support
- [ ] Logging improvements

### Low Priority

- [ ] Web UI improvements
- [ ] Additional test coverage
- [ ] Documentation enhancements
- [ ] Example projects

## Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Ideas:** Start a Discussion
- **Chat:** Join our community on Discord (if available)

## Release Process

Maintainers handle releases. The process:

1. Update version number in `__init__.py`
2. Update CHANGELOG
3. Create release notes
4. Tag release in Git
5. Publish to PyPI

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better. We appreciate your help! 🎉
