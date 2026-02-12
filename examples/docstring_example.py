"""
Example usage of the Docstring Generation Agent.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from docstring_agent.docstring_agent import DocstringAgent


def example_docstring_generation():
    """
    Demonstrate the Docstring Generation Agent.
    
    This example shows how to:
    1. Initialize the agent
    2. Process a single file
    3. Process an entire directory
    """
    
    # Initialize agent
    agent = DocstringAgent()
    
    # Example 1: Process single file
    print("=" * 60)
    print("Example 1: Processing single file")
    print("=" * 60)
    
    sample_file = os.path.join(os.path.dirname(__file__), 'sample_code.py')
    if os.path.exists(sample_file):
        try:
            result = agent.process_file(sample_file)
            print("Successfully processed sample_code.py")
            print("\nGenerated code with docstrings:")
            print(result[:500] + "..." if len(result) > 500 else result)
        except Exception as e:
            print(f"Error: {e}")
    
    # Example 2: Extract functions and classes
    print("\n" + "=" * 60)
    print("Example 2: Extracting functions and classes")
    print("=" * 60)
    
    code = agent.read_file(sample_file)
    elements = agent.extract_functions_and_classes(code)
    
    print(f"Found {len(elements)} elements:\n")
    for elem in elements:
        print(f"  - {elem['type'].upper()}: {elem['name']} (line {elem['lineno']})")
        if 'args' in elem:
            print(f"    Args: {', '.join(elem['args']) if elem['args'] else 'None'}")
        if 'methods' in elem:
            print(f"    Methods: {', '.join(elem['methods'])}")
    
    # Example 3: Generate single docstring
    print("\n" + "=" * 60)
    print("Example 3: Generating docstring for specific function")
    print("=" * 60)
    
    test_code = """def calculate_total(items, tax_rate=0.1):
    subtotal = sum(item['price'] for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax"""
    
    try:
        docstring = agent.generate_docstring(test_code, "function", "calculate_total")
        print("Generated docstring:")
        print(f'    """{docstring}"""')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    example_docstring_generation()
