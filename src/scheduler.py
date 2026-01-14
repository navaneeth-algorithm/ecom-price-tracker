"""
Automated Scheduler for E-commerce Price Tracker
Runs the price checking command at regular intervals using the schedule library
"""

import schedule
import time
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configure logging for scheduler
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PriceTrackerScheduler:
    """
    Scheduler for automated price tracking runs.
    Executes the tracker check command at configured intervals.
    """
    
    def __init__(self, interval_hours=6, script_path='tracker.py'):
        """
        Initialize the scheduler.
        
        Args:
            interval_hours (int): Hours between each check (default: 6)
            script_path (str): Path to the tracker script
        """
        self.interval_hours = interval_hours
        self.script_path = Path(script_path)
        self.python_executable = sys.executable
        self.run_count = 0
        self.last_run_time = None
        self.last_run_success = None
        
        logger.info(f"PriceTrackerScheduler initialized")
        logger.info(f"  Interval: Every {interval_hours} hours")
        logger.info(f"  Python: {self.python_executable}")
        logger.info(f"  Script: {self.script_path.absolute()}")
    
    def run_price_check(self):
        """
        Execute the price checking command.
        Runs 'python tracker.py check' and logs the result.
        """
        self.run_count += 1
        run_start_time = datetime.now()
        
        logger.info(f"=" * 80)
        logger.info(f"Starting scheduled price check #{self.run_count}")
        logger.info(f"Time: {run_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"=" * 80)
        
        try:
            # Run the tracker check command
            command = [self.python_executable, str(self.script_path), 'check']
            logger.info(f"Executing command: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            
            run_end_time = datetime.now()
            duration = (run_end_time - run_start_time).total_seconds()
            
            # Log execution results
            if result.returncode == 0:
                logger.info(f"✅ Price check completed successfully")
                logger.info(f"   Duration: {duration:.2f} seconds")
                logger.info(f"   Output lines: {len(result.stdout.splitlines())}")
                self.last_run_success = True
            else:
                logger.error(f"❌ Price check failed with return code {result.returncode}")
                logger.error(f"   Duration: {duration:.2f} seconds")
                logger.error(f"   Error output: {result.stderr[:500]}")
                self.last_run_success = False
            
            # Log sample output
            if result.stdout:
                output_lines = result.stdout.splitlines()
                logger.info(f"   First 5 lines of output:")
                for line in output_lines[:5]:
                    logger.info(f"     {line}")
            
            self.last_run_time = run_end_time
            
            logger.info(f"=" * 80)
            logger.info(f"Scheduled check #{self.run_count} completed")
            logger.info(f"Next run in {self.interval_hours} hours")
            logger.info(f"=" * 80)
            
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Price check timed out after 10 minutes")
            self.last_run_success = False
            
        except FileNotFoundError:
            logger.error(f"❌ Script not found: {self.script_path}")
            logger.error(f"   Make sure tracker.py exists in the correct location")
            self.last_run_success = False
            
        except Exception as e:
            logger.error(f"❌ Unexpected error during price check: {type(e).__name__}")
            logger.error(f"   Error details: {str(e)}")
            self.last_run_success = False
    
    def get_status(self):
        """
        Get current scheduler status.
        
        Returns:
            dict: Status information
        """
        status = {
            'total_runs': self.run_count,
            'last_run_time': self.last_run_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_run_time else 'Not yet run',
            'last_run_success': self.last_run_success if self.last_run_success is not None else 'Not yet run',
            'interval_hours': self.interval_hours,
            'next_run': self._calculate_next_run()
        }
        return status
    
    def _calculate_next_run(self):
        """Calculate time until next run."""
        if self.last_run_time:
            from datetime import timedelta
            next_run = self.last_run_time + timedelta(hours=self.interval_hours)
            time_until = next_run - datetime.now()
            
            if time_until.total_seconds() > 0:
                hours = int(time_until.total_seconds() // 3600)
                minutes = int((time_until.total_seconds() % 3600) // 60)
                return f"In {hours}h {minutes}m"
            else:
                return "Soon"
        return f"In {self.interval_hours} hours"
    
    def start(self, run_immediately=True):
        """
        Start the scheduler.
        
        Args:
            run_immediately (bool): Whether to run check immediately on start
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"🚀 PRICE TRACKER SCHEDULER STARTING")
        logger.info(f"{'='*80}")
        logger.info(f"Schedule: Every {self.interval_hours} hours")
        logger.info(f"Immediate run: {'Yes' if run_immediately else 'No'}")
        logger.info(f"Press Ctrl+C to stop")
        logger.info(f"{'='*80}\n")
        
        # Schedule the job
        schedule.every(self.interval_hours).hours.do(self.run_price_check)
        
        # Run immediately if requested
        if run_immediately:
            logger.info("Running initial price check...")
            self.run_price_check()
        
        # Keep the scheduler running
        logger.info(f"\n📊 Scheduler is now running...")
        logger.info(f"Logs are being written to: scheduler.log")
        logger.info(f"App logs are being written to: app.log\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info(f"\n\n{'='*80}")
            logger.info(f"🛑 SCHEDULER STOPPED BY USER")
            logger.info(f"{'='*80}")
            
            # Print final statistics
            status = self.get_status()
            logger.info(f"\n📊 Final Statistics:")
            logger.info(f"   Total runs: {status['total_runs']}")
            logger.info(f"   Last run: {status['last_run_time']}")
            logger.info(f"   Last status: {status['last_run_success']}")
            logger.info(f"\n{'='*80}\n")


def main():
    """
    Main function to start the scheduler.
    Supports command-line arguments for configuration.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automated scheduler for E-commerce Price Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scheduler.py                    # Run every 6 hours (default)
  python scheduler.py --interval 3       # Run every 3 hours
  python scheduler.py --no-immediate     # Don't run immediately on start
  python scheduler.py --interval 12      # Run every 12 hours
        """
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=6,
        help='Hours between each price check (default: 6)'
    )
    
    parser.add_argument(
        '--no-immediate',
        action='store_true',
        help='Do not run price check immediately on start'
    )
    
    parser.add_argument(
        '--script',
        type=str,
        default='tracker.py',
        help='Path to tracker script (default: tracker.py)'
    )
    
    args = parser.parse_args()
    
    # Validate interval
    if args.interval < 1:
        logger.error("Error: Interval must be at least 1 hour")
        sys.exit(1)
    
    if args.interval > 24:
        logger.warning(f"Warning: Interval is {args.interval} hours (more than 24 hours)")
    
    # Create and start scheduler
    scheduler = PriceTrackerScheduler(
        interval_hours=args.interval,
        script_path=args.script
    )
    
    scheduler.start(run_immediately=not args.no_immediate)


if __name__ == "__main__":
    main()
