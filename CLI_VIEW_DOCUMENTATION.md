# CLI View Command Documentation

## Overview
The CLI now supports a `view` command to display all tracked products with their latest recorded prices in a formatted table.

## Implementation

### 1. `get_all_products_with_prices()`
**Purpose:** Retrieves all tracked products with their latest recorded prices.

**Functionality:**
- Reads all products from the CSV storage
- Groups products by URL to handle multiple price entries
- Keeps only the most recent price entry for each unique product
- Returns a list of dictionaries with product details

**Returns:**
```python
[
    {
        'name': 'Product Name',
        'url': 'https://...',
        'price': '16900',
        'currency': '₹',
        'last_updated': '2026-01-14 16:52:59'
    },
    ...
]
```

### 2. `format_products_for_cli(products)`
**Purpose:** Formats product data into a human-readable table for console output.

**Features:**
- Creates a formatted table with headers
- Truncates long product names and URLs for readability
- Shows product number, name, price, and last updated timestamp
- Displays full URL on a separate line under each product
- Handles empty product lists gracefully

**Example Output:**
```
========================================================
TRACKED PRODUCTS WITH LATEST PRICES
========================================================

Total Products: 4

#    Product Name                       Price        Last Updated        
------------------------------------------------------------------------
1    Apple AirPods 4 Wireless...        ₹16900      2026-01-14 16:52:59 
     🔗 https://www.amazon.in/...

2    Original Wired for iPhone...       ₹1499       2026-01-14 16:53:04 
     🔗 https://www.amazon.in/...
```

### 3. `view_products_cli()`
**Purpose:** Main CLI command function that orchestrates the view functionality.

**Workflow:**
1. Displays loading message
2. Calls `get_all_products_with_prices()`
3. Calls `format_products_for_cli()` with the results
4. Prints the formatted output

### 4. Argparse Integration
**Purpose:** Command-line argument parsing for multiple CLI modes.

**Available Commands:**
- `view` - Display all tracked products with latest prices
- `add` - Quick add a new product
- `interactive` - Launch full interactive menu (default)

**Usage Examples:**
```bash
# View all products
python cli_app.py view

# Add a new product (quick mode)
python cli_app.py add

# Interactive menu (default)
python cli_app.py
python cli_app.py interactive

# Show help
python cli_app.py --help
```

## Testing

### Test Coverage
All tests in `test_cli_view.py` pass:
- ✅ Test 1: Get all products with latest prices
- ✅ Test 2: Format products for CLI display
- ✅ Test 3: Handle empty product list
- ✅ Test 4: Verify latest price selection (deduplication)
- ✅ Test 5: Execute full view_products_cli function

### Sample Data
The system currently tracks 4 products with 5 total price entries:
1. Apple AirPods 4 - ₹16,900
2. Original Wired for iPhone 15/16/17 - ₹1,499
3. Ambrane 20-in-1 Cleaning Kit - ₹599
4. EarFun Air Pro 4 - ₹7,297

## Definition of Done ✅

All requirements met:
- ✅ Created `get_all_products_with_prices()` function that queries CSV storage
- ✅ Implemented `format_products_for_cli()` for human-readable table output
- ✅ Integrated `view` sub-command using argparse
- ✅ View command displays product name, URL, and latest price
- ✅ Tested with sample data (4 products with price history)
- ✅ Command `python cli_app.py view` successfully displays all products

## Key Features
- **Deduplication**: Automatically shows only the latest price for each product
- **Formatted Display**: Clean table layout with aligned columns
- **URL Handling**: Truncates long URLs but shows them on separate lines
- **Error Handling**: Gracefully handles empty lists and errors
- **Flexible Usage**: Works as standalone command or within interactive menu
