"""
Docstring Generation Agent

An intelligent AI agent that automatically generates clear, meaningful, and
comprehensive docstrings for Python functions, classes, and methods using Claude API.
"""

import os
import re
import ast
from typing import Optional, Dict, List, Tuple, Callable
import concurrent.futures

try:
    import anthropic
except Exception:
    anthropic = None  # allow operation in environments without the package


class DocstringAgent:
    """
    An AI-powered agent that generates docstrings for Python code.
    
    This agent analyzes Python source code and uses Claude to generate
    comprehensive docstrings following Google-style format. It handles
    functions, classes, methods, and async variants.
    
    Attributes:
        client: Anthropic API client instance
        model: Claude model to use for generation (default: claude-3-5-sonnet-20241022)
        temperature: Temperature for API calls (default: 0.7)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        client: Optional[object] = None,
        docstring_style: str = "google",
        dry_run: bool = False,
    ):
        """
        Initialize the Docstring Agent.
        
        Args:
            api_key: Optional Anthropic API key. If not provided, uses ANTHROPIC_API_KEY env var
            model: Claude model to use for generation
            
        Raises:
            ValueError: If API key is not provided and not set in environment
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.temperature = 0.7
        self.docstring_style = docstring_style.lower()
        self.dry_run = bool(dry_run)

        # Dependency injection: use provided client if available (helps testing/mocking)
        if client is not None:
            self.client = client
        else:
            # If dry_run is enabled, we allow no API client to be present
            if self.dry_run:
                self.client = None
            else:
                if anthropic is None:
                    # Allow instantiation in environments without the Anthropic package
                    self.client = None
                else:
                    if not self.api_key:
                        raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")
                    self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def read_file(self, file_path: str) -> str:
        """
        Read and return the contents of a Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            File contents as string
            
        Raises:
            FileNotFoundError: If file does not exist
            IOError: If file cannot be read
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_functions_and_classes(self, code: str) -> List[Dict]:
        """
        Extract all functions and classes from Python code using AST.
        
        Args:
            code: Python source code as string
            
        Returns:
            List of dictionaries containing:
                - type: "function", "class", or "method"
                - name: Name of the function/class
                - lineno: Line number where it's defined
                - code: Source code snippet
                - args: Function arguments (for functions/methods)
                
        Raises:
            SyntaxError: If code is not valid Python
        """
        results = []
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise SyntaxError(f"Invalid Python code: {e}")
        
        lines = code.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                # Skip methods - we'll handle them separately
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                    
                # Get function signature
                args = [arg.arg for arg in node.args.args]
                
                # Get source code snippet
                start_line = node.lineno - 1
                end_line = node.end_lineno or node.lineno
                code_snippet = '\n'.join(lines[start_line:end_line])
                
                # Check if it has existing docstring
                has_docstring = bool(ast.get_docstring(node))
                
                results.append({
                    'type': 'async_function' if isinstance(node, ast.AsyncFunctionDef) else 'function',
                    'name': node.name,
                    'lineno': node.lineno,
                    'code': code_snippet,
                    'args': args,
                    'has_docstring': has_docstring,
                    'node': node
                })
            
            elif isinstance(node, ast.ClassDef):
                # Get source code snippet
                start_line = node.lineno - 1
                end_line = node.end_lineno or node.lineno
                code_snippet = '\n'.join(lines[start_line:end_line])
                
                has_docstring = bool(ast.get_docstring(node))
                
                results.append({
                    'type': 'class',
                    'name': node.name,
                    'lineno': node.lineno,
                    'code': code_snippet,
                    'has_docstring': has_docstring,
                    'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                    'node': node
                })
        
        return results
    
    def generate_docstring(self, code_snippet: str, element_type: str, name: str) -> str:
        """
        Generate a docstring for a code element using Claude.
        
        Args:
            code_snippet: The source code to document
            element_type: Type of element ("function", "class", "method", "async_function")
            name: Name of the element
            
        Returns:
            Generated docstring in Google-style format
        """
        # Choose template based on requested style
        style = self.docstring_style
        if style not in ("google", "numpy"):
            style = "google"

        prompt = f"""You are an expert Python developer. Generate a comprehensive {style.title()}-style docstring for the following {element_type}.

IMPORTANT RULES:
1. Use Google-style docstring format
2. Be concise but informative
3. Include Args, Returns, Raises sections when applicable
4. For classes, describe the purpose and key attributes
5. Do NOT include the code in the docstring
6. Do NOT include triple quotes in your response
7. Match the indentation of the original code

{element_type.upper()} NAME: {name}
{element_type.upper()} CODE:
```python
{code_snippet}
```

