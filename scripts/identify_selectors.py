from playwright.sync_api import sync_playwright

# Define the target e-commerce product URL
product_url = "https://www.amazon.in/Apple-Headphones-Cancellation-Transparency-Personalised/dp/B0DGJ6G1XG/ref=sr_1_1_sspa?adgrpid=60423959193&dib=eyJ2IjoiMSJ9.u0qvNrJHJIrE5QifMkx1jlpMG7NKYwxdWccPB7wP4q_vBM2RdP7XnY0k9VdUPsZZnl0l1BqgBCMCnV6CLSl64TiVx4lzj0UfFneVt1ow25r8gfQxnJ_sVOIwogX041BQgJ2LVaZrDLdr_8-jvrMzNKoLvm3IgnhNViAz2TKFcji9IFJ2YVZ6F_VdX7C3_1YlhK2zJEfRZHsxzoNjec9VdOCFl8GBN19reuNA1nXjfgY.hvh6TwBX7i4DyLvXXv9fASGG4Wuv9SEAEizWUdi5KeE&dib_tag=se&ext_vrnc=hi&hvadid=499120301018&hvdev=c&hvlocphy=1007772&hvnetw=g&hvqmt=b&hvrand=8726249873821178465&hvtargid=kwd-2266190195216&hydadcr=831_2482203&keywords=airpods%2F&mcid=0634dd9192fe3f74a5c1ffb081325fa5&qid=1768386571&sr=8-1-spons&aref=gFgUy9dUWO&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"

print(f"Analyzing product page: {product_url}\n")

with sync_playwright() as p:
    # Launch Chromium browser in headless mode
    browser = p.chromium.launch(headless=False)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    
    # Navigate to the product URL
    page.goto(product_url, wait_until='domcontentloaded')
    
    # Wait for page to load
    page.wait_for_timeout(3000)  # Wait 3 seconds for dynamic content
    
    print("=" * 80)
    print("PRODUCT NAME SELECTORS")
    print("=" * 80)
    
    # Common Amazon product name selectors
    name_selectors = [
        '#productTitle',
        'span#productTitle',
        '[data-a-size="large"]#productTitle',
        'h1#title span#productTitle',
        'h1.product-title-word-break span'
    ]
    
    for selector in name_selectors:
        try:
            element = page.query_selector(selector)
            if element:
                text = element.inner_text().strip()
                if text:
                    print(f"\n✓ CSS Selector: {selector}")
                    print(f"  Product Name: {text[:100]}...")
        except:
            pass
    
    print("\n" + "=" * 80)
    print("PRODUCT PRICE SELECTORS")
    print("=" * 80)
    
    # Common Amazon price selectors
    price_selectors = [
        '.a-price .a-offscreen',
        'span.a-price-whole',
        '.a-price span[aria-hidden="true"]',
        '#corePriceDisplay_desktop_feature_div .a-price .a-offscreen',
        '#corePrice_feature_div .a-price .a-offscreen',
        '.a-section.a-spacing-small .a-price .a-offscreen',
        'span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-offscreen',
        '.a-price-whole',
        '#corePrice_desktop .a-price .a-offscreen',
        '#priceblock_ourprice',
        '#priceblock_dealprice',
        '.a-offscreen'
    ]
    
    found_prices = []
    for selector in price_selectors:
        try:
            elements = page.query_selector_all(selector)
            for element in elements:
                text = element.inner_text().strip()
                if text and ('$' in text or text.replace('.', '').replace(',', '').isdigit()):
                    if text not in [p[1] for p in found_prices]:
                        found_prices.append((selector, text))
                        print(f"\n✓ CSS Selector: {selector}")
                        print(f"  Price: {text}")
                        break
        except:
            pass
    
    # Try to get the HTML structure for manual inspection
    print("\n" + "=" * 80)
    print("HTML STRUCTURE (for manual verification)")
    print("=" * 80)
    
    # Get product title HTML
    try:
        title_element = page.query_selector('#productTitle')
        if title_element:
            print("\nProduct Title HTML:")
            print(page.evaluate('(element) => element.outerHTML', title_element)[:500])
    except:
        pass
    
    # Get price HTML
    try:
        price_elements = page.query_selector_all('.a-price')
        if price_elements:
            print(f"\nFound {len(price_elements)} price elements:")
            for i, price_element in enumerate(price_elements[:3]):  # Show first 3
                print(f"\nPrice Element {i+1} HTML:")
                html = page.evaluate('(element) => element.outerHTML', price_element)
                print(html[:500])
    except Exception as e:
        print(f"Error getting price HTML: {e}")
    
    # Try to get all text with $ symbol
    try:
        all_text = page.content()
        import re
        prices_in_page = re.findall(r'\$[\d,]+\.?\d*', all_text)
        if prices_in_page:
            print(f"\nAll prices found in page (first 10):")
            for price in list(set(prices_in_page))[:10]:
                print(f"  {price}")
    except:
        pass
    
    browser.close()

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
