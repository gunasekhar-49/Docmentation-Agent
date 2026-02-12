import os
import sys
import importlib.util


# Dynamically load the docstring_agent module from the folder 'docstring-agent'
def load_docstring_agent():
    module_path = os.path.join(os.getcwd(), 'docstring-agent', 'docstring_agent.py')
    if not os.path.exists(module_path):
        raise FileNotFoundError(module_path)
    spec = importlib.util.spec_from_file_location('docstring_agent', module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.DocstringAgent


def main():
    DocstringAgent = load_docstring_agent()
    agent = DocstringAgent(dry_run=True)
    out_dir = os.path.join(os.getcwd(), "output_docs")
    ignore_list = ['.venv', 'venv', '.git', 'node_modules', '__pycache__', 'output_docs']
    results = agent.batch_process_directory('.', output_directory=out_dir, use_concurrency=True, max_workers=4, ignore_dirs=ignore_list)
    print(f"Processed {len(results)} files and wrote to: {out_dir}")
    for p in list(results)[:20]:
        print(f" - {p}")


if __name__ == '__main__':
    main()
