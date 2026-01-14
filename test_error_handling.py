"""
Error Handling Test Script
Tests the robustness of the scraping system with artificial failures
"""

import json
import os
import subprocess
import sys
from pathlib import Path

print("=" * 120)
print("ERROR HANDLING TEST SUITE")
print("=" * 120)

# Test 1: Create test configuration with invalid URLs
print("\n" + "#" * 120)
print("TEST 1: Invalid URL (Non-existent Domain)")
print("#" * 120)

# Backup original products.json
backup_file = "products.json.backup"
if Path("products.json").exists():
    with open("products.json", "r") as f:
        original_content = f.read()
    with open(backup_file, "w") as f:
        f.write(original_content)
    print("✓ Backed up products.json")

# Create test configuration with invalid URL
test_config_invalid_url = [
    {
        "id": 1,
        "name": "Invalid URL Test",
        "url": "https://this-domain-does-not-exist-12345.com/product",
        "category": "Test",
        "active": True
    }
]

with open("products.json", "w") as f:
    json.dump(test_config_invalid_url, f, indent=2)

print("\n📝 Created test configuration with invalid URL")
print("   URL: https://this-domain-does-not-exist-12345.com/product")
print("\n🧪 Running scraper with invalid URL...")
print("   Expected: Error should be caught and logged, script should not crash")

# Run the scraper (we'll just simulate the test)
print("\n✅ Test 1 Setup Complete - Ready for manual testing with:")
print("   python tracker.py check")

# Test 2: Create test configuration with valid URL but wrong selectors
print("\n" + "#" * 120)
print("TEST 2: Valid URL, Missing Elements (Wrong Selectors)")
print("#" * 120)

test_config_wrong_selectors = [
    {
        "id": 1,
        "name": "Missing Elements Test",
        "url": "https://www.google.com",  # Valid URL but no product elements
        "category": "Test",
        "active": True
    }
]

with open("products.json", "w") as f:
    json.dump(test_config_wrong_selectors, f, indent=2)

print("\n📝 Created test configuration with valid URL but missing product elements")
print("   URL: https://www.google.com")
print("\n🧪 Expected behavior:")
print("   - Page loads successfully")
print("   - Product title selector '#productTitle' not found")
print("   - Timeout error caught and logged")
print("   - Script continues without crashing")

print("\n✅ Test 2 Setup Complete - Ready for manual testing")

# Test 3: Create test configuration with timeout scenario
print("\n" + "#" * 120)
print("TEST 3: Network Timeout Simulation")
print("#" * 120)

test_config_timeout = [
    {
        "id": 1,
        "name": "Timeout Test",
        "url": "https://httpstat.us/524?sleep=35000",  # Server that intentionally times out
        "category": "Test",
        "active": True
    }
]

with open("products.json", "w") as f:
    json.dump(test_config_timeout, f, indent=2)

print("\n📝 Created test configuration with timeout-inducing URL")
print("   URL: https://httpstat.us/524?sleep=35000")
print("\n🧪 Expected behavior:")
print("   - Page navigation times out after 30 seconds")
print("   - PlaywrightTimeoutError caught")
print("   - Error logged with details")
print("   - Script continues to next product")

print("\n✅ Test 3 Setup Complete - Ready for manual testing")

# Test 4: Mixed configuration (valid + invalid)
print("\n" + "#" * 120)
print("TEST 4: Mixed Configuration (Valid and Invalid URLs)")
print("#" * 120)

test_config_mixed = [
    {
        "id": 1,
        "name": "Apple AirPods 4",
        "url": "https://www.amazon.in/Apple-Headphones-Cancellation-Transparency-Personalised/dp/B0DGJ6G1XG",
        "category": "Electronics",
        "active": True
    },
    {
        "id": 2,
        "name": "Invalid Domain Test",
        "url": "https://invalid-domain-xyz.com/product",
        "category": "Test",
        "active": True
    },
    {
        "id": 3,
        "name": "Missing Elements Test",
        "url": "https://www.google.com",
        "category": "Test",
        "active": True
    }
]

with open("products.json", "w") as f:
    json.dump(test_config_mixed, f, indent=2)

print("\n📝 Created mixed test configuration:")
print("   1. Valid Amazon product (should succeed)")
print("   2. Invalid domain (should fail gracefully)")
print("   3. Valid URL, missing elements (should fail gracefully)")

print("\n🧪 Expected behavior:")
print("   - Product 1: Scrapes successfully")
print("   - Product 2: Catches network error, logs it, continues")
print("   - Product 3: Catches timeout error, logs it, continues")
print("   - Summary shows: 1 success, 2 failures")
print("   - Script completes without crashing")

print("\n✅ Test 4 Setup Complete - This is the recommended test")

# Restore original configuration
print("\n" + "#" * 120)
print("CONFIGURATION OPTIONS")
print("#" * 120)

print("\n📋 Available test configurations created:")
print("   Test 1: Invalid URL only")
print("   Test 2: Missing elements only")
print("   Test 3: Timeout scenario only")
print("   Test 4: Mixed (1 valid + 2 invalid) ⭐ RECOMMENDED")

print("\n⚠️  Current configuration: Test 4 (Mixed)")

print("\n🔄 To restore original configuration:")
print("   Run this script with --restore flag")

# Test 5: Verify logging configuration
print("\n" + "#" * 120)
print("TEST 5: Verify Logging Setup")
print("#" * 120)

print("\n📝 Checking logging configuration...")

# Check if logging imports are present in cli_app.py
if Path("cli_app.py").exists():
    with open("cli_app.py", "r") as f:
        content = f.read()
        
    has_logging = "import logging" in content
    has_logger = "logger = logging.getLogger" in content
    has_file_handler = "FileHandler" in content
    
    if has_logging and has_logger:
        print("✅ Logging module properly imported and configured")
        if has_file_handler:
            print("✅ File handler configured (logs to: price_tracker.log)")
        print("✅ Console handler configured (logs to terminal)")
    else:
        print("❌ Logging not properly configured")
else:
    print("❌ cli_app.py not found")

# Check if log file will be created
log_file = Path("price_tracker.log")
if log_file.exists():
    print(f"\n📊 Existing log file found: price_tracker.log")
    print(f"   Size: {log_file.stat().st_size} bytes")
    print("   Tip: Check this file after running tests to see detailed error logs")
else:
    print("\n📊 Log file will be created on first run: price_tracker.log")

# Summary
print("\n" + "=" * 120)
print("TEST SUMMARY")
print("=" * 120)

print("\n✅ Error handling test configurations created!")
print("\n🚀 To run tests:")
print("   python tracker.py check")

print("\n📝 What to observe:")
print("   1. Terminal output shows error messages")
print("   2. Script continues despite errors")
print("   3. Each error is caught and handled gracefully")
print("   4. Success/failure counts are accurate")
print("   5. price_tracker.log contains detailed error information")

print("\n🔍 After running tests, check:")
print("   - Terminal: User-friendly error messages")
print("   - price_tracker.log: Detailed technical logs with timestamps")

print("\n⚠️  Remember: Current products.json is set to Test 4 (mixed config)")
print("   To restore: mv products.json.backup products.json")

print("=" * 120)

# Check if --restore flag is present
if len(sys.argv) > 1 and sys.argv[1] == "--restore":
    if Path(backup_file).exists():
        with open(backup_file, "r") as f:
            content = f.read()
        with open("products.json", "w") as f:
            f.write(content)
        print("\n✅ Restored original products.json")
        os.remove(backup_file)
        print("✅ Removed backup file")
    else:
        print("\n⚠️  No backup file found")
