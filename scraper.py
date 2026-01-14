"""
Scraper Module for E-commerce Price Tracker
Handles all web scraping logic using Playwright
"""

import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from datetime import datetime

# Initialize logger for this module
logger = logging.getLogger(__name__)


class ProductScraper:
    """
    Web scraper for e-commerce product data.
    Uses Playwright to extract product names, prices, and other information.
    """
    
    # CSS selectors for Amazon product pages
    SELECTORS = {
        'product_title': '#productTitle',
        'product_price': '.a-price-whole',
        'product_image': '#landingImage'
    }
    
    # Timeout settings (in milliseconds)
    PAGE_LOAD_TIMEOUT = 30000
    ELEMENT_WAIT_TIMEOUT = 30000
    
    def __init__(self, headless=True):
        """
        Initialize the scraper.
        
        Args:
            headless (bool): Whether to run browser in headless mode
        """
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        logger.info(f"ProductScraper initialized (headless={headless})")
    
    def launch_browser(self):
        """
        Launch Playwright browser and create a new page.
        
        Returns:
            tuple: (playwright_instance, browser, context, page) or (None, None, None, None) if failed
        """
        try:
            playwright_instance = sync_playwright().start()
            logger.info("Playwright instance started")
            
            self.browser = playwright_instance.chromium.launch(headless=self.headless)
            logger.info("Browser launched successfully")
            
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            logger.info("Browser context and page created successfully")
            
            return playwright_instance, self.browser, self.context, self.page
            
        except PlaywrightError as e:
            error_msg = f"Failed to launch browser: {str(e)}"
            logger.error(error_msg)
            return None, None, None, None
        except Exception as e:
            error_msg = f"Unexpected error launching browser: {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            return None, None, None, None
    
    def navigate_to_product_page(self, page, product_url):
        """
        Navigate to a product URL with error handling.
        
        Args:
            page: Playwright page object
            product_url (str): URL of the product page
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            logger.info(f"Navigating to URL: {product_url}")
            page.goto(product_url, wait_until='domcontentloaded', timeout=self.PAGE_LOAD_TIMEOUT)
            logger.info(f"Successfully navigated to {product_url}")
            return True
            
        except PlaywrightTimeoutError:
            error_msg = f"Timeout: Page failed to load within {self.PAGE_LOAD_TIMEOUT/1000}s for URL: {product_url}"
            logger.error(error_msg)
            return False
        except PlaywrightError as e:
            error_msg = f"Playwright error during navigation to {product_url}: {str(e)}"
            logger.error(error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected navigation error for {product_url}: {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            return False
    
    def extract_product_title(self, page, product_url):
        """
        Extract product title from the page.
        
        Args:
            page: Playwright page object
            product_url (str): URL for error logging
        
        Returns:
            str: Product title or None if extraction failed
        """
        try:
            logger.info(f"Waiting for product title element")
            page.wait_for_selector(self.SELECTORS['product_title'], timeout=self.ELEMENT_WAIT_TIMEOUT)
            
            product_title_element = page.query_selector(self.SELECTORS['product_title'])
            if not product_title_element:
                raise ValueError("Product title element not found")
            
            product_title = product_title_element.inner_text().strip()
            logger.info(f"Successfully extracted product title: {product_title[:50]}...")
            return product_title
            
        except PlaywrightTimeoutError:
            error_msg = f"Timeout: Product title element '{self.SELECTORS['product_title']}' not found within {self.ELEMENT_WAIT_TIMEOUT/1000}s"
            logger.error(error_msg)
            return None
        except ValueError as e:
            error_msg = f"Element not found: {str(e)}"
            logger.error(error_msg)
            return None
        except Exception as e:
            error_msg = f"Error extracting product title: {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            return None
    
    def extract_product_price(self, page, product_url):
        """
        Extract product price from the page.
        
        Args:
            page: Playwright page object
            product_url (str): URL for error logging
        
        Returns:
            str: Product price (cleaned) or None if extraction failed
        """
        try:
            logger.info(f"Waiting for price element")
            page.wait_for_selector(self.SELECTORS['product_price'], timeout=self.ELEMENT_WAIT_TIMEOUT)
            
            product_price_element = page.query_selector(self.SELECTORS['product_price'])
            if not product_price_element:
                raise ValueError("Price element not found")
            
            product_price_raw = product_price_element.inner_text().strip()
            if not product_price_raw or product_price_raw == "":
                raise ValueError("Price text is empty")
            
            # Clean up price formatting (remove newlines and trailing periods)
            product_price_cleaned = product_price_raw.replace('\n', '').replace('.', '').strip()
            
            logger.info(f"Successfully extracted price: ₹{product_price_cleaned}")
            return product_price_cleaned
            
        except PlaywrightTimeoutError:
            error_msg = f"Timeout: Price element '{self.SELECTORS['product_price']}' not found within {self.ELEMENT_WAIT_TIMEOUT/1000}s"
            logger.error(error_msg)
            return None
        except ValueError as e:
            error_msg = f"Price extraction error: {str(e)}"
            logger.error(error_msg)
            return None
        except Exception as e:
            error_msg = f"Error extracting price: {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            return None
    
    def scrape_product(self, page, product_config):
        """
        Scrape all data from a single product page.
        
        Args:
            page: Playwright page object
            product_config (dict): Product configuration with 'url' and 'name'
        
        Returns:
            dict: Scraped product data with keys: name, url, price, timestamp
                  or None if scraping failed
        """
        product_url = product_config['url']
        product_name_from_config = product_config.get('name', 'Unknown Product')
        
        logger.info(f"Starting scrape for product: {product_name_from_config} | URL: {product_url}")
        
        # Step 1: Navigate to the product page
        navigation_success = self.navigate_to_product_page(page, product_url)
        if not navigation_success:
            return None
        
        # Step 2: Extract product title
        product_title = self.extract_product_title(page, product_url)
        if not product_title:
            return None
        
        # Step 3: Extract product price
        product_price = self.extract_product_price(page, product_url)
        if not product_price:
            return None
        
        # Step 4: Generate timestamp and compile results
        try:
            scrape_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            scraped_data = {
                'name': product_title,
                'url': product_url,
                'price': product_price,
                'timestamp': scrape_timestamp
            }
            
            logger.info(f"Successfully scraped product: {product_title[:50]}... | Price: ₹{product_price} | Timestamp: {scrape_timestamp}")
            return scraped_data
            
        except Exception as e:
            error_msg = f"Error compiling scraped data: {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            return None
    
    def close_browser(self):
        """
        Close browser and clean up resources.
        """
        try:
            if self.browser:
                self.browser.close()
                logger.info("Browser closed successfully")
        except Exception as e:
            logger.warning(f"Error closing browser: {type(e).__name__} - {str(e)}")


def scrape_product_simple(page, product_config):
    """
    Simple function to scrape a product without class instantiation.
    Useful for backward compatibility.
    
    Args:
        page: Playwright page object
        product_config (dict): Product configuration with 'url' and 'name'
    
    Returns:
        dict: Scraped product data or None if failed
    """
    scraper = ProductScraper()
    return scraper.scrape_product(page, product_config)
