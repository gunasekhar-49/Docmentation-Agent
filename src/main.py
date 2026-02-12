#!/usr/bin/env python3
"""
================================================================================
APPLICATION ENTRY POINT
================================================================================

Main application server that combines:
1. Documentation Generation (Docstring + README)
2. Agentic AI System (Gemini + Agents)

Start: python src/main.py
Access: http://localhost:8000/docs (Swagger UI)
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import importlib.util
import tempfile
import shutil
from pathlib import Path

# ============================================================================
# Load Documentation Agents
# ============================================================================

# Load DocstringAgent
spec = importlib.util.spec_from_file_location(
    'docstring_agent', 
    'docstring-agent/docstring_agent.py'
)
docstring_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docstring_agent_module)
DocstringAgent = docstring_agent_module.DocstringAgent

# Load ReadmeAgent
spec_readme = importlib.util.spec_from_file_location(
    'readme_agent', 
    'readme-agent/readme_agent.py'
)
readme_agent_module = importlib.util.module_from_spec(spec_readme)
spec_readme.loader.exec_module(readme_agent_module)
ReadmeAgent = readme_agent_module.ReadmeAgent

# ============================================================================
# Load Agentic AI Agents
# ============================================================================
try:
    from app.agents import run_genai, run_agent2
    from app.models import ChatRequest, ChatResponse
    agentic_loaded = True
except ImportError:
    print("⚠️  Warning: Agentic AI system not loaded")
    agentic_loaded = False

# ============================================================================
# Create FastAPI Application
# ============================================================================
app = FastAPI(
    title="Documentation + AI Agents API",
    description="Unified API: Auto-docstrings + Auto-README + AI Agents",
    version="1.0.0"
)

# Initialize agents
docstring_agent = DocstringAgent(dry_run=True)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ============================================================================
# DOCUMENTATION ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Documentation + AI Agents API",
        "version": "1.0.0",
        "systems": {
            "documentation": "Auto-generate docstrings and README files",
            "agentic_ai": "AI agents with Gemini API"
        },
        "endpoints": {
            "docs": "http://localhost:8000/docs",
            "redoc": "http://localhost:8000/redoc"
        }
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload Python file to generate docstrings"""
    try:
        if not file.filename.endswith('.py'):
            raise HTTPException(status_code=400, detail="Only .py files supported")
        
        file_path = UPLOAD_DIR / file.filename
        content = await file.read()
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        result = docstring_agent.process_file(str(file_path))
        
        return {
            "status": "success",
            "filename": file.filename,
            "original_code": content.decode('utf-8'),
            "generated_code": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch")
async def batch_process(files: list[UploadFile] = File(...)):
    """Upload multiple Python files for batch docstring generation"""
    try:
        results = []
        for file in files:
            if not file.filename.endswith('.py'):
                results.append({
                    "filename": file.filename,
                    "status": "skipped"
                })
                continue
            
            file_path = UPLOAD_DIR / file.filename
            content = await file.read()
            
            with open(file_path, 'wb') as f:
                f.write(content)
            
            try:
                generated = docstring_agent.process_file(str(file_path))
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "generated_code": generated
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-readme")
async def generate_readme(directory: str = "."):
    """Generate README for project directory"""
    try:
        readme_agent = ReadmeAgent(dry_run=True)
        readme_content = readme_agent.generate_readme(directory)
        
        return {
            "status": "success",
            "directory": directory,
            "readme_content": readme_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# AGENTIC AI ENDPOINTS
# ============================================================================

if agentic_loaded:
    @app.post("/genai/chat")
    async def chat_with_gemini(request: ChatRequest):
        """Chat with Gemini AI directly"""
        try:
            answer = run_genai(request.question)
            return ChatResponse(answer=answer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/genai/agent")
    async def chat_with_agent(request: ChatRequest):
        """Use agentic framework with tools"""
        try:
            answer = run_agent2(request.question)
            return ChatResponse(answer=answer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 70)
    print("🚀 DOCUMENTATION + AI AGENTS API SERVER")
    print("=" * 70)
    
    print("\n📚 DOCUMENTATION SYSTEM")
    print("  ✓ POST /upload - Generate docstrings for single file")
    print("  ✓ POST /batch - Generate docstrings for multiple files")
    print("  ✓ POST /generate-readme - Generate project README")
    
    if agentic_loaded:
        print("\n🤖 AGENTIC AI SYSTEM")
        print("  ✓ POST /genai/chat - Direct Gemini API")
        print("  ✓ POST /genai/agent - Agentic framework")
    
    print("\n📖 Swagger UI: http://localhost:8000/docs")
    print("📊 ReDoc: http://localhost:8000/redoc")
    print("=" * 70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
