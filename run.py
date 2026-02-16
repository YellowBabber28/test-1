#!/usr/bin/env python3
"""
Run script for RA Automator
Usage: python run.py
"""
import sys
import os
from pathlib import Path

# Get project root directory
project_root = Path(__file__).parent.absolute()

# Add project root to Python path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Set PYTHONPATH environment variable for uvicorn reload
os.environ['PYTHONPATH'] = str(project_root)

# Change to project root directory
os.chdir(project_root)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root / "backend")]
    )
