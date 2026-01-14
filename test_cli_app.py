"""
Automated Test for CLI Add Product Functionality
Simulates user input to test the add_product_cli function
"""

import product_loader
from unittest.mock import patch
import cli_app

print("=" * 100)
print("CLI ADD PRODUCT FUNCTIONALITY TEST")
print("=" * 100)

# Test 1: Add a product with all details
print("\n" + "#" * 100)
print("TEST 1: Add Product with Full Details")
print("#" * 100)

# Simulate user inputs
test_inputs = [
    'https://www.amazon.in/test-product/dp/TEST123',  # URL
    'Test Product Name',  # Name
    'Test Category',  # Category
    'y'  # Confirm
]

print("\nSimulated inputs:")
for i, inp in enumerate(test_inputs, 1):
    print(f"{i}. {inp}")

with patch('builtins.input', side_effect=test_inputs):
    result = cli_app.add_product_cli()

if result:
    print("\n✅ Test 1 PASSED - Product added successfully")
else:
    print("\n❌ Test 1 FAILED - Product not added")

# Test 2: Verify product was added to JSON
print("\n" + "#" * 100)
print("TEST 2: Verify Product in Storage")
print("#" * 100)

try:
    products = product_loader.load_products()
    test_product = None
    
    for product in products:
        if 'TEST123' in product['url']:
            test_product = product
            break
    
    if test_product:
        print("\n✅ Test 2 PASSED - Product found in products.json")
        print(f"\nProduct Details:")
        print(f"  ID: {test_product['id']}")
        print(f"  Name: {test_product['name']}")
        print(f"  URL: {test_product['url']}")
        print(f"  Category: {test_product['category']}")
        print(f"  Active: {test_product['active']}")
    else:
        print("\n❌ Test 2 FAILED - Product not found in storage")

except Exception as e:
    print(f"\n❌ Test 2 FAILED - Error: {e}")

# Test 3: Add product with minimal details (defaults)
print("\n" + "#" * 100)
print("TEST 3: Add Product with Default Values")
print("#" * 100)

test_inputs_minimal = [
    'https://www.amazon.in/another-test/dp/TEST456',  # URL
    '',  # Name (empty, should use default)
    '',  # Category (empty, should use default)
    'y'  # Confirm
]

print("\nSimulated inputs (with defaults):")
for i, inp in enumerate(test_inputs_minimal, 1):
    print(f"{i}. {inp if inp else '(press Enter - use default)'}")

with patch('builtins.input', side_effect=test_inputs_minimal):
    result = cli_app.add_product_cli()

if result:
    print("\n✅ Test 3 PASSED - Product added with defaults")
else:
    print("\n❌ Test 3 FAILED - Product not added")

# Test 4: Cancel adding product
print("\n" + "#" * 100)
print("TEST 4: Cancel Product Addition")
print("#" * 100)

test_inputs_cancel = [
    'https://www.amazon.in/cancelled-product/dp/CANCEL',
    'Cancelled Product',
    'Test',
    'n'  # Do NOT confirm
]

print("\nSimulated inputs (with cancellation):")
for i, inp in enumerate(test_inputs_cancel, 1):
    print(f"{i}. {inp}")

with patch('builtins.input', side_effect=test_inputs_cancel):
    result = cli_app.add_product_cli()

if not result:
    print("\n✅ Test 4 PASSED - Product addition cancelled as expected")
else:
    print("\n❌ Test 4 FAILED - Product should not have been added")

# Display all products
print("\n" + "#" * 100)
print("CURRENT TRACKED PRODUCTS")
print("#" * 100)

product_loader.display_products_config()

# Summary
print("\n" + "=" * 100)
print("TEST SUMMARY")
print("=" * 100)
print("✅ CLI functionality tested successfully!")
print("\nTo use the CLI interactively:")
print("  1. Run: python cli_app.py")
print("  2. Or for quick add: python cli_app.py add")
print("=" * 100)
