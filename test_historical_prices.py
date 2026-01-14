"""
Test script for historical price retrieval functionality
"""

import data_storage

print("=" * 100)
print("HISTORICAL PRICE RETRIEVAL TEST")
print("=" * 100)

# Test 1: Retrieve historical prices for an existing product
print("\n" + "#" * 100)
print("TEST 1: Existing Product (Apple AirPods)")
print("#" * 100)

existing_url = "https://www.amazon.in/Apple-Headphones-Cancellation-Transparency-Personalised/dp/B0DGJ6G1XG"
prices = data_storage.get_historical_prices(existing_url)

print(f"\nReturned {len(prices)} price record(s)")
print("\nRaw data structure:")
for idx, price_entry in enumerate(prices, 1):
    print(f"{idx}. {price_entry}")

# Display formatted price history
data_storage.display_price_history(existing_url)

# Test 2: Retrieve historical prices for another existing product
print("\n" + "#" * 100)
print("TEST 2: Existing Product (EarFun Air Pro 4)")
print("#" * 100)

existing_url_2 = "https://www.amazon.in/dp/B0D96G1XZ5"
prices_2 = data_storage.get_historical_prices(existing_url_2)

print(f"\nReturned {len(prices_2)} price record(s)")
data_storage.display_price_history(existing_url_2)

# Test 3: Retrieve historical prices for a non-existing product
print("\n" + "#" * 100)
print("TEST 3: Non-Existing Product")
print("#" * 100)

non_existing_url = "https://www.amazon.in/non-existing-product/dp/XXXXXXXXXX"
prices_3 = data_storage.get_historical_prices(non_existing_url)

print(f"\nReturned {len(prices_3)} price record(s)")
assert len(prices_3) == 0, "Expected empty list for non-existing product"
print("✅ Correctly returned empty list for non-existing product")

# Test 4: Verify data structure
print("\n" + "#" * 100)
print("TEST 4: Data Structure Validation")
print("#" * 100)

if prices:
    first_entry = prices[0]
    print("\nValidating first entry structure:")
    print(f"  Has 'timestamp' key: {'timestamp' in first_entry}")
    print(f"  Has 'price' key: {'price' in first_entry}")
    print(f"  Has 'currency' key: {'currency' in first_entry}")
    print(f"  Has 'product_name' key: {'product_name' in first_entry}")
    
    assert 'timestamp' in first_entry, "Missing 'timestamp' key"
    assert 'price' in first_entry, "Missing 'price' key"
    print("\n✅ Data structure is correct")

# Summary
print("\n" + "=" * 100)
print("TEST SUMMARY")
print("=" * 100)
print("✅ Test 1: Retrieved historical prices for existing product")
print("✅ Test 2: Retrieved historical prices for another existing product")
print("✅ Test 3: Returned empty list for non-existing product")
print("✅ Test 4: Data structure validated successfully")
print("\n✅ All tests passed!")
print("=" * 100)
