"""
Product URL Loader Module
Loads and manages product URLs from products.json configuration file
"""

import json
import os
from pathlib import Path

# Configuration file path
PRODUCTS_FILE = "products.json"


def load_product_urls():
    """
    Load product URLs from the products.json configuration file.
    
    Returns:
        list: List of product URL strings from active products
    
    Raises:
        FileNotFoundError: If products.json doesn't exist
        json.JSONDecodeError: If products.json is not valid JSON
    """
    file_path = Path(PRODUCTS_FILE)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file '{PRODUCTS_FILE}' not found. Please create it first.")
    
    try:
        # Read and parse JSON file
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
            products = json.load(file)
        
        # Extract URLs from active products only
        urls = [product['url'] for product in products if product.get('active', True)]
        
        print(f"✓ Loaded {len(urls)} product URL(s) from {PRODUCTS_FILE}")
        return urls
    
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing JSON file: {e}")
        raise
    except Exception as e:
        print(f"✗ Error loading product URLs: {e}")
        raise


def load_products():
    """
    Load complete product information from the products.json configuration file.
    
    Returns:
        list: List of product dictionaries with all details
    
    Raises:
        FileNotFoundError: If products.json doesn't exist
        json.JSONDecodeError: If products.json is not valid JSON
    """
    file_path = Path(PRODUCTS_FILE)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file '{PRODUCTS_FILE}' not found.")
    
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
            products = json.load(file)
        
        # Filter only active products
        active_products = [p for p in products if p.get('active', True)]
        
        print(f"✓ Loaded {len(active_products)} active product(s) from {PRODUCTS_FILE}")
        return active_products
    
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing JSON file: {e}")
        raise
    except Exception as e:
        print(f"✗ Error loading products: {e}")
        raise


def add_product_to_config(name, url, category="General", active=True):
    """
    Add a new product to the products.json configuration file.
    
    Args:
        name (str): Product name
        url (str): Product URL
        category (str): Product category (default: "General")
        active (bool): Whether product tracking is active (default: True)
    
    Returns:
        bool: True if product was added successfully
    """
    try:
        # Load existing products
        products = []
        if Path(PRODUCTS_FILE).exists():
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
                products = json.load(file)
        
        # Generate new ID
        new_id = max([p.get('id', 0) for p in products], default=0) + 1
        
        # Create new product entry
        new_product = {
            "id": new_id,
            "name": name,
            "url": url,
            "category": category,
            "active": active
        }
        
        # Add to products list
        products.append(new_product)
        
        # Save back to file
        with open(PRODUCTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(products, file, indent=2, ensure_ascii=False)
        
        print(f"✓ Added product: {name}")
        return True
    
    except Exception as e:
        print(f"✗ Error adding product: {e}")
        return False


def display_products_config():
    """
    Display all products from the configuration in a formatted table.
    """
    try:
        products = load_products()
        
        if not products:
            print("No products found in configuration.")
            return
        
        print("\n" + "=" * 100)
        print("PRODUCT TRACKING CONFIGURATION")
        print("=" * 100)
        
        for product in products:
            print(f"\n{product['id']}. {product['name']}")
            print(f"   Category: {product['category']}")
            print(f"   URL: {product['url'][:80]}...")
            print(f"   Active: {'Yes' if product.get('active', True) else 'No'}")
        
        print("\n" + "=" * 100)
    
    except Exception as e:
        print(f"✗ Error displaying products: {e}")


# Main execution for testing
if __name__ == "__main__":
    print("=" * 80)
    print("PRODUCT URL LOADER TEST")
    print("=" * 80)
    print()
    
    try:
        # Load product URLs
        urls = load_product_urls()
        
        print("\n" + "=" * 80)
        print("ITERATING THROUGH PRODUCT URLS")
        print("=" * 80)
        
        # Iterate and print each URL
        for idx, url in enumerate(urls, 1):
            print(f"\n{idx}. {url}")
        
        print("\n" + "=" * 80)
        print("COMPLETE PRODUCT INFORMATION")
        print("=" * 80)
        
        # Display complete product configuration
        display_products_config()
        
        print("\n✅ Product URL loading test completed successfully!")
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
