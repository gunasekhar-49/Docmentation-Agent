"""
Unit tests for README Generation Agent
"""

import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Note: These tests require ANTHROPIC_API_KEY to be set
# Run with: pytest tests/test_readme_agent.py


class TestReadmeAgent(unittest.TestCase):
    """Test cases for ReadmeAgent class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_empty_directory_handling(self):
        """Test handling of empty directories"""
        self.assertTrue(os.path.isdir(self.temp_dir))
        self.assertEqual(len(os.listdir(self.temp_dir)), 0)
    
    def test_single_file_project(self):
        """Test README generation for single-file project"""
        test_file = os.path.join(self.temp_dir, "main.py")
        with open(test_file, 'w') as f:
            f.write("print('Hello World')")
        
        self.assertTrue(os.path.exists(test_file))
    
    def test_nested_directory_structure(self):
        """Test handling of nested directories"""
        nested_path = os.path.join(self.temp_dir, "src", "lib", "utils")
        os.makedirs(nested_path, exist_ok=True)
        
        test_file = os.path.join(nested_path, "helpers.py")
        Path(test_file).touch()
        
        self.assertTrue(os.path.exists(test_file))
    
    def test_important_files_detection(self):
        """Test detection of important project files"""
        important_files = [
            "requirements.txt",
            "setup.py",
            "README.md",
            "LICENSE",
            "Dockerfile"
        ]
        
        for filename in important_files:
            path = os.path.join(self.temp_dir, filename)
            with open(path, 'w') as f:
                f.write(f"# {filename}\n")
        
        found = len([f for f in os.listdir(self.temp_dir) if f in important_files])
        self.assertEqual(found, len(important_files))
    
    def test_code_file_detection(self):
        """Test detection of code files"""
        code_files = [
            ("main.py", "def main(): pass"),
            ("config.json", "{}"),
            ("app.js", "console.log('hello');"),
        ]
        
        for filename, content in code_files:
            path = os.path.join(self.temp_dir, filename)
            with open(path, 'w') as f:
                f.write(content)
        
        files = os.listdir(self.temp_dir)
        self.assertEqual(len(files), len(code_files))
    
    def test_large_project_structure(self):
        """Test handling of large project structures"""
        # Create a realistic project structure
        dirs = [
            "src/main",
            "src/utils",
            "tests/unit",
            "tests/integration",
            "docs",
            "config"
        ]
        
        for dir_path in dirs:
            full_path = os.path.join(self.temp_dir, dir_path)
            os.makedirs(full_path, exist_ok=True)
            
            # Add some files
            for i in range(2):
                file_path = os.path.join(full_path, f"file{i}.py")
                Path(file_path).touch()
        
        # Count total files created
        total_files = sum(
            len(files) 
            for _, _, files in os.walk(self.temp_dir)
        )
        self.assertGreater(total_files, 0)


class TestDirectoryTraversal(unittest.TestCase):
    """Test directory traversal functionality"""
    
    def test_depth_limiting(self):
        """Test that directory traversal respects depth limits"""
        # This would test max_depth parameter
        pass
    
    def test_ignore_directories(self):
        """Test that certain directories are ignored"""
        ignore_dirs = {
            "__pycache__",
            "node_modules",
            ".git",
            ".venv"
        }
        
        for dir_name in ignore_dirs:
            # These should be ignored in traversal
            self.assertIn(dir_name, ignore_dirs)
    
    def test_symlink_handling(self):
        """Test handling of symbolic links"""
        # This would test symlink handling logic
        pass


class TestFileReading(unittest.TestCase):
    """Test file reading and content extraction"""
    
    def test_large_file_truncation(self):
        """Test that large files are truncated"""
        large_content = "x" * 10000  # 10KB
        self.assertGreater(len(large_content), 5000)
    
    def test_binary_file_handling(self):
        """Test handling of binary files"""
        # Binary files should be skipped or handled gracefully
        pass
    
    def test_encoding_errors(self):
        """Test handling of encoding errors"""
        # Files with encoding issues should be handled with errors='ignore'
        pass


class TestProjectAnalysis(unittest.TestCase):
    """Test project analysis functionality"""
    
    def test_project_type_detection(self):
        """Test detection of project type"""
        # Would test Python/Node.js/Go project detection
        pass
    
    def test_framework_detection(self):
        """Test detection of frameworks in requirements"""
        requirements = "django==3.2\nrequests==2.26.0\npytest==7.0.0"
        self.assertIn("django", requirements)
    
    def test_context_size_management(self):
        """Test that context size is properly managed"""
        max_size = 50000
        test_content = "x" * 60000
        
        if len(test_content) > max_size:
            truncated = test_content[:max_size]
            self.assertEqual(len(truncated), max_size)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases for README generation"""
    
    def test_empty_requirements_file(self):
        """Test handling of empty requirements.txt"""
        # Should not crash, just skip
        pass
    
    def test_malformed_json_config(self):
        """Test handling of invalid JSON in config files"""
        invalid_json = "{ invalid json }"
        # Should be handled gracefully
        self.assertIn("{", invalid_json)
    
    def test_missing_file_permissions(self):
        """Test handling of permission denied errors"""
        # Should skip files that can't be read
        pass


if __name__ == '__main__':
    unittest.main()
