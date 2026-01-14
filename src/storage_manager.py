"""
Storage Manager Module for E-commerce Price Tracker
Handles all data storage and retrieval operations for product prices
Centralizes CSV, JSON, and price history management
"""

import csv
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Storage configuration
CSV_FILE = "products.csv"
JSON_CONFIG_FILE = "products.json"

# Define the product data schema for CSV
PRODUCT_SCHEMA = [
    "product_id",
    "product_name",
    "product_url",
    "current_price",
    "currency",
    "last_updated",
    "image_url"
]


class StorageManager:
    """
    Manages data persistence for product prices and configurations.
    Handles CSV storage for price history and JSON for product configurations.
    """
    
    def __init__(self, csv_file=CSV_FILE, json_file=JSON_CONFIG_FILE):
        """
        Initialize the storage manager.
        
        Args:
            csv_file (str): Path to CSV file for price data
            json_file (str): Path to JSON file for product configurations
        """
        self.csv_file = csv_file
        self.json_file = json_file
        self.csv_path = Path(csv_file)
        self.json_path = Path(json_file)
        logger.info(f"StorageManager initialized with CSV={csv_file}, JSON={json_file}")
    
    def initialize_csv_storage(self):
        """
        Initialize CSV storage if it doesn't exist.
        Creates a CSV file with headers based on the defined schema.
        
        Returns:
            bool: True if storage was created, False if it already existed
        """
        if self.csv_path.exists():
            logger.info(f"CSV storage already exists: {self.csv_file}")
            return False
        
        try:
            with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(PRODUCT_SCHEMA)
            
            logger.info(f"CSV storage initialized successfully: {self.csv_file}")
            logger.info(f"Schema: {', '.join(PRODUCT_SCHEMA)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize CSV storage: {type(e).__name__} - {str(e)}")
            raise
    
    def save_product_data(self, product_data):
        """
        Save product data to CSV file.
        
        Args:
            product_data (dict): Product data with keys: name, url, price, timestamp
        
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            # Ensure CSV file exists
            if not self.csv_path.exists():
                self.initialize_csv_storage()
            
            # Generate unique product ID based on URL
            product_id = hash(product_data['url']) % 1000000
            
            # Prepare row data
            row_data = [
                product_id,
                product_data['name'],
                product_data['url'],
                product_data['price'],
                '₹',  # Currency
                product_data['timestamp'],
                ''  # Image URL (placeholder)
            ]
            
            # Append data to CSV
            with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(row_data)
            
            logger.info(f"Product data saved: {product_data['name'][:50]}... | Price: ₹{product_data['price']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save product data: {type(e).__name__} - {str(e)}")
            return False
    
    def retrieve_all_products(self):
        """
        Retrieve all product entries from CSV.
        
        Returns:
            list: List of product dictionaries
        """
        if not self.csv_path.exists():
            logger.warning(f"CSV file does not exist: {self.csv_file}")
            return []
        
        try:
            products_list = []
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    products_list.append(row)
            
            logger.info(f"Retrieved {len(products_list)} product entries from CSV")
            return products_list
            
        except Exception as e:
            logger.error(f"Failed to retrieve products: {type(e).__name__} - {str(e)}")
            return []
    
    def get_price_history(self, product_url):
        """
        Get all historical prices for a specific product.
        
        Args:
            product_url (str): URL of the product
        
        Returns:
            list: List of dicts with 'timestamp' and 'price' keys
        """
        try:
            all_products = self.retrieve_all_products()
            
            # Filter entries for this product URL
            price_history = []
            for product_entry in all_products:
                if product_entry.get('product_url') == product_url:
                    price_history.append({
                        'timestamp': product_entry.get('last_updated'),
                        'price': product_entry.get('current_price')
                    })
            
            logger.info(f"Retrieved {len(price_history)} price entries for {product_url}")
            return price_history
            
        except Exception as e:
            logger.error(f"Failed to get price history: {type(e).__name__} - {str(e)}")
            return []
    
    def get_latest_price(self, product_url):
        """
        Get the most recent price for a product.
        
        Args:
            product_url (str): URL of the product
        
        Returns:
            dict: Latest price data with 'price' and 'timestamp' or None if not found
        """
        price_history = self.get_price_history(product_url)
        
        if not price_history:
            logger.info(f"No price history found for {product_url}")
            return None
        
        # Return the most recent entry (last in list)
        latest_price_data = price_history[-1]
        logger.info(f"Latest price for {product_url}: ₹{latest_price_data['price']} at {latest_price_data['timestamp']}")
        return latest_price_data
    
    def get_lowest_historical_price(self, product_url):
        """
        Get the lowest price from historical data.
        
        Args:
            product_url (str): URL of the product
        
        Returns:
            float: Lowest price or None if no history found
        """
        price_history = self.get_price_history(product_url)
        
        if not price_history:
            return None
        
        try:
            # Convert prices to float and find minimum
            prices_as_floats = []
            for entry in price_history:
                price_str = str(entry['price']).replace(',', '').replace('₹', '').strip()
                try:
                    price_float = float(price_str)
                    prices_as_floats.append(price_float)
                except ValueError:
                    logger.warning(f"Could not convert price to float: {entry['price']}")
                    continue
            
            if not prices_as_floats:
                return None
            
            lowest_price = min(prices_as_floats)
            logger.info(f"Lowest historical price for {product_url}: ₹{lowest_price}")
            return lowest_price
            
        except Exception as e:
            logger.error(f"Error calculating lowest price: {type(e).__name__} - {str(e)}")
            return None
    
    def load_product_config(self):
        """
        Load product configurations from JSON file.
        
        Returns:
            list: List of product configuration dictionaries
        """
        if not self.json_path.exists():
            logger.warning(f"JSON config file does not exist: {self.json_file}")
            return []
        
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                products_config = json.load(file)
            
            logger.info(f"Loaded {len(products_config)} products from JSON config")
            return products_config
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Failed to load product config: {type(e).__name__} - {str(e)}")
            return []
    
    def save_product_config(self, products_config):
        """
        Save product configurations to JSON file.
        
        Args:
            products_config (list): List of product configuration dictionaries
        
        Returns:
            bool: True if save successful, False otherwise
        """
        try:
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump(products_config, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(products_config)} products to JSON config")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save product config: {type(e).__name__} - {str(e)}")
            return False
    
    def display_price_history_table(self, product_url, max_entries=10):
        """
        Display price history in a formatted table.
        
        Args:
            product_url (str): URL of the product
            max_entries (int): Maximum number of entries to display
        """
        price_history = self.get_price_history(product_url)
        
        if not price_history:
            print(f"\n⚠️  No price history found for this product.")
            return
        
        print(f"\n{'='*80}")
        print(f"PRICE HISTORY")
        print(f"{'='*80}")
        print(f"URL: {product_url[:70]}...")
        print(f"Total Entries: {len(price_history)}")
        print(f"\n{'Timestamp':<25} {'Price':<15}")
        print(f"{'-'*40}")
        
        # Show most recent entries
        recent_entries = price_history[-max_entries:]
        for entry in recent_entries:
            timestamp = entry['timestamp']
            price = f"₹{entry['price']}"
            print(f"{timestamp:<25} {price:<15}")
        
        print(f"{'='*80}")


# Convenience functions for backward compatibility

def setup_storage():
    """Initialize CSV storage (backward compatible function)."""
    storage = StorageManager()
    return storage.initialize_csv_storage()


def save_product(product_data):
    """Save product data to CSV (backward compatible function)."""
    storage = StorageManager()
    return storage.save_product_data(product_data)


def get_historical_prices(product_url):
    """Get historical prices (backward compatible function)."""
    storage = StorageManager()
    return storage.get_price_history(product_url)


def display_price_history(product_url):
    """Display price history (backward compatible function)."""
    storage = StorageManager()
    storage.display_price_history_table(product_url)
