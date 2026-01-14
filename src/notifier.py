"""
Notifier Module for E-commerce Price Tracker
Handles all notification and alert logic for price drops
Formats messages and manages notification delivery
"""

import logging
from datetime import datetime

# Initialize logger for this module
logger = logging.getLogger(__name__)


class PriceDropNotifier:
    """
    Handles price drop detection and notification formatting.
    Manages alert generation for price changes.
    """
    
    def __init__(self, price_drop_threshold=0):
        """
        Initialize the notifier.
        
        Args:
            price_drop_threshold (float): Minimum price drop amount to trigger alert (default: any drop)
        """
        self.price_drop_threshold = price_drop_threshold
        logger.info(f"PriceDropNotifier initialized with threshold=₹{price_drop_threshold}")
    
    def detect_price_drop(self, current_price, historical_prices, threshold=None):
        """
        Detect if current price represents a drop compared to historical prices.
        
        Args:
            current_price (float): Current price of the product
            historical_prices (list): List of previous prices
            threshold (float): Optional override for price drop threshold
        
        Returns:
            bool: True if price drop detected, False otherwise
        """
        # Use provided threshold or instance default
        check_threshold = threshold if threshold is not None else self.price_drop_threshold
        
        if not historical_prices or len(historical_prices) == 0:
            logger.info("No historical prices available for comparison")
            return False
        
        try:
            # Find the lowest historical price
            lowest_historical_price = min(historical_prices)
            
            # Calculate price difference
            price_difference = lowest_historical_price - current_price
            
            logger.info(f"Price comparison: Current=₹{current_price:.2f}, Lowest=₹{lowest_historical_price:.2f}, Diff=₹{price_difference:.2f}")
            
            # Check if price dropped by more than threshold
            is_drop = price_difference >= check_threshold
            
            if is_drop:
                logger.info(f"✅ Price drop detected! Current price is ₹{price_difference:.2f} lower than previous lowest")
            else:
                logger.info(f"❌ No significant price drop (difference: ₹{price_difference:.2f}, threshold: ₹{check_threshold})")
            
            return is_drop
            
        except Exception as e:
            logger.error(f"Error detecting price drop: {type(e).__name__} - {str(e)}")
            return False
    
    def calculate_savings(self, current_price, previous_price):
        """
        Calculate savings amount and percentage.
        
        Args:
            current_price (float): Current price
            previous_price (float): Previous/comparison price
        
        Returns:
            dict: Dictionary with 'amount' and 'percentage' keys
        """
        try:
            savings_amount = previous_price - current_price
            savings_percentage = (savings_amount / previous_price) * 100 if previous_price > 0 else 0
            
            return {
                'amount': savings_amount,
                'percentage': savings_percentage
            }
        except Exception as e:
            logger.error(f"Error calculating savings: {type(e).__name__} - {str(e)}")
            return {'amount': 0, 'percentage': 0}
    
    def format_console_alert(self, product_name, current_price, previous_price, product_url):
        """
        Format a price drop alert for console display.
        
        Args:
            product_name (str): Name of the product
            current_price (float): Current price
            previous_price (float): Previous lowest price
            product_url (str): Product URL
        
        Returns:
            str: Formatted alert message
        """
        savings = self.calculate_savings(current_price, previous_price)
        
        alert_lines = [
            "\n" + "🎉" * 40,
            "🚨 PRICE DROP ALERT! 🚨",
            "🎉" * 40,
            "",
            f"📦 Product: {product_name[:80]}...",
            f"💰 New Price: ₹{current_price:,.2f}",
            f"📉 Previous Lowest: ₹{previous_price:,.2f}",
            f"💵 You Save: ₹{savings['amount']:,.2f} ({savings['percentage']:.2f}% OFF)",
            f"🔗 URL: {product_url[:60]}...",
            "",
            "🎉" * 40
        ]
        
        alert_message = "\n".join(alert_lines)
        logger.info(f"🚨 Price drop alert generated for: {product_name[:50]}")
        return alert_message
    
    def display_alert(self, product_name, current_price, previous_price, product_url):
        """
        Display price drop alert to console.
        
        Args:
            product_name (str): Name of the product
            current_price (float): Current price
            previous_price (float): Previous lowest price
            product_url (str): Product URL
        """
        alert_message = self.format_console_alert(product_name, current_price, previous_price, product_url)
        print(alert_message)
        logger.info(f"Alert displayed for product: {product_name[:50]}")
    
    def format_summary_message(self, price_drops_list):
        """
        Format a summary of all price drops.
        
        Args:
            price_drops_list (list): List of price drop dictionaries
        
        Returns:
            str: Formatted summary message
        """
        if not price_drops_list or len(price_drops_list) == 0:
            return "\n📊 No price drops detected in this check."
        
        summary_lines = [
            "\n" + "🎉" * 40,
            f"🚨 FOUND {len(price_drops_list)} PRICE DROP(S)!",
            "🎉" * 40
        ]
        
        for drop in price_drops_list:
            savings = self.calculate_savings(drop['current_price'], drop['previous_price'])
            summary_lines.extend([
                "",
                f"📦 {drop['name'][:60]}...",
                f"   💰 New: ₹{drop['current_price']:,.2f} | Previous: ₹{drop['previous_price']:,.2f}",
                f"   💵 Save: ₹{savings['amount']:,.2f} ({savings['percentage']:.2f}% OFF)"
            ])
        
        summary_lines.extend([
            "",
            "🎉" * 40
        ])
        
        summary_message = "\n".join(summary_lines)
        logger.info(f"Summary generated for {len(price_drops_list)} price drop(s)")
        return summary_message
    
    def display_summary(self, price_drops_list):
        """
        Display summary of all price drops.
        
        Args:
            price_drops_list (list): List of price drop dictionaries
        """
        summary_message = self.format_summary_message(price_drops_list)
        print(summary_message)
        logger.info(f"Summary displayed for {len(price_drops_list)} price drop(s)")
    
    def send_email_alert(self, recipient_email, product_name, current_price, previous_price, product_url):
        """
        Send email notification for price drop.
        (Placeholder for future email integration)
        
        Args:
            recipient_email (str): Email address to send alert to
            product_name (str): Name of the product
            current_price (float): Current price
            previous_price (float): Previous price
            product_url (str): Product URL
        
        Returns:
            bool: True if email sent successfully (currently returns False as not implemented)
        """
        logger.info(f"Email alert requested for {recipient_email} (not yet implemented)")
        # TODO: Implement email sending functionality
        # - Use smtplib or third-party service (SendGrid, Mailgun)
        # - Format HTML email with product details
        # - Handle email authentication and errors
        return False
    
    def send_sms_alert(self, phone_number, product_name, current_price, previous_price):
        """
        Send SMS notification for price drop.
        (Placeholder for future SMS integration)
        
        Args:
            phone_number (str): Phone number to send SMS to
            product_name (str): Name of the product
            current_price (float): Current price
            previous_price (float): Previous price
        
        Returns:
            bool: True if SMS sent successfully (currently returns False as not implemented)
        """
        logger.info(f"SMS alert requested for {phone_number} (not yet implemented)")
        # TODO: Implement SMS sending functionality
        # - Use Twilio, AWS SNS, or similar service
        # - Format concise SMS message
        # - Handle SMS authentication and errors
        return False


