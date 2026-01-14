#!/usr/bin/env python3
"""
Cron Setup Helper for Price Tracker
Helps users set up cron jobs on macOS/Linux systems.
"""

import sys
import os
import subprocess
from pathlib import Path


def get_python_path():
    """Get the full path to the Python interpreter."""
    # Try to get the virtual environment Python first
    venv_python = Path(".venv/bin/python")
    if venv_python.exists():
        return venv_python.absolute()
    
    # Otherwise get the current Python
    result = subprocess.run(["which", "python3"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    
    result = subprocess.run(["which", "python"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    
    return sys.executable


def get_project_path():
    """Get the full path to the project directory."""
    return Path.cwd().absolute()


def generate_cron_line(interval_hours=6):
    """Generate a cron line for the specified interval."""
    python_path = get_python_path()
    project_path = get_project_path()
    
    # Escape spaces in path
    project_path_str = str(project_path).replace(" ", r"\ ")
    
    if interval_hours == 1:
        cron_time = "0 * * * *"  # Every hour
    elif interval_hours == 2:
        cron_time = "0 */2 * * *"  # Every 2 hours
    elif interval_hours == 3:
        cron_time = "0 */3 * * *"  # Every 3 hours
    elif interval_hours == 4:
        cron_time = "0 */4 * * *"  # Every 4 hours
    elif interval_hours == 6:
        cron_time = "0 */6 * * *"  # Every 6 hours
    elif interval_hours == 8:
        cron_time = "0 */8 * * *"  # Every 8 hours
    elif interval_hours == 12:
        cron_time = "0 */12 * * *"  # Every 12 hours
    elif interval_hours == 24:
        cron_time = "0 0 * * *"  # Daily at midnight
    else:
        cron_time = f"0 */{interval_hours} * * *"
    
    cron_line = f"{cron_time} cd {project_path_str} && {python_path} tracker.py check >> {project_path_str}/cron.log 2>&1"
    
    return cron_line


def check_cron_service():
    """Check if cron service is available."""
    try:
        # Try to run crontab -l
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def get_existing_crontab():
    """Get existing crontab entries."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        return ""
    except:
        return ""


def main():
    """Main function."""
    print("\n" + "=" * 80)
    print("📅 CRON SETUP HELPER FOR PRICE TRACKER")
    print("=" * 80)
    print()
    
    # Check if on Unix-like system
    if sys.platform == "win32":
        print("❌ This script is for macOS/Linux systems.")
        print("   For Windows, please use Task Scheduler.")
        print("   See SCHEDULING_GUIDE.md for instructions.")
        print()
        return 1
    
    # Check if cron is available
    print("Checking cron availability...")
    if not check_cron_service():
        print("❌ Cron service not found.")
        print("   Make sure cron is installed on your system.")
        print()
        return 1
    print("✅ Cron service is available")
    print()
    
    # Get paths
    python_path = get_python_path()
    project_path = get_project_path()
    
    print("Detected Configuration:")
    print(f"  Python: {python_path}")
    print(f"  Project: {project_path}")
    print()
    
    # Ask for interval
    print("How often should the price tracker run?")
    print("  1. Every 1 hour")
    print("  2. Every 2 hours")
    print("  3. Every 3 hours")
    print("  4. Every 4 hours")
    print("  5. Every 6 hours (recommended)")
    print("  6. Every 8 hours")
    print("  7. Every 12 hours")
    print("  8. Daily (24 hours)")
    print()
    
    try:
        choice = input("Enter your choice (1-8) [default: 5]: ").strip()
        if not choice:
            choice = "5"
        
        interval_map = {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 6,
            "6": 8,
            "7": 12,
            "8": 24
        }
        
        if choice not in interval_map:
            print("❌ Invalid choice. Using default (6 hours).")
            choice = "5"
        
        interval = interval_map[choice]
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        return 1
    
    # Generate cron line
    cron_line = generate_cron_line(interval)
    
    print()
    print("=" * 80)
    print("GENERATED CRON LINE:")
    print("=" * 80)
    print(cron_line)
    print("=" * 80)
    print()
    
    # Check existing crontab
    existing_crontab = get_existing_crontab()
    if "tracker.py" in existing_crontab:
        print("⚠️  Warning: Found existing price tracker cron job(s):")
        print()
        for line in existing_crontab.splitlines():
            if "tracker.py" in line:
                print(f"   {line}")
        print()
        print("You may want to remove old entries before adding the new one.")
        print()
    
    # Instructions
    print("NEXT STEPS:")
    print()
    print("Option 1: Manual Setup")
    print("-" * 80)
    print("1. Open crontab editor:")
    print("   crontab -e")
    print()
    print("2. Add the following line:")
    print(f"   {cron_line}")
    print()
    print("3. Save and exit:")
    print("   - In vi/vim: Press Esc, type :wq, press Enter")
    print("   - In nano: Press Ctrl+X, then Y, then Enter")
    print()
    
    print("Option 2: Automatic Setup")
    print("-" * 80)
    print("Run the following command to add the cron job automatically:")
    print()
    if existing_crontab:
        print(f'(crontab -l ; echo "{cron_line}") | crontab -')
    else:
        print(f'echo "{cron_line}" | crontab -')
    print()
    
    print("=" * 80)
    print("VERIFICATION:")
    print("=" * 80)
    print("After setup, verify the cron job:")
    print()
    print("1. List cron jobs:")
    print("   crontab -l")
    print()
    print("2. Test the command manually:")
    print(f"   cd {project_path}")
    print(f"   {python_path} tracker.py check")
    print()
    print("3. Monitor the log file:")
    print(f"   tail -f {project_path}/cron.log")
    print()
    print("4. Wait for scheduled execution and check:")
    print(f"   cat {project_path}/cron.log")
    print()
    
    print("=" * 80)
    print("ALTERNATIVE: Use Python Scheduler")
    print("=" * 80)
    print("Instead of cron, you can use the built-in Python scheduler:")
    print()
    print(f"   cd {project_path}")
    print(f"   {python_path} scheduler.py --interval {interval}")
    print()
    print("This runs in the foreground and provides real-time logging.")
    print("Use nohup, screen, or tmux to run it in the background.")
    print("See SCHEDULING_GUIDE.md for details.")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
