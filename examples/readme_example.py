"""
Example usage of the README Generation Agent.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from readme_agent.readme_agent import ReadmeAgent


def example_readme_generation():
    """
    Demonstrate the README Generation Agent.
    
    This example shows how to:
    1. Initialize the agent
    2. Analyze a project directory
    3. Generate a comprehensive README
    """
    
    # Initialize agent
    agent = ReadmeAgent()
    
    # Example 1: Analyze project structure
    print("=" * 60)
    print("Example 1: Analyzing project structure")
    print("=" * 60)
    
    project_dir = os.path.dirname(os.path.dirname(__file__))
    
    try:
        project_info = agent.gather_project_info(project_dir)
        
        print(f"Project name: {project_info['project_name']}\n")
        print("Directory structure:")
        print(project_info['directory_structure'])
        
        print("\nImportant files found:")
        for filename in project_info['important_files'].keys():
            print(f"  - {filename}")
        
        print("\nCode files analyzed:")
        for filepath in project_info['code_samples'].keys():
            print(f"  - {filepath}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Generate README
    print("\n" + "=" * 60)
    print("Example 2: Generating README")
    print("=" * 60)
    
    try:
        readme = agent.process_directory(project_dir)
        print("README generated successfully!")
        print("\nPreview (first 1000 chars):")
        print(readme[:1000])
        if len(readme) > 1000:
            print("...")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    example_readme_generation()
