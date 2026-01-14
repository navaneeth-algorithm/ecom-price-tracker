"""
Unit Tests for Price Drop Detection Function
Tests various scenarios for the detect_price_drop function
"""

import data_storage

print("=" * 100)
print("PRICE DROP DETECTION UNIT TESTS")
print("=" * 100)

# Test counters
total_tests = 0
passed_tests = 0
failed_tests = 0

def run_test(test_name, result, expected, description=""):
    """Helper function to run and report test results"""
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    
    print(f"\n{'='*100}")
    print(f"Test {total_tests}: {test_name}")
    if description:
        print(f"Description: {description}")
    print(f"{'='*100}")
    
    if result == expected:
        print(f"✅ PASSED - Result: {result}, Expected: {expected}")
        passed_tests += 1
        return True
    else:
        print(f"❌ FAILED - Result: {result}, Expected: {expected}")
        failed_tests += 1
        return False


# Test 1: Empty historical prices list
print("\n" + "#" * 100)
print("SCENARIO 1: Empty Historical Prices List")
print("#" * 100)

result = data_storage.detect_price_drop(
    product_id="test_product_1",
    current_price=100,
    historical_prices_list=[],
    price_drop_threshold=0
)
run_test(
    "Empty Historical List",
    result,
    False,
    "Should return False when there are no historical prices to compare against"
)


# Test 2: New lowest price (no threshold)
print("\n" + "#" * 100)
print("SCENARIO 2: New Lowest Price (No Threshold)")
print("#" * 100)

historical_prices = [
    {'price': '150', 'timestamp': '2026-01-01'},
    {'price': '140', 'timestamp': '2026-01-02'},
    {'price': '130', 'timestamp': '2026-01-03'}
]
result = data_storage.detect_price_drop(
    product_id="test_product_2",
    current_price=120,
    historical_prices_list=historical_prices,
    price_drop_threshold=0
)
run_test(
    "New Lowest Price",
    result,
    True,
    "Current price (120) is lower than lowest historical price (130)"
)


# Test 3: Price increase
print("\n" + "#" * 100)
print("SCENARIO 3: Price Increase")
print("#" * 100)

result = data_storage.detect_price_drop(
    product_id="test_product_3",
    current_price=160,
    historical_prices_list=historical_prices,
    price_drop_threshold=0
)
run_test(
    "Price Increase",
    result,
    False,
    "Current price (160) is higher than lowest historical price (130)"
)


# Test 4: Price drop that meets threshold
print("\n" + "#" * 100)
print("SCENARIO 4: Price Drop Meets Threshold")
print("#" * 100)

historical_prices_2 = [
    {'price': '200', 'timestamp': '2026-01-01'},
    {'price': '180', 'timestamp': '2026-01-02'},
    {'price': '170', 'timestamp': '2026-01-03'}
]
result = data_storage.detect_price_drop(
    product_id="test_product_4",
    current_price=150,
    historical_prices_list=historical_prices_2,
    price_drop_threshold=10
)
run_test(
    "Price Drop Meets Threshold",
    result,
    True,
    "Current price (150) < (lowest 170 - threshold 10 = 160)"
)


# Test 5: Price drop that doesn't meet threshold
print("\n" + "#" * 100)
print("SCENARIO 5: Price Drop Doesn't Meet Threshold")
print("#" * 100)

result = data_storage.detect_price_drop(
    product_id="test_product_5",
    current_price=165,
    historical_prices_list=historical_prices_2,
    price_drop_threshold=10
)
run_test(
    "Price Drop Doesn't Meet Threshold",
    result,
    False,
    "Current price (165) > (lowest 170 - threshold 10 = 160)"
)


# Test 6: Current price equals lowest historical price
print("\n" + "#" * 100)
print("SCENARIO 6: Current Price Equals Lowest")
print("#" * 100)

result = data_storage.detect_price_drop(
    product_id="test_product_6",
    current_price=170,
    historical_prices_list=historical_prices_2,
    price_drop_threshold=0
)
run_test(
    "Price Equals Lowest",
    result,
    False,
    "Current price (170) equals lowest historical price (170)"
)


# Test 7: Single historical price
print("\n" + "#" * 100)
print("SCENARIO 7: Single Historical Price")
print("#" * 100)

single_price = [{'price': '100', 'timestamp': '2026-01-01'}]
result = data_storage.detect_price_drop(
    product_id="test_product_7",
    current_price=90,
    historical_prices_list=single_price,
    price_drop_threshold=5
)
run_test(
    "Single Historical Price with Drop",
    result,
    True,
    "Current price (90) < (single historical 100 - threshold 5 = 95)"
)


# Test 8: Large price drop
print("\n" + "#" * 100)
print("SCENARIO 8: Large Price Drop")
print("#" * 100)

high_prices = [
    {'price': '500', 'timestamp': '2026-01-01'},
    {'price': '480', 'timestamp': '2026-01-02'},
    {'price': '450', 'timestamp': '2026-01-03'}
]
result = data_storage.detect_price_drop(
    product_id="test_product_8",
    current_price=300,
    historical_prices_list=high_prices,
    price_drop_threshold=50
)
run_test(
    "Large Price Drop",
    result,
    True,
    "Current price (300) < (lowest 450 - threshold 50 = 400) - Significant savings!"
)


# Test 9: Price with decimal values
print("\n" + "#" * 100)
print("SCENARIO 9: Decimal Price Values")
print("#" * 100)

decimal_prices = [
    {'price': '99.99', 'timestamp': '2026-01-01'},
    {'price': '95.50', 'timestamp': '2026-01-02'}
]
result = data_storage.detect_price_drop(
    product_id="test_product_9",
    current_price=92.99,
    historical_prices_list=decimal_prices,
    price_drop_threshold=1.0
)
run_test(
    "Decimal Prices",
    result,
    True,
    "Current price (92.99) < (lowest 95.50 - threshold 1.0 = 94.50)"
)


# Test 10: String current price (should handle conversion)
print("\n" + "#" * 100)
print("SCENARIO 10: String Current Price")
print("#" * 100)

result = data_storage.detect_price_drop(
    product_id="test_product_10",
    current_price="85",  # String instead of number
    historical_prices_list=decimal_prices,
    price_drop_threshold=0
)
run_test(
    "String Current Price",
    result,
    True,
    "Should handle string to float conversion for current price"
)


# Print Summary
print("\n" + "=" * 100)
print("TEST SUMMARY")
print("=" * 100)
print(f"Total Tests Run: {total_tests}")
print(f"✅ Passed: {passed_tests}")
print(f"❌ Failed: {failed_tests}")
print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
print("=" * 100)

if failed_tests == 0:
    print("\n🎉 All tests passed successfully!")
else:
    print(f"\n⚠️  {failed_tests} test(s) failed. Please review the results above.")

print("=" * 100)
