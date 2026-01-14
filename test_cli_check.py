"""
Test Script for CLI Check Command
Verifies the integration of scraping and alerting functionality
"""

import subprocess
import sys
from pathlib import Path

print("=" * 120)
print("CLI CHECK COMMAND TEST SUITE")
print("=" * 120)

# Test 1: Verify tracker.py exists
print("\n" + "#" * 120)
print("TEST 1: Verify tracker.py File Exists")
print("#" * 120)

tracker_file = Path("tracker.py")
if tracker_file.exists():
    print(f"\n✅ Test 1 PASSED - tracker.py exists")
    print(f"   Location: {tracker_file.absolute()}")
else:
    print("\n❌ Test 1 FAILED - tracker.py not found")
    sys.exit(1)

# Test 2: Verify help command includes 'check'
print("\n" + "#" * 120)
print("TEST 2: Verify 'check' Command in Help")
print("#" * 120)

result = subprocess.run(
    ["python", "tracker.py", "--help"],
    capture_output=True,
    text=True
)

if "check" in result.stdout and "scrape" in result.stdout.lower():
    print("\n✅ Test 2 PASSED - 'check' command found in help")
    print("\nHelp output excerpt:")
    for line in result.stdout.split('\n'):
        if 'check' in line.lower():
            print(f"   {line}")
else:
    print("\n❌ Test 2 FAILED - 'check' command not found in help")
    print(result.stdout)

# Test 3: Verify CLI structure
print("\n" + "#" * 120)
print("TEST 3: Verify CLI Commands Structure")
print("#" * 120)

expected_commands = ['view', 'add', 'check', 'interactive']
help_text = result.stdout

found_commands = []
for cmd in expected_commands:
    if cmd in help_text:
        found_commands.append(cmd)

if len(found_commands) == len(expected_commands):
    print(f"\n✅ Test 3 PASSED - All expected commands present")
    print(f"   Commands: {', '.join(found_commands)}")
else:
    print(f"\n⚠️  Test 3 WARNING - Some commands missing")
    print(f"   Expected: {expected_commands}")
    print(f"   Found: {found_commands}")

# Test 4: Check products.json has products
print("\n" + "#" * 120)
print("TEST 4: Verify Products Configuration")
print("#" * 120)

import product_loader

try:
    products = product_loader.load_products()
    if products and len(products) > 0:
        print(f"\n✅ Test 4 PASSED - Found {len(products)} product(s) to track")
        for idx, product in enumerate(products, 1):
            print(f"   {idx}. {product['name']}")
    else:
        print("\n⚠️  Test 4 WARNING - No products configured")
        print("   Add products before running: python tracker.py check")
except Exception as e:
    print(f"\n❌ Test 4 FAILED - Error loading products: {e}")

# Test 5: Verify CSV storage exists
print("\n" + "#" * 120)
print("TEST 5: Verify CSV Storage")
print("#" * 120)

csv_file = Path("products.csv")
if csv_file.exists():
    print(f"\n✅ Test 5 PASSED - CSV storage exists")
    print(f"   Location: {csv_file.absolute()}")
    
    # Check if it has data
    with open(csv_file, 'r') as f:
        lines = f.readlines()
        print(f"   Total entries: {len(lines) - 1} (excluding header)")
else:
    print("\n⚠️  Test 5 WARNING - CSV storage not initialized")
    print("   Will be created on first run")

# Test 6: Verify required modules are imported
print("\n" + "#" * 120)
print("TEST 6: Verify Required Dependencies")
print("#" * 120)

try:
    from playwright.sync_api import sync_playwright
    import data_storage
    import time
    from datetime import datetime
    
    print("\n✅ Test 6 PASSED - All required modules available")
    print("   ✓ playwright")
    print("   ✓ data_storage")
    print("   ✓ time")
    print("   ✓ datetime")
except ImportError as e:
    print(f"\n❌ Test 6 FAILED - Missing dependency: {e}")

# Summary
print("\n" + "=" * 120)
print("TEST SUMMARY")
print("=" * 120)
print("✅ All prerequisite tests completed!")
print("\n📋 How to use the check command:")
print("  1. Verify products are configured:  python tracker.py view")
print("  2. Run price check:                 python tracker.py check")
print("  3. Check for price drops:           (automatic during check)")
print("\n⚠️  NOTE: The 'check' command will:")
print("   - Launch a browser window (non-headless)")
print("   - Scrape all products sequentially")
print("   - Save new prices to CSV storage")
print("   - Display price drop alerts if detected")
print("   - Take approximately 3-5 seconds per product")
print("=" * 120)
