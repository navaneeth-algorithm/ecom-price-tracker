# Amazon Product Page Selectors

## Product URL
**Amazon India**: `https://www.amazon.in/Apple-Headphones-Cancellation-Transparency-Personalised/dp/B0DGJ6G1XG`

---

## Identified Selectors

### Product Name

**Recommended CSS Selector**: `#productTitle`

**Alternative Selectors**:
- `span#productTitle`
- `h1#title span#productTitle`
- `.a-size-large.product-title-word-break`

**Example Output**: 
```
Apple AirPods 4 Wireless Earbuds, Bluetooth Headphones, with Active Noise Cancellation, Adaptive Audio, Transparency Mode, Personalised Spatial Audio, USB-C Charging Case, Wireless Charging, H2 Chip
```

**HTML Structure**:
```html
<span id="productTitle" class="a-size-large product-title-word-break">
    Apple AirPods 4 Wireless Earbuds, Bluetooth Headphones...
</span>
```

---

### Product Price

**Recommended CSS Selector**: `.a-price .a-offscreen`

**Alternative Selectors**:
- `span.a-price-whole` (returns: "16,900.")
- `.a-price span[aria-hidden="true"]` (returns: "16,900.00")
- `.a-price-whole` (returns: "16,900")

**Example Output**: 
```
₹16,900.00
```

**HTML Structure**:
```html
<span class="a-price aok-align-center" data-a-size="xl" data-a-color="base">
    <span class="a-offscreen">₹16,900.00</span>
    <span aria-hidden="true">
        <span class="a-price-symbol">₹</span>
        <span class="a-price-whole">16,900<span class="a-price-decimal">.</span></span>
        <span class="a-price-fraction">00</span>
    </span>
</span>
```

---

## Usage Notes

1. **Product Name**: The `#productTitle` selector is the most reliable as it's a unique ID that Amazon consistently uses across product pages.

2. **Product Price**: The `.a-offscreen` class inside `.a-price` contains the full formatted price including currency symbol and is screen-reader accessible, making it the most reliable option.

3. **Price Format**: Amazon India uses ₹ (Rupee) symbol. The price format is: `₹16,900.00`

4. **Robustness**: These selectors have been tested and verified to work on Amazon India product pages as of January 2026.

---

## XPath Alternatives

### Product Name XPath
```xpath
//span[@id='productTitle']
```

### Product Price XPath
```xpath
//span[@class='a-price']//span[@class='a-offscreen']
```

---

## Implementation Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.amazon.in/...")
    
    # Get product name
    product_name = page.query_selector('#productTitle').inner_text().strip()
    
    # Get product price
    product_price = page.query_selector('.a-price .a-offscreen').inner_text().strip()
    
    print(f"Product: {product_name}")
    print(f"Price: {product_price}")
    
    browser.close()
```
