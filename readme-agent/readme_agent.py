"""
README Generation Agent

An intelligent AI agent that analyzes project structures and automatically
generates comprehensive README.md files using Claude API.
"""

import os
import json
from typing import Optional, Dict, List, Tuple
import anthropic


class ReadmeAgent:
    """
    An AI-powered agent that generates comprehensive README files.
    
    This agent analyzes a project directory structure, reads relevant files,
    and uses Claude to generate a cohesive README.md that documents the
    entire project including purpose, structure, usage, and features.
    
    Attributes:
        client: Anthropic API client instance
        model: Claude model to use for generation (default: claude-3-5-sonnet-20241022)
        max_context_chars: Maximum characters to include in analysis (prevents token overflow)
    """
    
    IMPORTANT_FILES = {
        'setup.py', 'setup.cfg', 'pyproject.toml',
        'requirements.txt', 'Pipfile', 'poetry.lock',
        'package.json', 'package-lock.json',
        'Dockerfile', 'docker-compose.yml',
        'config.yaml', 'config.json', '.env.example',
        'LICENSE', 'CONTRIBUTING.md'
    }
    
    CODE_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java', '.cpp', '.c', '.h'}
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize the README Agent.
        
        Args:
            api_key: Optional Anthropic API key. If not provided, uses ANTHROPIC_API_KEY env var
            model: Claude model to use for generation
            
        Raises:
            ValueError: If API key is not provided and not set in environment
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        self.temperature = 0.7
        self.max_context_chars = 50000  # ~12.5K tokens max for context
    
    def get_directory_structure(self, directory: str, max_depth: int = 3, current_depth: int = 0, 
                               prefix: str = "", ignore_dirs: Optional[set] = None) -> str:
        """
        Generate a tree-like directory structure.
        
        Args:
            directory: Path to directory to analyze
            max_depth: Maximum depth to traverse (default: 3)
            current_depth: Current depth level (internal use)
            prefix: Prefix for tree formatting (internal use)
            ignore_dirs: Set of directory names to ignore
            
        Returns:
            String representation of directory tree
        """
        if ignore_dirs is None:
            ignore_dirs = {
                '__pycache__', '.git', '.venv', 'venv', 'node_modules',
                '.pytest_cache', 'build', 'dist', '.egg-info', '.tox'
            }
        
        if current_depth >= max_depth:
            return ""
        
        try:
            items = os.listdir(directory)
        except PermissionError:
            return ""
        
        # Filter and sort items
        items = [item for item in items if item not in ignore_dirs and not item.startswith('.')]
        items.sort()
        
        structure = ""
        for i, item in enumerate(items):
            path = os.path.join(directory, item)
            is_last = i == len(items) - 1
            
            current_prefix = "└── " if is_last else "├── "
            structure += f"{prefix}{current_prefix}{item}\n"
            
            if os.path.isdir(path):
                extension = "    " if is_last else "│   "
                structure += self.get_directory_structure(
                    path, max_depth, current_depth + 1, prefix + extension, ignore_dirs
                )
        
        return structure
    
    def read_important_files(self, directory: str) -> Dict[str, str]:
        """
        Read important project files like requirements, config, etc.
        
        Args:
            directory: Path to project directory
            
        Returns:
            Dictionary mapping filename to file contents
        """
        contents = {}
        
        for file in self.IMPORTANT_FILES:
            path = os.path.join(directory, file)
            if os.path.exists(path) and os.path.isfile(path):
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Limit file size
                        if len(content) > 5000:
                            content = content[:5000] + "\n... (truncated)"
                        contents[file] = content
                except Exception as e:
                    contents[file] = f"Error reading: {e}"
        
        return contents
    
    def analyze_code_files(self, directory: str, max_files: int = 10) -> Dict[str, str]:
        """
        Analyze key code files to understand project purpose.
        
        Args:
            directory: Path to project directory
            max_files: Maximum number of code files to analyze
            
        Returns:
            Dictionary mapping file path to code snippet
        """
        code_files = {}
        count = 0
        
        for root, dirs, files in os.walk(directory):
            # Skip common unimportant directories
            dirs[:] = [d for d in dirs if d not in {
                '__pycache__', '.git', '.venv', 'venv', 'node_modules',
                '.pytest_cache', 'build', 'dist', '.egg-info'
            }]
            
            for file in sorted(files):
                if count >= max_files:
                    break
                
                if any(file.endswith(ext) for ext in self.CODE_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # Limit file size
                            if len(content) > 2000:
                                content = content[:2000] + "\n... (truncated)"
                            code_files[relative_path] = content
                            count += 1
                    except Exception as e:
                        code_files[relative_path] = f"Error reading: {e}"
        
        return code_files
    
    def gather_project_info(self, directory: str) -> Dict:
        """
        Gather comprehensive information about a project.
        
        Args:
            directory: Path to project directory
            
        Returns:
            Dictionary containing project analysis
        """
        if not os.path.isdir(directory):
            raise ValueError(f"Directory does not exist: {directory}")
        
        return {
            'directory_structure': self.get_directory_structure(directory),
            'important_files': self.read_important_files(directory),
            'code_samples': self.analyze_code_files(directory),
            'project_name': os.path.basename(directory.rstrip(os.sep))
        }
    
    def generate_readme(self, project_info: Dict) -> str:
        """
        Generate a comprehensive README using Claude.
        
        Args:
            project_info: Dictionary containing project information from gather_project_info
            
        Returns:
            Generated README.md content
        """
        # Build context with size limits
        context_parts = [
            f"# Project Analysis for: {project_info['project_name']}\n",
            "## Directory Structure\n",
            f"{project_info['directory_structure']}\n"
        ]
        
        if project_info['important_files']:
            context_parts.append("## Important Files\n")
            for filename, content in project_info['important_files'].items():
                context_parts.append(f"### {filename}\n```\n{content}\n```\n")
        
        if project_info['code_samples']:
            context_parts.append("## Code Samples\n")
            for filepath, content in project_info['code_samples'].items():
                context_parts.append(f"### {filepath}\n```\n{content}\n```\n")
        
        context = '\n'.join(context_parts)
        
        # Truncate if too large
        if len(context) > self.max_context_chars:
            context = context[:self.max_context_chars] + "\n... (context truncated)"
        
        prompt = f"""Based on the following project analysis, generate a comprehensive, professional README.md file.

PROJECT ANALYSIS:
{context}

IMPORTANT REQUIREMENTS:
1. Create a well-structured README with clear sections
2. Include a descriptive title and brief overview
3. Document features, installation, usage, project structure
4. Add sections for requirements, configuration, and contributing if applicable
5. Include badges for any frameworks/languages detected
6. Make it engaging and professional
7. Use proper Markdown formatting
8. Include examples where relevant
9. Be specific to the project based on the analysis

REQUIRED SECTIONS (if applicable):
- Title and Description
- Features
- Installation/Setup
- Usage/Getting Started
- Project Structure
- Configuration
- Requirements/Dependencies
- Contributing
- License

Generate ONLY the README.md content, starting with the title. Do not include any explanations outside the README."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=self.temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text.strip()
    
    def process_directory(self, directory: str, output_path: str = "README.md") -> str:
        """
        Generate README for a directory and optionally save it.
        
        Args:
            directory: Path to project directory
            output_path: Path where README.md will be saved
            
        Returns:
            Generated README content
        """
        # Gather project information
        project_info = self.gather_project_info(directory)
        
        # Generate README
        readme = self.generate_readme(project_info)
        
        # Save to file
        output_file = os.path.join(directory, output_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(readme)
        
        return readme


def main():
    """Example usage of the README Agent."""
    agent = ReadmeAgent()
    
    # Example: Process current directory
    current_dir = os.getcwd()
    readme = agent.process_directory(current_dir)
    print("Generated README:")
    print(readme)


if __name__ == "__main__":
    main()
