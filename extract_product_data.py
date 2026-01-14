from playwright.sync_api import sync_playwright

# Define the target e-commerce product URL (simplified)
product_url = "https://www.amazon.in/Apple-Headphones-Cancellation-Transparency-Personalised/dp/B0DGJ6G1XG"

print("=" * 80)
print("E-COMMERCE PRODUCT PRICE TRACKER")
print("=" * 80)
print(f"\nFetching product details from: {product_url}\n")

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
    
    # Print the extracted data in a formatted manner
    print("=" * 80)
    print("EXTRACTED PRODUCT INFORMATION")
    print("=" * 80)
    print(f"\n📦 Product Name:\n   {product_name}\n")
    print(f"💰 Product Price:\n   {product_price}\n")
    print("=" * 80)
    
    # Close the browser
    browser.close()

print("\n✅ Data extraction completed successfully!")
