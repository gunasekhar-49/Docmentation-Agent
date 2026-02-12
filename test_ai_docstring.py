#!/usr/bin/env python3
"""
Test script to verify AI docstring generation is working.
"""

import sys
import os
sys.path.insert(0, os.getcwd())

# Import the agent using direct module loading
import importlib.util
spec = importlib.util.spec_from_file_location('docstring_agent', 'docstring-agent/docstring_agent.py')
docstring_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docstring_agent_module)
DocstringAgent = docstring_agent_module.DocstringAgent

# Check if API key is available
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ERROR: ANTHROPIC_API_KEY not set!")
    print("Please set your API key:")
    print("  - Windows (PowerShell): $env:ANTHROPIC_API_KEY='your_key'")
    print("  - Windows (CMD): set ANTHROPIC_API_KEY=your_key")
    print("  - Or create a .env file with: ANTHROPIC_API_KEY=your_key")
    sys.exit(1)

print("✅ API key found!")

# Test with dry-run first (no API call)
print("\n🔧 Testing DRY-RUN mode (template-based, no API call)...")
agent_dry = DocstringAgent(dry_run=True)
result_dry = agent_dry.process_file('1.py')
print("✅ DRY-RUN successful! Generated docstrings:")
print(result_dry[:500])

# Test with real API
print("\n🚀 Testing REAL AI mode (with Claude API)...")
try:
    agent_real = DocstringAgent(dry_run=False)
    result_real = agent_real.process_file('1.py')
    print("✅ REAL AI successful! Generated docstrings with Claude:")
    print(result_real[:500])
except Exception as e:
    print(f"❌ ERROR with real API: {e}")
    print("Check your API key and internet connection")
    sys.exit(1)

print("\n✅ All tests passed! AI docstring generation is working!")
