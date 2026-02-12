#!/usr/bin/env python3
"""
Insert AI-generated docstrings into Python files.
Usage: python insert_docstrings_auto.py <filename.py>
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Load DocstringAgent module
import importlib.util
spec = importlib.util.spec_from_file_location('docstring_agent', 'docstring-agent/docstring_agent.py')
docstring_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docstring_agent_module)
DocstringAgent = docstring_agent_module.DocstringAgent

# Validate filename argument
if len(sys.argv) < 2:
    print("Usage: python insert_docstrings_auto.py <filename>")
    print("Example: python insert_docstrings_auto.py 1.py")
    sys.exit(1)

filename = sys.argv[1]

# Check if file exists
if not os.path.exists(filename):
    print(f"❌ Error: File '{filename}' not found!")
    sys.exit(1)

print("=" * 60)
print(f"🚀 INSERTING DOCSTRINGS INTO {filename}")
print("=" * 60)

# Create agent in dry-run mode (no API key needed)
agent = DocstringAgent(dry_run=True)

# Generate and insert docstrings
print(f"\n📝 Processing {filename}...")
result = agent.process_file(filename)

# Save updated code to file
with open(filename, 'w') as f:
    f.write(result)

print(f"✅ Successfully inserted docstrings into {filename}!")
print("\n📄 Updated code:")
print("-" * 60)
print(result)
print("-" * 60)
print("\n✨ Done!")
