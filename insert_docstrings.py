#!/usr/bin/env python3
"""
Script to automatically insert docstrings into your Python code.
"""

import sys
import os
sys.path.insert(0, os.getcwd())

import importlib.util
spec = importlib.util.spec_from_file_location('docstring_agent', 'docstring-agent/docstring_agent.py')
docstring_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docstring_agent_module)
DocstringAgent = docstring_agent_module.DocstringAgent

print("=" * 60)
print("🚀 DOCSTRING AUTO-INSERT SCRIPT")
print("=" * 60)

# Use dry-run mode (works without API key)
agent = DocstringAgent(dry_run=True)

# Generate docstrings with insertions
print("\n📝 Processing 1.py...")
result = agent.process_file('1.py')

# Save the result back to the file
with open('1.py', 'w') as f:
    f.write(result)

print("✅ Successfully inserted docstrings into 1.py!")
print("\n📄 Updated code:")
print("-" * 60)
print(result)
print("-" * 60)

print("\n✨ Done! Your code now has automatic AI-generated docstrings!")
