#!/usr/bin/env python3
"""
Universal README Generator Script
Generate README for ANY project directory automatically.
Usage: python generate_readme_auto.py <directory>
"""

import sys
import os

sys.path.insert(0, os.getcwd())

import importlib.util
spec = importlib.util.spec_from_file_location('readme_agent', 'readme-agent/readme_agent.py')
readme_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readme_agent_module)
ReadmeAgent = readme_agent_module.ReadmeAgent

# Get directory from command line argument
directory = sys.argv[1] if len(sys.argv) > 1 else '.'

# Check if directory exists
if not os.path.isdir(directory):
    print(f"❌ Error: Directory '{directory}' not found!")
    sys.exit(1)

print("=" * 60)
print(f"🚀 GENERATING README FOR {directory}")
print("=" * 60)

# Create README agent
agent = ReadmeAgent(dry_run=True)

# Generate README
print(f"\n📝 Analyzing {directory}...")
readme_content = agent.generate_readme(directory)

# Save the README
readme_path = os.path.join(directory, 'README.md')
with open(readme_path, 'w') as f:
    f.write(readme_content)

print(f"✅ Successfully generated README.md in {directory}!")
print("\n📄 Generated README:")
print("-" * 60)
print(readme_content)
print("-" * 60)

print("\n✨ Done! Your project now has an AI-generated README!")
