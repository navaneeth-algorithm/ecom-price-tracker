# 🛒 E-Commerce Price Tracker

A powerful, automated price monitoring system for tracking product prices across e-commerce platforms. Get instant alerts when prices drop and make smart purchasing decisions.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Adding Products](#adding-products)
- [Scheduling Automated Runs](#scheduling-automated-runs)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)
- [Resources](#resources)

---

## ✨ Features

- **🕷️ Web Scraping**: Uses Playwright for reliable product data extraction
- **📊 Price Tracking**: Maintains historical price records for trend analysis
- **🔔 Price Drop Alerts**: Instant notifications when prices decrease
- **⏰ Automated Scheduling**: Runs checks automatically at configurable intervals
- **📝 Comprehensive Logging**: Detailed logs for debugging and monitoring
- **🎯 CLI Interface**: Easy-to-use command-line tools for all operations
- **📦 Modular Architecture**: Clean separation of concerns with dedicated modules
- **🛡️ Error Handling**: Robust error handling with graceful failure recovery
- **💾 Multiple Storage Options**: CSV for historical data, JSON for configuration
- **🔍 Price Analysis**: Detect trends and calculate savings automatically

---

## 🗂️ Project Structure

```
ecom-price-tracker/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── tracker.py                         # Main entry point
├── cli_app.py                         # CLI interface implementation
├── scheduler.py                       # Automated scheduling system
├── setup_cron.py                      # Cron configuration helper
│
├── Core Modules:
├── scraper.py                         # Web scraping logic
├── storage_manager.py                 # Data storage and retrieval
├── notifier.py                        # Price drop alerts
├── product_loader.py                  # Product configuration
├── data_storage.py                    # Legacy storage utilities
│
├── Configuration Files:
├── products.json                      # Product configuration
├── products.csv                       # Historical price data
├── SELECTORS.md                       # CSS selector documentation
│
├── Tests:
├── test_scheduler.py                  # Scheduler tests
├── test_refactored_modules.py         # Module integration tests
├── test_logging.py                    # Logging verification
├── test_error_handling.py             # Error handling tests
├── test_cli_*.py                      # CLI command tests
│
├── Documentation:
├── SCHEDULING_GUIDE.md                # Complete scheduling documentation
├── SCHEDULING_SUMMARY.md              # Scheduling quick reference
├── REFACTORING_DOCUMENTATION.md       # Architecture documentation
├── ERROR_HANDLING_DOCUMENTATION.md    # Error handling guide
├── CLI_QUICK_REFERENCE.md             # CLI command reference
│
└── logs/
    ├── app.log                        # Application activity log
    └── scheduler.log                  # Scheduler execution log
```

---

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher (tested on 3.13)
- **OS**: macOS, Linux, or Windows
- **RAM**: Minimum 512MB (1GB recommended)
- **Disk Space**: 100MB for dependencies and data

### Required Tools
- Git (for cloning and version control)
- Pip (Python package manager)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/navaneeth-algorithm/ecom-price-tracker.git
cd ecom-price-tracker
```

### Step 2: Create a Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt):**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3: Upgrade Pip

```bash
pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **Playwright** (1.57.0+): Browser automation for web scraping
- **Requests**: HTTP library for additional web operations
- **Schedule**: Job scheduling library for automated runs

### Step 5: Install Browser Drivers

Playwright requires browser drivers. Install them with:

```bash
playwright install
```

This installs:
- Chromium browser
- Firefox browser
- WebKit browser

**Note:** First installation may take 5-10 minutes.

### Step 6: Verify Installation

```bash
python tracker.py --help
```

You should see the CLI help menu. If successful, installation is complete!

---

## ⚙️ Configuration

### Products Configuration File

The `products.json` file contains the list of products to track:

```json
[
  {
    "product_id": "product_1",
    "product_name": "Product Name",
    "product_url": "https://example.com/product-page",
    "currency": "USD",
    "price_drop_threshold": 10
  }
]
```

**Fields:**
- `product_id`: Unique identifier for the product
- `product_name`: Human-readable product name
- `product_url`: Full URL to the product page
- `currency`: Currency code (USD, EUR, INR, etc.)
- `price_drop_threshold`: Minimum price drop amount to trigger alert

### CSS Selectors

For new e-commerce sites, you may need to update CSS selectors in [SELECTORS.md](SELECTORS.md):

```python
SELECTORS = {
    'product_title': '#productTitle',      # Product name selector
    'product_price': '.a-price-whole',     # Price selector
    'product_image': '#landingImage'       # Product image selector
}
```

Use browser Developer Tools (F12) to find correct selectors for your target sites.

---

## 📖 Usage

### CLI Commands

#### 1. View All Tracked Products

Display all products currently being tracked with their latest prices:

```bash
python tracker.py view
```

**Output Example:**
```
ID    | Product Name          | Price    | Last Updated
------|----------------------|----------|------------------
prod1 | Wireless Headphones   | $49.99   | 2026-01-14 10:30
prod2 | USB-C Cable           | $12.99   | 2026-01-14 10:25
```

#### 2. Add a New Product

Interactively add a product to track:

```bash
python tracker.py add
```

**Prompts:**
- Product ID: `my_product_1`
- Product Name: `Product Name`
- Product URL: `https://example.com/product`
- Currency: `USD`
- Price Drop Threshold: `10`

#### 3. Check Prices Now

Manually trigger price checks for all products:

```bash
python tracker.py check
```

**What it does:**
1. Fetches the latest price for each product
2. Stores new prices in `products.csv`
3. Detects price drops based on thresholds
4. Displays alerts for products with significant price drops
5. Logs all activity to `app.log`

#### 4. Get Help

Display all available commands:

```bash
python tracker.py --help
```

---

## ➕ Adding Products

### Method 1: Interactive CLI (Recommended)

```bash
python tracker.py add
```

Follow the prompts to enter:
1. **Product ID**: Unique identifier (e.g., `amazon_headphones_001`)
2. **Product Name**: Descriptive name (e.g., `Sony WH-1000XM4 Headphones`)
3. **Product URL**: Full product page URL (e.g., `https://amazon.com/s?k=...`)
4. **Currency**: Product currency (e.g., `USD`)
5. **Price Drop Threshold**: Alert threshold in currency units (e.g., `50`)

### Method 2: Manual JSON Editing

Edit `products.json` directly:

```json
[
  {
    "product_id": "sony_xm4",
    "product_name": "Sony WH-1000XM4 Wireless Headphones",
    "product_url": "https://www.amazon.com/Sony-WH-1000XM4/dp/B07D7MHZQD",
    "currency": "USD",
    "price_drop_threshold": 50
  }
]
```

### Finding the Correct Product URL

1. Navigate to the product page in your browser
2. Copy the full URL from the address bar
3. Ensure the URL shows the product details page (not search results)
4. Test by running `python tracker.py check`

### Supported E-commerce Platforms

Currently tested on:
- **Amazon** (amazon.com, amazon.co.uk, amazon.in, etc.)
- **Other platforms**: May work with selector adjustments (see [SELECTORS.md](SELECTORS.md))

---

## ⏰ Scheduling Automated Runs

### Quick Start: Python Scheduler

**Easiest method** - runs in the foreground:

```bash
python scheduler.py
```

Runs price checks every 6 hours with real-time logging.

### Custom Intervals

```bash
# Every 3 hours
python scheduler.py --interval 3

# Every 12 hours
python scheduler.py --interval 12
```

### Background Execution

Keep the scheduler running in the background:

**Using nohup (macOS/Linux):**
```bash
nohup python scheduler.py > scheduler_output.log 2>&1 &
```

**Using screen (macOS/Linux):**
```bash
screen -dmS price-tracker python scheduler.py
```

**Using Task Scheduler (Windows):**
See [SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md) for detailed instructions.

### System-Level Scheduling (Advanced)

For persistent, system-integrated scheduling:

**macOS/Linux (Cron):**
```bash
python setup_cron.py
```

Interactive helper to set up cron jobs.

**Windows (Task Scheduler):**
See [SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md) - Comprehensive setup guide.

---

## 🔍 Troubleshooting

### Installation Issues

#### 1. "Module 'playwright' not found"

**Problem**: Playwright not installed properly.

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Reinstall Playwright
pip install --force-reinstall playwright==1.57.0

# Install browser drivers
playwright install
```

#### 2. "Chromium browser not found"

**Problem**: Browser drivers were not installed.

**Solution:**
```bash
playwright install chromium
```

#### 3. "Permission denied" on macOS/Linux

**Problem**: Script files lack execute permission.

**Solution:**
```bash
chmod +x tracker.py
chmod +x scheduler.py
chmod +x setup_cron.py
```

---

### Runtime Issues

#### 1. "No products configured"

**Problem**: `products.json` is empty or missing.

**Solution:**
```bash
# Check if file exists
ls -la products.json

# Add a product
python tracker.py add

# Or manually create with sample content
echo '[{"product_id": "test", "product_name": "Test Product", "product_url": "https://...", "currency": "USD", "price_drop_threshold": 10}]' > products.json
```

#### 2. "Product page title not found"

**Problem**: CSS selectors don't match the target website.

**Solution:**
1. Open the product page in a browser
2. Right-click → Inspect Element
3. Find the correct CSS selector
4. Update [SELECTORS.md](SELECTORS.md)
5. Test with `python tracker.py check`

Example for Amazon product titles:
```python
SELECTORS = {
    'product_title': '#productTitle',  # Standard Amazon selector
    # or try these alternatives if needed:
    # 'product_title': 'h1.product-title'
    # 'product_title': 'span.title'
}
```

#### 3. "Network timeout" or "Connection refused"

**Problem**: Website blocking or network issues.

**Causes:**
- Website is blocking automated requests
- Slow internet connection
- Website server is down

**Solutions:**
```bash
# Test connection
curl -I https://example.com

# Check if website is accessible
python -c "import urllib.request; urllib.request.urlopen('https://example.com')"

# Increase timeout in scraper.py
# Change: ELEMENT_WAIT_TIMEOUT = 30000  # 30 seconds
# To:     ELEMENT_WAIT_TIMEOUT = 60000  # 60 seconds
```

#### 4. "Playwright hangs and doesn't complete"

**Problem**: Browser process not terminating properly.

**Solution:**
```bash
# Kill any hanging Playwright processes
pkill -f "chromium"  # macOS/Linux
taskkill /F /IM chrome.exe  # Windows

# Reduce browser timeout
# Edit scraper.py and decrease timeouts

# Or restart terminal and virtual environment
source .venv/bin/activate
python tracker.py check
```

---

### Data Issues

#### 1. "CSV file is corrupted"

**Problem**: `products.csv` has formatting issues.

**Solution:**
```bash
# Backup corrupted file
cp products.csv products.csv.backup

# Create fresh CSV with headers
python -c "
import csv
with open('products.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['product_id', 'product_name', 'product_url', 'current_price', 'currency', 'last_updated', 'image_url'])
"
```

#### 2. "Missing or invalid price data"

**Problem**: Prices are not being captured correctly.

**Solution:**
1. Verify product URL is correct
2. Check website structure hasn't changed
3. Update CSS selectors in [SELECTORS.md](SELECTORS.md)
4. Test selector manually:
   ```bash
   python -c "
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
       browser = p.chromium.launch()
       page = browser.new_page()
       page.goto('https://example.com/product')
       price = page.query_selector('.a-price-whole').inner_text()
       print(f'Price: {price}')
       browser.close()
   "
   ```

---

### Logging Issues

#### 1. "No log entries created"

**Problem**: `app.log` or `scheduler.log` is empty.

**Solution:**
```bash
# Check file permissions
ls -la app.log scheduler.log

# Make files writable
chmod 644 app.log scheduler.log

# Clear and retry
> app.log
python tracker.py check
tail app.log
```

#### 2. "Log files growing too large"

**Problem**: Log files consuming significant disk space.

**Solution:**
```bash
# Archive old logs
mv app.log app.log.$(date +%Y%m%d)

# Create fresh log
touch app.log

# Or use logrotate (Linux)
# Set up automatic rotation in cron job
```

---

### Scheduling Issues

#### 1. "Scheduler not starting"

**Problem**: `scheduler.py` fails to run.

**Solution:**
```bash
# Verify schedule library installed
pip list | grep schedule

# Check Python path
which python

# Run with explicit Python path
/usr/local/bin/python3 scheduler.py

# Check for syntax errors
python -m py_compile scheduler.py
```

#### 2. "Cron job not executing"

**Problem**: Cron job doesn't run on schedule.

**Solution:**
```bash
# Verify cron service running (Linux)
systemctl status cron

# Check crontab is configured
crontab -l

# View cron logs
grep CRON /var/log/syslog  # Linux
log show --predicate 'process == "cron"' --last 1d  # macOS

# Test command manually
cd /path/to/project && python tracker.py check
```

#### 3. "Task Scheduler task not running (Windows)"

**Problem**: Scheduled task doesn't execute.

**Solution:**
1. Open Task Scheduler
2. Right-click task → Run
3. Check History tab for errors
4. Verify Python path is correct
5. Ensure task has proper permissions

---

### Performance Issues

#### 1. "Script is very slow"

**Problem**: Scraping or processing takes too long.

**Possible causes:**
- Website is slow
- Network latency
- Too many products to check
- Playwright initialization overhead

**Solutions:**
```bash
# Check website response time
curl -w "%{time_total}s\n" -o /dev/null -s https://example.com

# Optimize by reducing products
# Edit products.json to include only essential products

# Increase timeout if needed
# In scraper.py: ELEMENT_WAIT_TIMEOUT = 60000
```

#### 2. "High memory usage"

**Problem**: Script consumes excessive RAM.

**Solutions:**
```bash
# Run with memory limit
# Python doesn't have built-in limit, but use system tools:
ulimit -v 1048576  # Limit to 1GB (macOS/Linux)

# Close other applications to free memory
# Check memory usage
top -l 1 | grep tracker  # macOS
top -bn1 | grep tracker  # Linux
```

---

### Getting Help

#### Check Logs

```bash
# View application logs
tail -f app.log

# View scheduler logs
tail -f scheduler.log

# Search for errors
grep ERROR app.log
grep ERROR scheduler.log
```

#### Run Tests

```bash
# Test scheduler functionality
python test_scheduler.py

# Test modules
python test_refactored_modules.py

# Test error handling
python test_error_handling.py

# Test logging
python test_logging.py
```

#### Get CLI Help

```bash
# Main help
python tracker.py --help

# Scheduler help
python scheduler.py --help

# Cron setup helper
python setup_cron.py
```

---

## 📚 Documentation

Comprehensive documentation for advanced usage:

### Getting Started
- **[SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md)** - Complete scheduling setup guide for all platforms
- **[SCHEDULING_SUMMARY.md](SCHEDULING_SUMMARY.md)** - Quick reference for scheduling

### Architecture & Design
- **[REFACTORING_DOCUMENTATION.md](REFACTORING_DOCUMENTATION.md)** - Modular architecture overview
- **[ERROR_HANDLING_DOCUMENTATION.md](ERROR_HANDLING_DOCUMENTATION.md)** - Error handling strategies

### Command Reference
- **[CLI_QUICK_REFERENCE.md](CLI_QUICK_REFERENCE.md)** - All CLI commands and options
- **[SELECTORS.md](SELECTORS.md)** - CSS selector documentation for web scraping

---

## 🔧 Development

### Project Structure

The codebase is organized into logical modules:

- **scraper.py**: `ProductScraper` class for web scraping logic
- **storage_manager.py**: `StorageManager` class for data persistence
- **notifier.py**: `PriceDropNotifier` class for alerts
- **cli_app.py**: CLI interface implementation
- **scheduler.py**: Automated scheduling system
- **tracker.py**: Main entry point combining all modules

### Running Tests

```bash
# Run all tests
python test_*.py

# Run specific test
python test_scheduler.py
python test_refactored_modules.py
python test_logging.py
```

### Contributing

For contributions:
1. Create a feature branch
2. Make your changes
3. Run tests to ensure nothing breaks
4. Commit with clear messages
5. Push to your fork
6. Create a pull request

---

## 📝 License

This project is provided as-is for educational and personal use.

---

## 🤝 Support

For issues, questions, or suggestions:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review existing documentation files
3. Check log files for detailed error messages
4. Run the test suite to identify specific issues

---

## 🎉 Quick Reference

### Most Common Commands

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Add a product
python tracker.py add

# Check prices now
python tracker.py check

# View all products
python tracker.py view

# Run scheduler (6 hours)
python scheduler.py

# Get help
python tracker.py --help
python scheduler.py --help
```

### Important Files

- **products.json**: Configure products to track
- **products.csv**: Historical price data (auto-generated)
- **app.log**: Application activity log
- **scheduler.log**: Scheduler execution log

### Key Documentation

- **Setup**: See [Installation](#installation) section
- **Scheduling**: See [SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md)
- **Troubleshooting**: See [Troubleshooting](#troubleshooting) section
- **All Commands**: See [CLI_QUICK_REFERENCE.md](CLI_QUICK_REFERENCE.md)

---

## 📹 Resources

- **Video Demo**: [Watch on YouTube](https://youtu.be/gTPwOjdsiAI)

---

**Last Updated**: January 14, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