# Convenience functions for backward compatibility

def detect_price_drop(product_id, current_price, historical_prices_list, price_drop_threshold=0):
    """
    Detect price drop (backward compatible function).
    
    Args:
        product_id: Product identifier (not used, for compatibility)
        current_price (float): Current price
        historical_prices_list (list): List of historical prices
        price_drop_threshold (float): Minimum price drop to detect
    
    Returns:
        bool: True if price drop detected
    """
    notifier = PriceDropNotifier(price_drop_threshold)
    return notifier.detect_price_drop(current_price, historical_prices_list)


def display_price_drop_alert(product_name, current_price, previous_price, product_url):
    """
    Display price drop alert (backward compatible function).
    
    Args:
        product_name (str): Name of the product
        current_price (float): Current price
        previous_price (float): Previous price
        product_url (str): Product URL
    """
    notifier = PriceDropNotifier()
    notifier.display_alert(product_name, current_price, previous_price, product_url)


def format_notification_message(product_name, current_price, previous_price, savings_amount, savings_percent):
    """
    Format notification message (backward compatible function).
    
    Args:
        product_name (str): Name of the product
        current_price (float): Current price
        previous_price (float): Previous price
        savings_amount (float): Amount saved
        savings_percent (float): Percentage saved
    
    Returns:
        str: Formatted message
    """
    message_lines = [
        f"🚨 PRICE DROP ALERT!",
        f"Product: {product_name}",
        f"New Price: ₹{current_price:,.2f}",
        f"Previous Price: ₹{previous_price:,.2f}",
        f"You Save: ₹{savings_amount:,.2f} ({savings_percent:.2f}% OFF)"
    ]
    return "\n".join(message_lines)
