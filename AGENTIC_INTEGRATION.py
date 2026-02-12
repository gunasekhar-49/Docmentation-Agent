"""
================================================================================
AGENTIC TEMPLATE INTEGRATION
================================================================================

WHAT IS INCLUDED:
- app/agents.py: AI agent implementations (run_genai, run_agent2)
- app/config.py: Configuration settings
- app/models.py: Data models (ChatRequest, ChatResponse)
- app/tools.py: Tool definitions for agents
- app/__main__.py: FastAPI endpoints

HOW TO USE:
1. The agentic template provides AI agents powered by Google Gemini
2. Two main agents:
   - run_genai(): Direct API calls to Gemini
   - run_agent2(): Agentic framework with tools

INTEGRATION WITH YOUR PROJECT:
Your project has TWO main systems:

SYSTEM 1: Documentation Generation (Existing)
- DocstringAgent: Auto-generates docstrings
- ReadmeAgent: Auto-generates README files
- Use: python insert_docstrings_auto.py <file.py>
- Use: python generate_readme_auto.py <directory>

SYSTEM 2: Agentic AI (New - from template)
- AI agents with tool integration
- Conversational interface
- Flexible reasoning capabilities
- Use: FastAPI endpoints in app/__main__.py

COMBINED API SERVER:
You can now run BOTH systems in one API server!
- Existing endpoints: /upload, /batch, /process-code, /generate-readme
- New endpoints: /genai/chat, /genai/agent

================================================================================
"""

print(__doc__)
