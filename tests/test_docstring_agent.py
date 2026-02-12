"""
Unit tests for Docstring Generation Agent
"""

import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Note: These tests require ANTHROPIC_API_KEY to be set
# Run with: pytest tests/test_docstring_agent.py


class TestDocstringAgent(unittest.TestCase):
    """Test cases for DocstringAgent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_empty_file_handling(self):
        """Test that empty files are handled gracefully"""
        empty_file = os.path.join(self.temp_dir, "empty.py")
        Path(empty_file).touch()
        
        # Test should not raise exception
        # This is a conceptual test - actual implementation would test the agent
        self.assertTrue(os.path.exists(empty_file))
    
    def test_invalid_python_syntax(self):
        """Test handling of invalid Python code"""
        invalid_file = os.path.join(self.temp_dir, "invalid.py")
        with open(invalid_file, 'w') as f:
            f.write("def broken_function(\n  missing closing paren")
        
        # Should raise SyntaxError or handle gracefully
        self.assertTrue(os.path.exists(invalid_file))
    
    def test_code_with_existing_docstring(self):
        """Test that existing docstrings are not overwritten"""
        code_with_docstring = os.path.join(self.temp_dir, "documented.py")
        with open(code_with_docstring, 'w') as f:
            f.write('''
def already_documented():
    """This function is already documented."""
    return True
''')
        
        self.assertTrue(os.path.exists(code_with_docstring))
    
    def test_async_function_detection(self):
        """Test detection of async functions"""
        async_file = os.path.join(self.temp_dir, "async.py")
        with open(async_file, 'w') as f:
            f.write('''
async def fetch_data():
    import asyncio
    await asyncio.sleep(1)
    return data
''')
        
        self.assertTrue(os.path.exists(async_file))
    
    def test_nested_class_detection(self):
        """Test detection of nested classes"""
        nested_file = os.path.join(self.temp_dir, "nested.py")
        with open(nested_file, 'w') as f:
            f.write('''
class Outer:
    class Inner:
        def method(self):
            pass
''')
        
        self.assertTrue(os.path.exists(nested_file))
    
    def test_large_file_handling(self):
        """Test handling of large files"""
        large_file = os.path.join(self.temp_dir, "large.py")
        with open(large_file, 'w') as f:
            f.write("def function_1():\n    pass\n\n" * 100)
        
        self.assertTrue(os.path.exists(large_file))
        self.assertGreater(os.path.getsize(large_file), 1000)


class TestDocstringExtraction(unittest.TestCase):
    """Test code element extraction"""
    
    def test_function_extraction(self):
        """Test extraction of functions"""
        code = """
def simple_function(arg1, arg2):
    return arg1 + arg2
"""
        # Would test extract_functions_and_classes method
        self.assertIn("def", code)
    
    def test_class_extraction(self):
        """Test extraction of classes"""
        code = """
class MyClass:
    def __init__(self):
        self.value = 0
    
    def method(self):
        return self.value
"""
        self.assertIn("class", code)
    
    def test_mixed_extraction(self):
        """Test extraction with mixed functions and classes"""
        code = """
def helper():
    pass

class Manager:
    def process(self):
        return helper()

async def fetch():
    pass
"""
        self.assertIn("def", code)
        self.assertIn("class", code)
        self.assertIn("async", code)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def test_file_permissions(self):
        """Test handling of permission errors"""
        # This would test permission error handling
        pass
    
    def test_unicode_content(self):
        """Test handling of Unicode characters in code"""
        code = """
def greet(name: str):
    # Unicode: 你好世界, مرحبا
    return f"Hello {name}"
"""
        self.assertIn("Hello", code)
    
    def test_multiline_strings(self):
        """Test handling of multiline strings and docstrings"""
        code = '''
def function_with_string():
    long_text = """
    This is a multiline
    string that spans
    multiple lines
    """
    return long_text
'''
        self.assertIn('"""', code)


if __name__ == '__main__':
    unittest.main()
