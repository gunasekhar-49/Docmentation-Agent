#!/usr/bin/env python3
"""
Universal Docstring Inserter Script
Insert docstrings into ANY Python file automatically.
Usage: python insert_docstrings_auto.py <filename>
"""

import sys
import os

sys.path.insert(0, os.getcwd())

import importlib.util
spec = importlib.util.spec_from_file_location('docstring_agent', 'docstring-agent/docstring_agent.py')
docstring_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docstring_agent_module)
DocstringAgent = docstring_agent_module.DocstringAgent

# Get filename from command line argument
if len(sys.argv) < 2:
    print("Usage: python insert_docstrings_auto.py <filename>")
    print("Example: python insert_docstrings_auto.py 1.py")
    print("         python insert_docstrings_auto.py 2.py")
    print("         python insert_docstrings_auto.py 3.py")
    sys.exit(1)

filename = sys.argv[1]

# Check if file exists
if not os.path.exists(filename):
    print(f"❌ Error: File '{filename}' not found!")
    sys.exit(1)

print("=" * 60)
print(f"🚀 INSERTING DOCSTRINGS INTO {filename}")
print("=" * 60)

# Use dry-run mode (works without API key)
agent = DocstringAgent(dry_run=True)

# Generate docstrings with insertions
print(f"\n📝 Processing {filename}...")
result = agent.process_file(filename)

# Save the result back to the file
with open(filename, 'w') as f:
    f.write(result)

print(f"✅ Successfully inserted docstrings into {filename}!")
print("\n📄 Updated code:")
print("-" * 60)
print(result)
print("-" * 60)

print("\n✨ Done! Your code now has automatic AI-generated docstrings!")
