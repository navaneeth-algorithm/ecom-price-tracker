"""
Command-Line Interface for E-commerce Price Tracker
Provides interactive commands to manage tracked products
"""

import product_loader
import data_storage
import sys


def display_menu():
    """Display the main menu options"""
    print("\n" + "=" * 80)
    print("E-COMMERCE PRICE TRACKER - CLI")
    print("=" * 80)
    print("\nAvailable Commands:")
    print("  1. Add Product         - Add a new product to track")
    print("  2. List Products       - View all tracked products")
    print("  3. View Price History  - Check price history for a product")
    print("  4. Remove Product      - Remove a product from tracking")
    print("  5. Exit                - Exit the application")
    print("=" * 80)


def add_product_cli():
    """
    Interactive function to add a new product to track.
    Prompts user for product URL, name, and category.
    """
    print("\n" + "=" * 80)
    print("ADD NEW PRODUCT TO TRACK")
    print("=" * 80)
    
    # Prompt for product URL
    print("\n📝 Enter product details:")
    product_url = input("Product URL: ").strip()
    
    if not product_url:
        print("❌ Error: Product URL cannot be empty!")
        return False
    
    # Validate URL format
    if not (product_url.startswith('http://') or product_url.startswith('https://')):
        print("❌ Error: Please enter a valid URL (starting with http:// or https://)")
        return False
    
    # Prompt for product name
    product_name = input("Product Name (optional, press Enter to skip): ").strip()
    if not product_name:
        product_name = f"Product-{product_url.split('/')[-1][:20]}"
    
    # Prompt for category
    product_category = input("Category (default: Electronics): ").strip()
    if not product_category:
        product_category = "Electronics"
    
    # Confirm before adding
    print("\n" + "-" * 80)
    print("CONFIRM PRODUCT DETAILS:")
    print("-" * 80)
    print(f"Name: {product_name}")
    print(f"URL: {product_url}")
    print(f"Category: {product_category}")
    print("-" * 80)
    
    confirm = input("\nAdd this product? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Product not added.")
        return False
    
    # Add product to configuration
    success = product_loader.add_product_to_config(
        name=product_name,
        url=product_url,
        category=product_category,
        active=True
    )
    
    if success:
        print("\n✅ Product added successfully to tracking list!")
        return True
    else:
        print("\n❌ Failed to add product.")
        return False


def list_products_cli():
    """Display all tracked products"""
    print("\n" + "=" * 80)
    print("TRACKED PRODUCTS")
    print("=" * 80)
    
    try:
        product_loader.display_products_config()
    except Exception as e:
        print(f"❌ Error loading products: {e}")


def view_price_history_cli():
    """View price history for a specific product"""
    print("\n" + "=" * 80)
    print("VIEW PRICE HISTORY")
    print("=" * 80)
    
    try:
        # Show available products first
        products = product_loader.load_products()
        
        if not products:
            print("\n⚠️  No products found. Add products first!")
            return
        
        print("\nAvailable Products:")
        for idx, product in enumerate(products, 1):
            print(f"{idx}. {product['name']}")
        
        # Get user selection
        choice = input("\nEnter product number (or 'q' to cancel): ").strip()
        
        if choice.lower() == 'q':
            return
        
        try:
            product_idx = int(choice) - 1
            if 0 <= product_idx < len(products):
                selected_product = products[product_idx]
                data_storage.display_price_history(selected_product['url'])
            else:
                print("❌ Invalid product number!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    except Exception as e:
        print(f"❌ Error: {e}")


def remove_product_cli():
    """Remove a product from tracking"""
    print("\n" + "=" * 80)
    print("REMOVE PRODUCT")
    print("=" * 80)
    print("\n⚠️  This feature will be implemented in a future update.")
    print("For now, manually edit products.json to remove products.")


def main():
    """Main CLI application loop"""
    print("\n🚀 Welcome to E-commerce Price Tracker CLI!")
    
    while True:
        display_menu()
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            add_product_cli()
        elif choice == '2':
            list_products_cli()
        elif choice == '3':
            view_price_history_cli()
        elif choice == '4':
            remove_product_cli()
        elif choice == '5':
            print("\n👋 Thank you for using Price Tracker CLI. Goodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 5.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


# Simple add product mode (for quick access)
def quick_add_product():
    """Quick mode to just add a product without full menu"""
    print("\n🚀 E-commerce Price Tracker - Quick Add Product")
    add_product_cli()


if __name__ == "__main__":
    # Check if running in quick mode or full CLI mode
    if len(sys.argv) > 1 and sys.argv[1] == 'add':
        # Quick add mode: python cli_app.py add
        quick_add_product()
    else:
        # Full interactive CLI mode: python cli_app.py
        main()
