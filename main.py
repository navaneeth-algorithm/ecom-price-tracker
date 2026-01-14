#!/usr/bin/env python3
"""
E-Commerce Price Tracker - Main Entry Point

This is the main entry point for the price tracker application.
Run this script to access all CLI commands.

Usage:
    python main.py view      # View all tracked products
    python main.py add       # Add a new product
    python main.py check     # Check prices now
    python main.py --help    # Show help
"""

import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from src.tracker import main

if __name__ == '__main__':
    main()
