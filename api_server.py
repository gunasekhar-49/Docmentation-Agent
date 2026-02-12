#!/usr/bin/env python3
"""
Web API server for AI docstring and README generation.
Start: python api_server.py
Access: http://localhost:8001/docs (Swagger UI)
"""

import sys
import os
sys.path.insert(0, os.getcwd())

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import importlib.util
import tempfile
import shutil
from pathlib import Path

# Load DocstringAgent
spec = importlib.util.spec_from_file_location('docstring_agent', 'docstring-agent/docstring_agent.py')
docstring_agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docstring_agent_module)
DocstringAgent = docstring_agent_module.DocstringAgent

# Load ReadmeAgent
spec_readme = importlib.util.spec_from_file_location('readme_agent', 'readme-agent/readme_agent.py')
readme_agent_module = importlib.util.module_from_spec(spec_readme)
spec_readme.loader.exec_module(readme_agent_module)
ReadmeAgent = readme_agent_module.ReadmeAgent

# Create FastAPI app with Swagger UI
app = FastAPI(
    title="AI Docstring Generator",
    description="Upload Python files and get AI-generated docstrings automatically!",
    version="1.0.0"
)

# Initialize agents
agent = DocstringAgent(dry_run=True)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize the agent with dry-run mode
agent = DocstringAgent(dry_run=True)

# Create a temporary directory for uploads
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint - returns API info"""
    return {
        "name": "AI Docstring Generator API",
        "description": "Upload Python files to generate docstrings AND README automatically",
        "endpoints": {
            "swagger_ui": "http://localhost:8000/docs",
            "upload_file": "POST /upload - Single file docstrings",
            "batch_files": "POST /batch - Multiple files docstrings",
            "process_code": "POST /process-code - Paste code directly",
            "generate_readme": "POST /generate-readme - Generate README for directory",
            "batch_with_readme": "POST /batch-with-readme - Files + README generation"
        }
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a Python file and get docstrings generated automatically.
    
    Args:
        file: Python file to process
        
    Returns:
        JSON with generated code and docstrings
    """
    try:
        # Validate file type
        if not file.filename.endswith('.py'):
            raise HTTPException(status_code=400, detail="Only .py files are supported")
        
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Generate docstrings
        result = agent.process_file(str(file_path))
        
        return {
            "status": "success",
            "filename": file.filename,
            "original_code": content.decode('utf-8'),
            "generated_code": result,
            "message": "Docstrings generated successfully!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch")
async def batch_process(files: list[UploadFile] = File(...)):
    """
    Upload multiple Python files and get docstrings for all of them.
    
    Args:
        files: List of Python files to process
        
    Returns:
        JSON with results for each file
    """
    try:
        results = []
        
        for file in files:
            if not file.filename.endswith('.py'):
                results.append({
                    "filename": file.filename,
                    "status": "skipped",
                    "message": "Only .py files are supported"
                })
                continue
            
            # Save file
            file_path = UPLOAD_DIR / file.filename
            content = await file.read()
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Generate docstrings
            try:
                generated = agent.process_file(str(file_path))
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "original_code": content.decode('utf-8'),
                    "generated_code": generated
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "status": "success",
            "total_files": len(files),
            "processed": len([r for r in results if r["status"] == "success"]),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-code")
async def process_code(code: str):
    """
    Process Python code directly (paste code instead of uploading).
    
    Args:
        code: Python code as string
        
    Returns:
        JSON with generated code and docstrings
    """
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        # Generate docstrings
        result = agent.process_file(temp_path)
        
        # Clean up
        os.unlink(temp_path)
        
        return {
            "status": "success",
            "original_code": code,
            "generated_code": result,
            "message": "Docstrings generated successfully!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-readme")
async def generate_readme(directory: str = "."):
    """
    Generate README file for a project directory.
    
    Args:
        directory: Directory path to analyze (default: current directory)
        
    Returns:
        JSON with generated README content
    """
    try:
        # Create README agent
        readme_agent = ReadmeAgent(dry_run=True)
        
        # Generate README
        readme_content = readme_agent.generate_readme(directory)
        
        return {
            "status": "success",
            "directory": directory,
            "readme_content": readme_content,
            "message": "README generated successfully!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-with-readme")
async def batch_with_readme(files: list[UploadFile] = File(...)):
    """
    Upload multiple Python files and generate both docstrings AND README.
    
    Args:
        files: List of Python files to process
        
    Returns:
        JSON with results for each file plus generated README
    """
    try:
        results = []
        temp_dir = tempfile.mkdtemp()
        
        # Process each file
        for file in files:
            if not file.filename.endswith('.py'):
                results.append({
                    "filename": file.filename,
                    "status": "skipped",
                    "message": "Only .py files are supported"
                })
                continue
            
            # Save file to temp directory
            file_path = Path(temp_dir) / file.filename
            content = await file.read()
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # Generate docstrings
            try:
                generated = agent.process_file(str(file_path))
                
                # Save generated code
                with open(file_path, 'w') as f:
                    f.write(generated)
                
                results.append({
                    "filename": file.filename,
                    "status": "success",
                    "original_code": content.decode('utf-8'),
                    "generated_code": generated
                })
            except Exception as e:
                results.append({
                    "filename": file.filename,
                    "status": "error",
                    "error": str(e)
                })
        
        # Generate README for the project
        try:
            readme_agent = ReadmeAgent(dry_run=True)
            readme_content = readme_agent.generate_readme(temp_dir)
        except Exception as e:
            readme_content = f"Error generating README: {str(e)}"
        
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return {
            "status": "success",
            "total_files": len(files),
            "processed": len([r for r in results if r["status"] == "success"]),
            "results": results,
            "readme": {
                "status": "generated",
                "content": readme_content
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 AI DOCSTRING & README GENERATOR API SERVER")
    print("=" * 60)
    print("\n✨ Server starting...")
    print("\n📖 Swagger UI: http://localhost:8001/docs")
    print("📊 ReDoc: http://localhost:8001/redoc")
    print("\n🔗 API Endpoints:")
    print("  - POST /upload           - Upload single Python file")
    print("  - POST /batch            - Upload multiple Python files")
    print("  - POST /process-code     - Paste code directly")
    print("  - POST /generate-readme  - Generate README for directory")
    print("  - POST /batch-with-readme - Files + README generation")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
