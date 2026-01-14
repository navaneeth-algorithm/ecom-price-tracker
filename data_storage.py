"""
Data Storage Module for E-commerce Price Tracker
Handles CSV file initialization and data operations
"""

import csv
import os
from datetime import datetime
from pathlib import Path

# CSV file configuration
CSV_FILE = "products.csv"

# Define the product data schema
PRODUCT_SCHEMA = [
    "product_id",
    "product_name",
    "product_url",
    "current_price",
    "currency",
    "last_updated",
    "image_url"
]


def setup_storage():
    """
    Initialize CSV storage if it doesn't exist.
    Creates a CSV file with headers based on the defined schema.
    Does nothing if the file already exists.
    
    Returns:
        bool: True if storage was created, False if it already existed
    """
    file_path = Path(CSV_FILE)
    
    # Check if CSV file already exists
    if file_path.exists():
        print(f"✓ Storage already exists: {CSV_FILE}")
        return False
    
    # Create new CSV file with headers
    try:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(PRODUCT_SCHEMA)
        
        print(f"✓ Storage initialized successfully: {CSV_FILE}")
        print(f"  Schema: {', '.join(PRODUCT_SCHEMA)}")
        return True
    
    except Exception as e:
        print(f"✗ Error initializing storage: {e}")
        raise


def add_product(product_name, product_url, current_price, currency="₹", image_url=""):
    """
    Add a new product to the CSV storage.
    
    Args:
        product_name (str): Name of the product
        product_url (str): URL of the product page
        current_price (str): Current price of the product
        currency (str): Currency symbol (default: ₹)
        image_url (str): URL of the product image (optional)
    
    Returns:
        bool: True if product was added successfully
    """
    try:
        # Generate a simple product ID based on timestamp
        product_id = datetime.now().strftime("%Y%m%d%H%M%S")
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare product data
        product_data = [
            product_id,
            product_name,
            product_url,
            current_price,
            currency,
            last_updated,
            image_url
        ]
        
        # Append to CSV file
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(product_data)
        
        print(f"✓ Product added: {product_name} - {currency}{current_price}")
        return True
    
    except Exception as e:
        print(f"✗ Error adding product: {e}")
        return False


def get_all_products():
    """
    Retrieve all products from the CSV storage.
    
    Returns:
        list: List of dictionaries containing product data
    """
    products = []
    
    try:
        if not Path(CSV_FILE).exists():
            print("✗ Storage file not found. Run setup_storage() first.")
            return products
        
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            products = list(reader)
        
        print(f"✓ Retrieved {len(products)} product(s)")
        return products
    
    except Exception as e:
        print(f"✗ Error reading products: {e}")
        return products


def display_products():
    """
    Display all products in a formatted table.
    """
    products = get_all_products()
    
    if not products:
        print("No products found in storage.")
        return
    
    print("\n" + "=" * 100)
    print("STORED PRODUCTS")
    print("=" * 100)
    
    for idx, product in enumerate(products, 1):
        print(f"\n{idx}. {product['product_name']}")
        print(f"   Price: {product['currency']}{product['current_price']}")
        print(f"   Last Updated: {product['last_updated']}")
        print(f"   URL: {product['product_url'][:80]}...")
    
    print("\n" + "=" * 100)


# Main execution for testing
if __name__ == "__main__":
    print("=" * 80)
    print("CSV STORAGE INITIALIZATION")
    print("=" * 80)
    print()
    
    # Initialize storage
    setup_storage()
    
    print("\n" + "=" * 80)
    print("TESTING SECOND INITIALIZATION (should not recreate)")
    print("=" * 80)
    print()
    
    # Test that it doesn't recreate on second run
    setup_storage()
    
    print("\n✅ Storage setup complete!")
