"""
Test Price Drop Notification Integration
Simulates a price drop scenario to test the notification system
"""

import data_storage
from datetime import datetime

print("=" * 100)
print("PRICE DROP NOTIFICATION INTEGRATION TEST")
print("=" * 100)

# Test product URL
test_url = "https://www.amazon.in/dp/B0G12JYP7G"

print("\n" + "#" * 100)
print("STEP 1: Get Historical Prices")
print("#" * 100)

historical_prices = data_storage.get_historical_prices(test_url)
data_storage.display_price_history(test_url)

print("\n" + "#" * 100)
print("STEP 2: Simulate New Lower Price")
print("#" * 100)

# Simulate a new lower price (lower than the current lowest)
if historical_prices:
    lowest_price = min(float(p['price']) for p in historical_prices)
    new_lower_price = lowest_price - 200  # 200 rupees less
    
    print(f"\nCurrent Lowest Price: ₹{lowest_price:,.2f}")
    print(f"Simulated New Price: ₹{new_lower_price:,.2f}")
    
    print("\n" + "#" * 100)
    print("STEP 3: Check for Price Drop")
    print("#" * 100)
    
    is_price_drop = data_storage.detect_price_drop(
        product_id=test_url,
        current_price=new_lower_price,
        historical_prices_list=historical_prices,
        price_drop_threshold=0
    )
    
    if is_price_drop:
        savings = lowest_price - new_lower_price
        savings_percent = (savings / lowest_price) * 100
        
        print("\n" + "#" * 100)
        print("STEP 4: Display Price Drop Notification (As seen in main script)")
        print("#" * 100)
        
        # This is exactly what the main script will show
        print("\n" + "🎉" * 40)
        print("🚨 PRICE DROP ALERT! 🚨")
        print("🎉" * 40)
        print(f"\n📦 Product: {historical_prices[0]['product_name'][:80]}...")
        print(f"💰 New Price: ₹{new_lower_price:,.2f}")
        print(f"📉 Previous Lowest: ₹{lowest_price:,.2f}")
        print(f"💵 You Save: ₹{savings:,.2f} ({savings_percent:.2f}% OFF)")
        print(f"🔗 URL: {test_url[:60]}...")
        print("\n" + "🎉" * 40)
        
        print("\n✅ Price drop notification displayed successfully!")
    else:
        print("\n⚠️  No price drop detected (this shouldn't happen in this test)")

else:
    print("\n⚠️  No historical prices found. Please run track_all_products.py first to generate data.")

print("\n" + "=" * 100)
print("TEST COMPLETE")
print("=" * 100)
print("\nTo see this in action with real scraping:")
print("1. Run: python track_all_products.py")
print("2. The script will detect if any product has a lower price than before")
print("3. A price drop notification will be displayed if detected")
print("=" * 100)
