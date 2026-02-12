#!/usr/bin/env python3
"""
Test script to upload a file to the API and get docstrings
"""

import requests
import json
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/upload"

# File to upload
file_path = "1.py"

if not Path(file_path).exists():
    print(f"❌ Error: {file_path} not found!")
    exit(1)

print("=" * 60)
print("📤 UPLOADING FILE TO API")
print("=" * 60)

# Read the file
with open(file_path, 'rb') as f:
    files = {'file': (file_path, f, 'text/plain')}
    
    print(f"\n📁 Uploading {file_path}...")
    
    try:
        # Send request to API
        response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ Upload successful!")
            print("\n" + "=" * 60)
            print("📄 GENERATED CODE WITH DOCSTRINGS:")
            print("=" * 60)
            print(result['generated_code'])
            
            # Save the result to a new file
            output_file = f"output_{file_path}"
            with open(output_file, 'w') as out:
                out.write(result['generated_code'])
            
            print("\n" + "=" * 60)
            print(f"✨ Generated code saved to: {output_file}")
            print("=" * 60)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API!")
        print("Make sure the server is running: python api_server.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
