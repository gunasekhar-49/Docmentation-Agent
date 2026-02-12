from docstring_agent.docstring_agent import DocstringAgent
import os

agent = DocstringAgent(dry_run=True)
path = os.path.join('examples','sample_code.py')
res = agent.process_file(path)
print('=== Preview (first 2000 chars) ===')
print(res[:2000])