Generate ONLY the docstring content (without triple quotes). The docstring should be ready to insert directly after the function/class definition line."""

        # If dry_run is enabled or no client is available, return a local fallback
        if self.dry_run or self.client is None:
            return self._local_docstring_template(code_snippet, element_type, name, style)

        # Otherwise call the provided client
        # Support both Anthropic-like and simple client interfaces (duck-typed)
        try:
            if hasattr(self.client, 'messages'):
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}],
                )
                # Anthropic client returns nested content in some SDKs
                try:
                    return message.content[0].text.strip()
                except Exception:
                    return str(message).strip()
            elif callable(self.client):
                # If client is a callable (mock), call it with the prompt
                return str(self.client(prompt)).strip()
            elif hasattr(self.client, 'create'):
                # OpenAI-like interface
                resp = self.client.create(prompt=prompt)
                return str(resp).strip()
            else:
                return self._local_docstring_template(code_snippet, element_type, name, style)
        except Exception:
            # On any API error, fall back to local template to avoid breaking the flow
            return self._local_docstring_template(code_snippet, element_type, name, style)

    def _local_docstring_template(self, code_snippet: str, element_type: str, name: str, style: str) -> str:
        """Create a simple, deterministic docstring template as a fallback (dry-run or on API failure)."""
        # Basic heuristic: extract args from snippet using AST when possible
        args = []
        try:
            node = ast.parse(code_snippet)
            for n in ast.walk(node):
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [a.arg for a in n.args.args]
                    break
        except Exception:
            args = []

        if style == 'numpy':
            parts = [f"{name}.", "", "Parameters", "----------"]
            for a in args:
                parts.append(f"{a} : Any\n    Description.")
            parts.append("\nReturns\n-------\nAny\n    Description.")
            return "\n".join(parts)
        else:
            # Google-style
            parts = [f"Brief description of {name}.", ""]
            if args:
                parts.append("Args:")
                for a in args:
                    parts.append(f"    {a} (Any): Description of {a}.")
            parts.append("\nReturns:\n    Any: Description of return value.")
            return "\n".join(parts)
    
    def process_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        Process a Python file and generate docstrings for all functions and classes.
        
        Args:
            file_path: Path to the Python file to process
            output_path: Optional path to save the modified file. If None, returns as string
            
        Returns:
            Modified Python code with generated docstrings
            
        Raises:
            FileNotFoundError: If input file does not exist
            SyntaxError: If file contains invalid Python
        """
        code = self.read_file(file_path)
        elements = self.extract_functions_and_classes(code)
        
        # Sort elements by line number in reverse order for safe insertion
        elements_sorted = sorted(elements, key=lambda x: x['lineno'], reverse=True)
        
        lines = code.split('\n')
        
        for element in elements_sorted:
            if element['has_docstring']:
                continue  # Skip elements that already have docstrings

            # Generate docstring
            docstring = self.generate_docstring(element['code'], element['type'], element['name'])

            # Format docstring for insertion
            lineno = element['lineno'] - 1
            # If the definition line does not end with ':' (e.g., one-liner like "def f(): pass"), skip
            if not lines[lineno].rstrip().endswith(':'):
                # Conservative: skip injecting into one-line defs to avoid breaking code
                continue

            indent = len(lines[lineno]) - len(lines[lineno].lstrip()) + 4
            # Use 4-space deeper indentation for the docstring block
            indent_str = ' ' * indent

            # Build a multi-line, properly-indented docstring block
            doc_lines = docstring.split('\n') if docstring else [f"Brief description of {element['name']}."]
            formatted_lines = [indent_str + '"""'] + [indent_str + l for l in doc_lines] + [indent_str + '"""']

            insert_line = lineno + 1
            # Insert the formatted lines into the file
            for offset, l in enumerate(formatted_lines):
                lines.insert(insert_line + offset, l)
        
        result = '\n'.join(lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
        
        return result
    
    def batch_process_directory(
        self,
        directory: str,
        output_directory: Optional[str] = None,
        use_concurrency: bool = False,
        max_workers: Optional[int] = None,
        ignore_dirs: Optional[List[str]] = None,
    ) -> Dict[str, str]:
        """
        Process all Python files in a directory recursively.
        
        Args:
            directory: Path to directory containing Python files
            output_directory: Optional directory to save modified files
            
        Returns:
            Dictionary mapping file paths to processed code
        """
        results = {}

        # Prepare ignore list and ensure outputs are not re-traversed
        default_ignores = ['.venv', 'venv', '.git', 'node_modules', '__pycache__', 'output_docs']
        ignore_dirs = list(ignore_dirs or [])
        for d in default_ignores:
            if d not in ignore_dirs:
                ignore_dirs.append(d)

        file_paths = []
        for root, dirs, files in os.walk(directory):
            # Mutate dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith('.py') and not file.startswith('__pycache__'):
                    file_paths.append(os.path.join(root, file))

        def _process(file_path: str) -> Tuple[str, Optional[str]]:
            try:
                processed = self.process_file(file_path)
                if output_directory:
                    rel_path = os.path.relpath(file_path, directory)
                    output_path = os.path.join(output_directory, rel_path)
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(processed)
                return file_path, processed
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                return file_path, None

        if use_concurrency and len(file_paths) > 1:
            workers = max_workers or min(32, (os.cpu_count() or 1) + 4)
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
                futures = {ex.submit(_process, fp): fp for fp in file_paths}
                for fut in concurrent.futures.as_completed(futures):
                    fp, processed = fut.result()
                    if processed is not None:
                        results[fp] = processed
        else:
            for fp in file_paths:
                fp, processed = _process(fp)
                if processed is not None:
                    results[fp] = processed
        
        return results


def main():
    """Example usage of the Docstring Agent."""
    agent = DocstringAgent()
    
    # Example: Process a single file
    test_file = "example.py"
    if os.path.exists(test_file):
        result = agent.process_file(test_file)
        print(result)


if __name__ == "__main__":
    main()
