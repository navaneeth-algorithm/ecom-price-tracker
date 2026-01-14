"""
Command-Line Interface for E-commerce Price Tracker
Provides interactive commands to manage tracked products
"""

import product_loader
import data_storage
import sys
import argparse
import logging
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from datetime import datetime
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('price_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def display_menu():
    """Display the main menu options"""
    print("\n" + "=" * 80)
    print("E-COMMERCE PRICE TRACKER - CLI")
    print("=" * 80)
    print("\nAvailable Commands:")
    print("  1. Add Product         - Add a new product to track")
    print("  2. List Products       - View all tracked products")
    print("  3. View Price History  - Check price history for a product")
    print("  4. Remove Product      - Remove a product from tracking")
    print("  5. Exit                - Exit the application")
    print("=" * 80)


def add_product_cli():
    """
    Interactive function to add a new product to track.
    Prompts user for product URL, name, and category.
    """
    print("\n" + "=" * 80)
    print("ADD NEW PRODUCT TO TRACK")
    print("=" * 80)
    
    # Prompt for product URL
    print("\n📝 Enter product details:")
    product_url = input("Product URL: ").strip()
    
    if not product_url:
        print("❌ Error: Product URL cannot be empty!")
        return False
    
    # Validate URL format
    if not (product_url.startswith('http://') or product_url.startswith('https://')):
        print("❌ Error: Please enter a valid URL (starting with http:// or https://)")
        return False
    
    # Prompt for product name
    product_name = input("Product Name (optional, press Enter to skip): ").strip()
    if not product_name:
        product_name = f"Product-{product_url.split('/')[-1][:20]}"
    
    # Prompt for category
    product_category = input("Category (default: Electronics): ").strip()
    if not product_category:
        product_category = "Electronics"
    
    # Confirm before adding
    print("\n" + "-" * 80)
    print("CONFIRM PRODUCT DETAILS:")
    print("-" * 80)
    print(f"Name: {product_name}")
    print(f"URL: {product_url}")
    print(f"Category: {product_category}")
    print("-" * 80)
    
    confirm = input("\nAdd this product? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Product not added.")
        return False
    
    # Add product to configuration
    success = product_loader.add_product_to_config(
        name=product_name,
        url=product_url,
        category=product_category,
        active=True
    )
    
    if success:
        print("\n✅ Product added successfully to tracking list!")
        return True
    else:
        print("\n❌ Failed to add product.")
        return False


def list_products_cli():
    """Display all tracked products"""
    print("\n" + "=" * 80)
    print("TRACKED PRODUCTS")
    print("=" * 80)
    
    try:
        product_loader.display_products_config()
    except Exception as e:
        print(f"❌ Error loading products: {e}")


def view_price_history_cli():
    """View price history for a specific product"""
    print("\n" + "=" * 80)
    print("VIEW PRICE HISTORY")
    print("=" * 80)
    
    try:
        # Show available products first
        products = product_loader.load_products()
        
        if not products:
            print("\n⚠️  No products found. Add products first!")
            return
        
        print("\nAvailable Products:")
        for idx, product in enumerate(products, 1):
            print(f"{idx}. {product['name']}")
        
        # Get user selection
        choice = input("\nEnter product number (or 'q' to cancel): ").strip()
        
        if choice.lower() == 'q':
            return
        
        try:
            product_idx = int(choice) - 1
            if 0 <= product_idx < len(products):
                selected_product = products[product_idx]
                data_storage.display_price_history(selected_product['url'])
            else:
                print("❌ Invalid product number!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def remove_product_cli():
    """Remove a product from tracking"""
    print("\n" + "=" * 80)
    print("REMOVE PRODUCT")
    print("=" * 80)
    print("\n⚠️  This feature will be implemented in a future update.")
    print("For now, manually edit products.json to remove products.")


def get_all_products_with_prices():
    """
    Retrieve all tracked products with their latest recorded prices.
    
    Returns:
        list: List of dictionaries containing product name, URL, and latest price.
              Each dictionary has keys: 'name', 'url', 'price', 'currency', 'last_updated'
    """
    products_with_prices = []
    
    try:
        # Get all products from CSV
        all_products = data_storage.get_all_products()
        
        if not all_products:
            return products_with_prices
        
        # Group products by URL to find the latest price for each
        product_dict = {}
        
        for product in all_products:
            url = product['product_url']
            
            # If this URL isn't in our dict yet, or if this entry is newer
            if url not in product_dict:
                product_dict[url] = {
                    'name': product['product_name'],
                    'url': url,
                    'price': product['current_price'],
                    'currency': product.get('currency', '₹'),
                    'last_updated': product['last_updated']
                }
            else:
                # Compare timestamps to keep the most recent entry
                existing_time = product_dict[url]['last_updated']
                current_time = product['last_updated']
                
                if current_time > existing_time:
                    product_dict[url] = {
                        'name': product['product_name'],
                        'url': url,
                        'price': product['current_price'],
                        'currency': product.get('currency', '₹'),
                        'last_updated': current_time
                    }
        
        # Convert dictionary to list
        products_with_prices = list(product_dict.values())
        
        print(f"✓ Retrieved {len(products_with_prices)} unique product(s) with latest prices")
        return products_with_prices
    
    except Exception as e:
        print(f"✗ Error retrieving products with prices: {e}")
        return products_with_prices


def format_products_for_cli(products):
    """
    Format a list of products into a human-readable table for CLI output.
    
    Args:
        products (list): List of product dictionaries with keys: name, url, price, currency
    
    Returns:
        str: Formatted string ready for console output
    """
    if not products:
        return "\n⚠️  No tracked products found. Add some products first!"
    
    # Build the formatted output
    output = []
    output.append("\n" + "=" * 120)
    output.append("TRACKED PRODUCTS WITH LATEST PRICES")
    output.append("=" * 120)
    output.append(f"\nTotal Products: {len(products)}\n")
    
    # Table header
    output.append(f"{'#':<4} {'Product Name':<50} {'Price':<15} {'Last Updated':<20}")
    output.append("-" * 120)
    
    # Table rows
    for idx, product in enumerate(products, 1):
        name = product['name'][:47] + "..." if len(product['name']) > 50 else product['name']
        price = f"{product['currency']}{product['price']}"
        last_updated = product.get('last_updated', 'N/A')
        
        output.append(f"{idx:<4} {name:<50} {price:<15} {last_updated:<20}")
        
        # Add URL on next line (indented)
        url = product['url']
        if len(url) > 110:
            url = url[:107] + "..."
        output.append(f"     🔗 {url}")
        output.append("")  # Empty line between products
    
    output.append("=" * 120)
    
    return "\n".join(output)


def view_products_cli():
    """
    CLI command to view all tracked products with their latest prices.
    Retrieves products and displays them in a formatted table.
    """
    print("\n🔍 Fetching tracked products...")
    
    # Get all products with their latest prices
    products = get_all_products_with_prices()
    
    # Format and display
    formatted_output = format_products_for_cli(products)
    print(formatted_output)


def remove_product_cli():
    """Remove a product from tracking"""
    print("\n" + "=" * 80)
    print("REMOVE PRODUCT")
    print("=" * 80)
    print("\n⚠️  This feature will be implemented in a future update.")
    print("For now, manually edit products.json to remove products.")


def scrape_single_product(page, product):
    """
    Scrape data from a single product page.
    
    Args:
        page: Playwright page object
        product (dict): Product information including name and URL
    
    Returns:
        dict: Scraped product data or None if scraping failed
    """
    product_url = product['url']
    product_name_from_config = product.get('name', 'Unknown Product')
    
    print(f"\n{'='*80}")
    print(f"Scraping: {product_name_from_config}")
    print(f"URL: {product_url}")
    print(f"{'='*80}")
    
    # Navigate to product page
    try:
        logger.info(f"Navigating to URL: {product_url}")
        page.goto(product_url, wait_until='domcontentloaded', timeout=30000)
        logger.info(f"Successfully navigated to {product_url}")
    except PlaywrightTimeoutError:
        error_msg = f"Timeout error: Page failed to load within 30 seconds for URL: {product_url}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    except PlaywrightError as e:
        error_msg = f"Playwright error during navigation to {product_url}: {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    except Exception as e:
        error_msg = f"Unexpected error during navigation to {product_url}: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    
    # Extract product name
    try:
        logger.info(f"Waiting for product title element for {product_url}")
        page.wait_for_selector('#productTitle', timeout=30000)
        product_name_element = page.query_selector('#productTitle')
        
        if not product_name_element:
            raise ValueError("Product title element not found")
        
        product_name = product_name_element.inner_text().strip()
        logger.info(f"Successfully extracted product name: {product_name[:50]}...")
        
    except PlaywrightTimeoutError:
        error_msg = f"Timeout: Product title element '#productTitle' not found within 30 seconds for {product_url}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    except ValueError as e:
        error_msg = f"Element not found: {str(e)} for URL: {product_url}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    except Exception as e:
        error_msg = f"Error extracting product name from {product_url}: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    
    # Extract product price
    try:
        logger.info(f"Waiting for price element for {product_url}")
        page.wait_for_selector('.a-price-whole', timeout=30000)
        product_price_element = page.query_selector('.a-price-whole')
        
        if not product_price_element:
            raise ValueError("Price element not found")
        
        product_price = product_price_element.inner_text().strip()
        
        if not product_price or product_price == "":
            raise ValueError("Price text is empty")
        
        # Clean up price formatting
        product_price = product_price.replace('\n', '').replace('.', '').strip()
        logger.info(f"Successfully extracted price: ₹{product_price}")
        
    except PlaywrightTimeoutError:
        error_msg = f"Timeout: Price element '.a-price-whole' not found within 30 seconds for {product_url}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    except ValueError as e:
        error_msg = f"Price extraction error: {str(e)} for URL: {product_url}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    except Exception as e:
        error_msg = f"Error extracting price from {product_url}: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None
    
    # Generate timestamp and return data
    try:
        scrape_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print extracted data
        print(f"\n📦 Product Name: {product_name}")
        print(f"💰 Product Price: ₹{product_price}")
        print(f"🕒 Scrape Timestamp: {scrape_timestamp}")
        
        logger.info(f"Successfully scraped product: {product_name[:50]}... - ₹{product_price}")
        
        return {
            'name': product_name,
            'url': product_url,
            'price': product_price,
            'timestamp': scrape_timestamp
        }
    except Exception as e:
        error_msg = f"Error formatting scraped data for {product_url}: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return None


def run_check_command():
    """
    CLI command handler for 'check' command.
    Executes the full scraping process for all tracked products,
    saves new prices, and triggers price drop notifications.
    """
    print("\n" + "=" * 80)
    print("🔍 CHECKING PRICES FOR ALL TRACKED PRODUCTS")
    print("=" * 80)
    
    logger.info("Starting price check command")
    
    # Initialize CSV storage
    try:
        data_storage.setup_storage()
        logger.info("CSV storage initialized successfully")
    except Exception as e:
        error_msg = f"Failed to initialize storage: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return
    
    # Load all tracked products
    try:
        products = product_loader.load_products()
        
        if not products:
            logger.warning("No products found in configuration")
            print("\n⚠️  No products found in configuration.")
            print("Add some products first using: python cli_app.py add")
            return
        
        logger.info(f"Found {len(products)} product(s) to track")
        print(f"\n✓ Found {len(products)} product(s) to track")
        
    except FileNotFoundError as e:
        error_msg = f"Configuration file not found: {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return
    except Exception as e:
        error_msg = f"Error loading products: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return
    
    # Launch browser for scraping
    print("\n🚀 Launching browser...")
    logger.info("Launching Playwright browser")
    
    try:
        with sync_playwright() as p:
            # Launch Chromium browser
            try:
                browser = p.chromium.launch(
                    headless=False,
                    args=['--disable-blink-features=AutomationControlled']
                )
                logger.info("Browser launched successfully")
            except PlaywrightError as e:
                error_msg = f"Failed to launch browser: {str(e)}"
                logger.error(error_msg)
                print(f"\n❌ {error_msg}")
                return
            except Exception as e:
                error_msg = f"Unexpected error launching browser: {type(e).__name__} - {str(e)}"
                logger.error(error_msg)
                print(f"\n❌ {error_msg}")
                return
            
            # Create browser context
            try:
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-IN'
                )
                page = context.new_page()
                logger.info("Browser context and page created successfully")
            except Exception as e:
                error_msg = f"Failed to create browser context: {type(e).__name__} - {str(e)}"
                logger.error(error_msg)
                print(f"\n❌ {error_msg}")
                browser.close()
                return
            
            # Track results
            success_count = 0
            failed_count = 0
            price_drops = []
            
            # Iterate through all products
            for idx, product in enumerate(products, 1):
                print(f"\n\n{'#'*80}")
                print(f"Processing Product {idx}/{len(products)}")
                print(f"{'#'*80}")
                
                logger.info(f"Processing product {idx}/{len(products)}: {product.get('name', 'Unknown')}")
                
                # Scrape product data
                scraped_data = scrape_single_product(page, product)
                
                if scraped_data:
                    try:
                        # Extract price value
                        price_value = scraped_data['price'].replace(',', '').strip()
                        
                        # Get historical prices before saving new price
                        print(f"\n📊 Checking price history...")
                        logger.info(f"Retrieving historical prices for {scraped_data['url']}")
                        
                        try:
                            historical_prices = data_storage.get_historical_prices(scraped_data['url'])
                        except Exception as e:
                            error_msg = f"Error retrieving historical prices: {type(e).__name__} - {str(e)}"
                            logger.error(error_msg)
                            print(f"\n⚠️  {error_msg}")
                            historical_prices = []
                        
                        # Check for price drop
                        if historical_prices:
                            print(f"\n🔍 Analyzing price drop...")
                            logger.info(f"Analyzing price drop for {scraped_data['url']}")
                            
                            try:
                                is_price_drop = data_storage.detect_price_drop(
                                    product_id=scraped_data['url'],
                                    current_price=price_value,
                                    historical_prices_list=historical_prices,
                                    price_drop_threshold=0
                                )
                                
                                if is_price_drop:
                                    # Calculate savings
                                    lowest_historical_price = min(float(p['price']) for p in historical_prices)
                                    current_price_float = float(price_value)
                                    savings = lowest_historical_price - current_price_float
                                    savings_percent = (savings / lowest_historical_price) * 100
                                    
                                    # Store price drop info
                                    price_drops.append({
                                        'name': scraped_data['name'],
                                        'current_price': current_price_float,
                                        'previous_price': lowest_historical_price,
                                        'savings': savings,
                                        'savings_percent': savings_percent,
                                        'url': scraped_data['url']
                                    })
                                    
                                    logger.info(f"Price drop detected: {scraped_data['name'][:50]}... - Save ₹{savings:.2f}")
                                    
                                    # Print price drop notification
                                    print("\n" + "🎉" * 40)
                                    print("🚨 PRICE DROP ALERT! 🚨")
                                    print("🎉" * 40)
                                    print(f"\n📦 Product: {scraped_data['name'][:80]}...")
                                    print(f"💰 New Price: ₹{current_price_float:,.2f}")
                                    print(f"📉 Previous Lowest: ₹{lowest_historical_price:,.2f}")
                                    print(f"💵 You Save: ₹{savings:,.2f} ({savings_percent:.2f}% OFF)")
                                    print(f"🔗 URL: {scraped_data['url'][:60]}...")
                                    print("\n" + "🎉" * 40)
                                    
                            except ValueError as e:
                                error_msg = f"Error analyzing price drop (invalid price value): {str(e)}"
                                logger.error(error_msg)
                                print(f"\n⚠️  {error_msg}")
                            except Exception as e:
                                error_msg = f"Error detecting price drop: {type(e).__name__} - {str(e)}"
                                logger.error(error_msg)
                                print(f"\n⚠️  {error_msg}")
                        
                        # Save to storage
                        print(f"\n📝 Saving to storage...")
                        logger.info(f"Saving product to storage: {scraped_data['name'][:50]}...")
                        
                        try:
                            success = data_storage.add_product(
                                product_name=scraped_data['name'],
                                product_url=scraped_data['url'],
                                current_price=price_value,
                                currency="₹",
                                image_url=""
                            )
                            
                            if success:
                                print(f"✅ Product {idx} saved successfully!")
                                logger.info(f"Product {idx} saved successfully")
                                success_count += 1
                            else:
                                print(f"❌ Failed to save product {idx}")
                                logger.warning(f"Failed to save product {idx}")
                                failed_count += 1
                                
                        except Exception as e:
                            error_msg = f"Error saving product to storage: {type(e).__name__} - {str(e)}"
                            logger.error(error_msg)
                            print(f"\n❌ {error_msg}")
                            failed_count += 1
                            
                    except Exception as e:
                        error_msg = f"Error processing scraped data: {type(e).__name__} - {str(e)}"
                        logger.error(error_msg)
                        print(f"\n❌ {error_msg}")
                        failed_count += 1
                else:
                    logger.warning(f"Failed to scrape product {idx}")
                    print(f"❌ Failed to scrape product {idx}")
                    failed_count += 1
                
                # Delay between requests
                if idx < len(products):
                    print(f"\n⏳ Waiting 3 seconds before next product...")
                    time.sleep(3)
            
            # Close browser
            try:
                browser.close()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.warning(f"Error closing browser: {type(e).__name__} - {str(e)}")
            
    except Exception as e:
        error_msg = f"Unexpected error during scraping process: {type(e).__name__} - {str(e)}"
        logger.error(error_msg)
        print(f"\n❌ {error_msg}")
        return
    
    # Print summary
    print("\n" + "=" * 80)
    print("SCRAPING SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully scraped and saved: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total products: {len(products)}")
    print("=" * 80)
    
    # Print price drop summary
    if price_drops:
        print("\n" + "🎉" * 40)
        print(f"🚨 FOUND {len(price_drops)} PRICE DROP(S)!")
        print("🎉" * 40)
        
        for drop in price_drops:
            print(f"\n📦 {drop['name'][:60]}...")
            print(f"   💰 New: ₹{drop['current_price']:,.2f} | Previous: ₹{drop['previous_price']:,.2f}")
            print(f"   💵 Save: ₹{drop['savings']:,.2f} ({drop['savings_percent']:.2f}% OFF)")
        
        print("\n" + "🎉" * 40)
    else:
        print("\n📊 No price drops detected in this check.")
    
    logger.info("Price check completed")
    print("\n✅ Price check completed!")


def main():
    """Main CLI application loop"""
    print("\n🚀 Welcome to E-commerce Price Tracker CLI!")
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            add_product_cli()
        elif choice == '2':
            list_products_cli()
        elif choice == '3':
            view_price_history_cli()
        elif choice == '4':
            remove_product_cli()
        elif choice == '5':
            print("\n👋 Thank you for using Price Tracker CLI. Goodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 5.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


# Simple add product mode (for quick access)
def quick_add_product():
    """Quick mode to just add a product without full menu"""
    print("\n🚀 E-commerce Price Tracker - Quick Add Product")
    add_product_cli()


def setup_argparse():
    """
    Setup argparse for command-line argument parsing.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="E-commerce Price Tracker CLI - Manage and view tracked products",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_app.py view          - View all tracked products with latest prices
  python cli_app.py add           - Quick add a new product
  python cli_app.py check         - Scrape all products, save prices, and check for drops
  python cli_app.py interactive   - Launch interactive menu (default)
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['view', 'add', 'check', 'interactive'],
        default='interactive',
        help='Command to execute: view (display products), add (quick add), check (scrape & alert), interactive (full menu)'
    )
    
    return parser


if __name__ == "__main__":
    # Parse command-line arguments
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Execute based on command
    if args.command == 'view':
        # View command: Display all tracked products
        view_products_cli()
    elif args.command == 'add':
        # Quick add mode: python cli_app.py add
        quick_add_product()
    elif args.command == 'check':
        # Check command: Scrape all products and check for price drops
        run_check_command()
    else:
        # Full interactive CLI mode (default)
        main()
