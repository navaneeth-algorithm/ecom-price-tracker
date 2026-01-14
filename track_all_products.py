"""
Multi-Product Price Tracker
Scrapes multiple products from a list and saves data to CSV storage
"""

from playwright.sync_api import sync_playwright
from datetime import datetime
import data_storage
import product_loader
import time


def scrape_product(page, product):
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
    
    try:
        # Navigate to the product URL
        page.goto(product_url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait for the product title to be visible
        page.wait_for_selector('#productTitle', timeout=30000)
        
        # Extract product name using the identified CSS selector
        product_name = page.query_selector('#productTitle').inner_text().strip()
        
        # Extract product price using the identified CSS selector
        page.wait_for_selector('.a-price-whole', timeout=30000)
        product_price_element = page.query_selector('.a-price-whole')
        product_price = product_price_element.inner_text().strip() if product_price_element else "N/A"
        
        # Clean up price formatting (remove trailing periods and newlines)
        product_price = product_price.replace('\n', '').replace('.', '').strip()
        
        # Format the price (add currency symbol if not present)
        if product_price != "N/A" and not product_price.startswith('₹'):
            product_price = f"₹{product_price}"
        
        # Generate timestamp for the scrape
        scrape_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print the extracted data
        print(f"\n📦 Product Name: {product_name}")
        print(f"💰 Product Price: {product_price}")
        print(f"🕒 Scrape Timestamp: {scrape_timestamp}")
        
        # Return scraped data
        return {
            'name': product_name,
            'url': product_url,
            'price': product_price,
            'timestamp': scrape_timestamp
        }
    
    except Exception as e:
        print(f"\n❌ Error scraping product: {e}")
        return None


def scrape_all_products():
    """
    Scrape all products from the products.json configuration file
    and save them to CSV storage.
    """
    print("=" * 80)
    print("MULTI-PRODUCT PRICE TRACKER")
    print("=" * 80)
    
    # Initialize CSV storage
    data_storage.setup_storage()
    
    # Load products from configuration
    try:
        products = product_loader.load_products()
        
        if not products:
            print("\n⚠️ No products found in configuration.")
            return
        
        print(f"\n✓ Found {len(products)} product(s) to track")
        
    except Exception as e:
        print(f"\n❌ Error loading products: {e}")
        return
    
    # Launch browser
    with sync_playwright() as p:
        # Launch Chromium browser in non-headless mode for better success rate
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # Create a new browser context with additional settings
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-IN'
        )
        
        # Create a new page
        page = context.new_page()
        
        # Track scraping results
        success_count = 0
        failed_count = 0
        
        # Iterate through all products
        for idx, product in enumerate(products, 1):
            print(f"\n\n{'#'*80}")
            print(f"Processing Product {idx}/{len(products)}")
            print(f"{'#'*80}")
            
            # Scrape product data
            scraped_data = scrape_product(page, product)
            
            if scraped_data:
                # Extract just the price value without currency symbol for storage
                price_value = scraped_data['price'].replace('₹', '').replace(',', '').strip()
                
                # Get historical prices for this product before saving new price
                print(f"\n📊 Checking price history...")
                historical_prices = data_storage.get_historical_prices(scraped_data['url'])
                
                # Check for price drop
                if historical_prices:
                    print(f"\n🔍 Analyzing price drop...")
                    is_price_drop = data_storage.detect_price_drop(
                        product_id=scraped_data['url'],
                        current_price=price_value,
                        historical_prices_list=historical_prices,
                        price_drop_threshold=0  # Set to 0 to detect any price drop
                    )
                    
                    if is_price_drop:
                        # Find the previous lowest price
                        lowest_historical_price = min(float(p['price']) for p in historical_prices)
                        current_price_float = float(price_value)
                        savings = lowest_historical_price - current_price_float
                        savings_percent = (savings / lowest_historical_price) * 100
                        
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
                
                # Save the product data to CSV
                print(f"\n📝 Saving to storage...")
                success = data_storage.add_product(
                    product_name=scraped_data['name'],
                    product_url=scraped_data['url'],
                    current_price=price_value,
                    currency="₹",
                    image_url=""
                )
                
                if success:
                    print(f"✅ Product {idx} saved successfully!")
                    success_count += 1
                else:
                    print(f"❌ Failed to save product {idx}")
                    failed_count += 1
            else:
                print(f"❌ Failed to scrape product {idx}")
                failed_count += 1
            
            # Add delay between requests to avoid overwhelming the server
            if idx < len(products):
                print(f"\n⏳ Waiting 3 seconds before next product...")
                time.sleep(3)
        
        # Close browser
        browser.close()
        
        # Print summary
        print("\n" + "=" * 80)
        print("SCRAPING SUMMARY")
        print("=" * 80)
        print(f"✅ Successfully scraped and saved: {success_count}")
        print(f"❌ Failed: {failed_count}")
        print(f"📊 Total products: {len(products)}")
        print("=" * 80)


# Main execution
if __name__ == "__main__":
    scrape_all_products()
    
    # Display all stored products
    print("\n" + "=" * 80)
    print("STORED PRODUCTS")
    print("=" * 80)
    data_storage.display_products()
    
    print("\n✅ Multi-product scraping completed!")
