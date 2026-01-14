# CLI Check Command - Integration Documentation

## Overview
The `check` command integrates scraping, price storage, and price drop alerting into a single CLI command. Running `python tracker.py check` executes the full price tracking workflow for all configured products.

## Command Usage

### Basic Usage
```bash
python tracker.py check
```

### Alternative Usage
```bash
python cli_app.py check
```

## What the Check Command Does

### 1. Initialization
- Loads all tracked products from `products.json`
- Initializes CSV storage (`products.csv`)
- Displays count of products to track

### 2. Browser Launch
- Launches Chromium browser (non-headless mode)
- Sets user agent to avoid bot detection
- Configures viewport and locale

### 3. Product Scraping (For Each Product)
- Navigates to product URL
- Extracts product name from `#productTitle` selector
- Extracts price from `.a-price-whole` selector
- Cleans and formats price data
- Generates timestamp for the scrape

### 4. Price History Analysis
- Retrieves historical prices for the product
- Compares current price with previous prices
- Detects price drops (any decrease from lowest historical price)

### 5. Price Drop Notifications
If a price drop is detected:
```
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
🚨 PRICE DROP ALERT! 🚨
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

📦 Product: Apple AirPods 4 Wireless Earbuds...
💰 New Price: ₹15,900.00
📉 Previous Lowest: ₹16,900.00
💵 You Save: ₹1,000.00 (5.92% OFF)
🔗 URL: https://www.amazon.in/...

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
```

### 6. Data Storage
- Saves new price entry to CSV storage
- Maintains historical price data
- Updates last_updated timestamp

### 7. Summary Report
After all products are processed:
- Success count
- Failed count
- Total products
- List of all price drops detected (if any)

## Implementation Details

### File Structure
```
tracker.py              # Main CLI entry point
cli_app.py             # Core CLI implementation
├── run_check_command()        # Main check handler
├── scrape_single_product()    # Product scraping logic
└── setup_argparse()           # CLI argument parsing
```

### Key Functions

#### `run_check_command()`
Main handler for the check command that:
1. Initializes storage
2. Loads products
3. Launches browser
4. Iterates through products
5. Calls scraping and analysis functions
6. Displays summary

#### `scrape_single_product(page, product)`
Handles individual product scraping:
- **Input**: Playwright page object, product dict
- **Output**: Dict with name, url, price, timestamp
- **Error Handling**: Returns None on failure

**Returns:**
```python
{
    'name': 'Product Name',
    'url': 'https://...',
    'price': '16900',
    'timestamp': '2026-01-14 17:16:00'
}
```

### Integration Points

#### With Data Storage Module
```python
# Get historical prices
historical_prices = data_storage.get_historical_prices(url)

# Detect price drops
is_drop = data_storage.detect_price_drop(
    product_id=url,
    current_price=price,
    historical_prices_list=historical_prices,
    price_drop_threshold=0
)

# Save new price
data_storage.add_product(
    product_name=name,
    product_url=url,
    current_price=price,
    currency="₹"
)
```

#### With Product Loader Module
```python
# Load all tracked products
products = product_loader.load_products()
```

### Timing and Delays
- **Page Load Timeout**: 30 seconds
- **Between Products**: 3 seconds delay
- **Total Time**: ~15-20 seconds for 4 products

## Example Output

### Successful Run (No Price Drops)
```bash
$ python tracker.py check

================================================================================
🔍 CHECKING PRICES FOR ALL TRACKED PRODUCTS
================================================================================
✓ Storage already exists: products.csv
✓ Loaded 4 active product(s) from products.json

✓ Found 4 product(s) to track

🚀 Launching browser...

################################################################################
Processing Product 1/4
################################################################################

================================================================================
Scraping: Apple AirPods 4
URL: https://www.amazon.in/...
================================================================================

📦 Product Name: Apple AirPods 4 Wireless Earbuds...
💰 Product Price: ₹16,900
🕒 Scrape Timestamp: 2026-01-14 17:16:00

📊 Checking price history...
✓ Found 2 historical price(s) for product

🔍 Analyzing price drop...
✓ No significant price drop

📝 Saving to storage...
✓ Product added
✅ Product 1 saved successfully!

⏳ Waiting 3 seconds before next product...

[... continues for all products ...]

================================================================================
SCRAPING SUMMARY
================================================================================
✅ Successfully scraped and saved: 4
❌ Failed: 0
📊 Total products: 4
================================================================================

📊 No price drops detected in this check.

✅ Price check completed!
```

### Run with Price Drops
```bash
[... scraping output ...]

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
🚨 FOUND 2 PRICE DROP(S)!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

📦 Apple AirPods 4 Wireless Earbuds...
   💰 New: ₹15,900.00 | Previous: ₹16,900.00
   💵 Save: ₹1,000.00 (5.92% OFF)

📦 EarFun Air Pro 4...
   💰 New: ₹6,997.00 | Previous: ₹7,297.00
   💵 Save: ₹300.00 (4.11% OFF)

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
```

## Testing

### Run Automated Tests
```bash
python test_cli_check.py
```

### Test Coverage
All 6 tests pass:
- ✅ tracker.py file exists
- ✅ 'check' command in help
- ✅ All CLI commands present
- ✅ Products configuration loaded
- ✅ CSV storage verified
- ✅ Required dependencies available

## Error Handling

### Product Scraping Failures
- Logs error message
- Continues to next product
- Included in failed count

### Browser Issues
- Timeout after 30 seconds
- Descriptive error messages
- Non-headless mode for better success rate

### Storage Errors
- Initializes storage if missing
- Validates data before saving
- Reports success/failure per product

## Performance Considerations

### Browser Mode
- **Non-headless**: Better success rate with Amazon
- **User Agent Spoofing**: Avoids bot detection
- **Viewport**: Standard desktop resolution (1920x1080)

### Rate Limiting
- 3-second delay between products
- Respects server load
- Prevents IP blocking

### Memory Management
- Single browser instance
- Reuses page object
- Closes browser after completion

## Automation Potential

### Cron Job (Linux/Mac)
```bash
# Run check every 6 hours
0 */6 * * * cd /path/to/ecom-price-tracker && /path/to/.venv/bin/python tracker.py check >> logs/check.log 2>&1
```

### Task Scheduler (Windows)
- Action: `python tracker.py check`
- Trigger: Daily at specific time
- Start in: Project directory

## Dependencies

### Python Packages
- `playwright` - Browser automation
- `data_storage` - CSV operations
- `product_loader` - JSON configuration
- `datetime` - Timestamps
- `time` - Delays
- `argparse` - CLI parsing

### External
- Chromium browser (installed via playwright)
- Internet connection
- Amazon India access

## Definition of Done ✅

All requirements met:
- ✅ `python tracker.py check` command works
- ✅ Scrapes all configured products
- ✅ Updates prices in CSV storage
- ✅ Displays clear price drop notifications
- ✅ Integrated with argparse
- ✅ Dedicated `run_check_command()` function
- ✅ Loads products from configuration
- ✅ Iterates through all products
- ✅ Compares with previous prices
- ✅ Tested and verified working

## Future Enhancements

Potential improvements:
- Headless mode option via CLI flag
- Email notifications for price drops
- Configurable delay between products
- Parallel scraping support
- Price drop threshold configuration
- Silent mode (no console output)
- JSON output format option
