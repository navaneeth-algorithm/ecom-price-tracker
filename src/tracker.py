#!/usr/bin/env python3
"""
Price Tracker CLI Entry Point
Main command-line interface for the E-commerce Price Tracker
Supports check, view, add, and interactive commands
"""

# Import all CLI functionality from cli_app
from cli_app import (
    setup_argparse,
    run_check_command,
    view_products_cli,
    quick_add_product,
    main
)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Execute based on command
    if args.command == 'check':
        # Check command: Scrape all products and check for price drops
        run_check_command()
    elif args.command == 'view':
        # View command: Display all tracked products
        view_products_cli()
    elif args.command == 'add':
        # Quick add mode
        quick_add_product()
    else:
        # Full interactive CLI mode (default)
        main()
