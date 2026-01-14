from playwright.sync_api import sync_playwright

# Define the target e-commerce product URL
product_url = "https://www.amazon.com/dp/B0D1XD1ZV3"

# Launch browser and capture screenshot
with sync_playwright() as p:
    # Launch Chromium browser in headless mode
    browser = p.chromium.launch(headless=True)
    
    # Create a new browser page
    page = browser.new_page()
    
    # Navigate to the product URL
    page.goto(product_url)
    
    # Capture full-page screenshot
    page.screenshot(path='product_page.png', full_page=True)
    
    # Close the browser
    browser.close()

print("Screenshot saved successfully as 'product_page.png'")
