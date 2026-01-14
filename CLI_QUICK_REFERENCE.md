# E-commerce Price Tracker - CLI Quick Reference

## Available Commands

### View All Tracked Products
```bash
python cli_app.py view
```
Displays a formatted table with:
- Product number
- Product name (truncated if long)
- Latest recorded price with currency
- Last updated timestamp
- Full product URL

### Add New Product (Quick Mode)
```bash
python cli_app.py add
```
Prompts for:
- Product URL (required)
- Product name (optional, auto-generated if empty)
- Category (default: Electronics)
- Confirmation before adding

### Interactive Menu (Default)
```bash
python cli_app.py
# or
python cli_app.py interactive
```
Shows full menu with options:
1. Add Product
2. List Products
3. View Price History
4. Remove Product
5. Exit

### Show Help
```bash
python cli_app.py --help
```

## Examples

### Example 1: View all products
```bash
$ python cli_app.py view

🔍 Fetching tracked products...
✓ Retrieved 4 unique product(s) with latest prices

========================================================
TRACKED PRODUCTS WITH LATEST PRICES
========================================================

#    Product Name                       Price        Last Updated        
------------------------------------------------------------------------
1    Apple AirPods 4 Wireless...        ₹16900      2026-01-14 16:52:59 
     🔗 https://www.amazon.in/...
...
```

### Example 2: Quick add product
```bash
$ python cli_app.py add

🚀 E-commerce Price Tracker - Quick Add Product
================================================================================
ADD NEW PRODUCT TO TRACK
================================================================================

📝 Enter product details:
Product URL: https://www.amazon.in/product/dp/ABC123
Product Name (optional, press Enter to skip): New Product
Category (default: Electronics): 

CONFIRM PRODUCT DETAILS:
Name: New Product
URL: https://www.amazon.in/product/dp/ABC123
Category: Electronics

Add this product? (y/n): y
✅ Product added successfully to tracking list!
```

## Features

### View Command Features
- **Deduplication**: Shows only the latest price for each unique product
- **Smart Formatting**: Truncates long names/URLs while keeping readability
- **URL Display**: Shows full URLs on separate lines for easy copying
- **Empty Handling**: Displays helpful message when no products are tracked
- **Error Resilient**: Gracefully handles storage errors

### Data Display
- **CSV Source**: Reads from products.csv with all historical data
- **Latest Price**: Automatically selects most recent entry per product
- **Structured Output**: Aligned columns for easy reading
- **Metadata**: Shows last updated timestamp for each product

## File Structure
```
ecom-price-tracker/
├── cli_app.py                    # Main CLI application
├── test_cli_view.py              # Test suite for view command
├── CLI_VIEW_DOCUMENTATION.md     # Detailed documentation
├── products.csv                  # Product data storage
├── products.json                 # Product configuration
├── data_storage.py               # CSV operations
└── product_loader.py             # JSON configuration management
```

## Testing
Run all tests:
```bash
python test_cli_view.py
```

All tests verify:
- ✅ Product retrieval with deduplication
- ✅ Formatting functionality
- ✅ Empty list handling
- ✅ Latest price selection logic
- ✅ Full command execution

## Current Status
- **Tracked Products**: 4 unique products
- **Price History**: 5 total entries
- **Test Results**: All tests passing (5/5)
- **Storage**: CSV-based with automatic deduplication
