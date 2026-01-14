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

from src.cli_app import (
    setup_argparse,
    run_check_command,
    view_products_cli,
    quick_add_product,
    main as interactive_main,
)


if __name__ == '__main__':
    # Mirror the CLI dispatch used in src/tracker.py so `python main.py <cmd>` works
    parser = setup_argparse()
    args = parser.parse_args()

    if args.command == 'check':
        run_check_command()
    elif args.command == 'view':
        view_products_cli()
    elif args.command == 'add':
        quick_add_product()
    else:
        interactive_main()
