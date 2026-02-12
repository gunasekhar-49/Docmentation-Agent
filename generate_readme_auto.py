#!/usr/bin/env python3
"""
Generate README files for Python projects.
Usage: python generate_readme_auto.py <directory>
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Load ReadmeAgent module
import importlib.util
spec = importlib.util.spec_from_file_location('readme_agent', 'readme-agent/readme_agent.py')
readme_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readme_agent_module)
ReadmeAgent = readme_agent_module.ReadmeAgent

# Get directory from argument (default to current directory)
directory = sys.argv[1] if len(sys.argv) > 1 else '.'

# Check if directory exists
if not os.path.isdir(directory):
    print(f"❌ Error: Directory '{directory}' not found!")
    sys.exit(1)

print("=" * 60)
print(f"🚀 GENERATING README FOR {directory}")
print("=" * 60)

# Create README agent in dry-run mode
agent = ReadmeAgent(dry_run=True)

# Generate README content
print(f"\n📝 Analyzing {directory}...")
readme_content = agent.generate_readme(directory)

# Save README to file
readme_path = os.path.join(directory, 'README.md')
with open(readme_path, 'w') as f:
    f.write(readme_content)

print(f"✅ README.md generated successfully!")
print("\n📄 Generated README:")
print("-" * 60)
print(readme_content)
print("-" * 60)
print("\n✨ Done!")
