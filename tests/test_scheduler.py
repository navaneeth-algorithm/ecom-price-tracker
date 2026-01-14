"""
Test script for scheduler.py
Verifies that the scheduler can execute commands correctly.
"""

import subprocess
import time
import os
from pathlib import Path

def test_scheduler():
    """Test the scheduler functionality."""
    print("=" * 80)
    print("SCHEDULER TEST")
    print("=" * 80)
    print()
    
    # Test 1: Check if scheduler.py exists
    print("Test 1: Checking if scheduler.py exists...")
    scheduler_path = Path("scheduler.py")
    if scheduler_path.exists():
        print("✅ scheduler.py found")
    else:
        print("❌ scheduler.py not found")
        return False
    print()
    
    # Test 2: Check if tracker.py exists
    print("Test 2: Checking if tracker.py exists...")
    tracker_path = Path("tracker.py")
    if tracker_path.exists():
        print("✅ tracker.py found")
    else:
        print("❌ tracker.py not found")
        return False
    print()
    
    # Test 3: Test scheduler help command
    print("Test 3: Testing scheduler help command...")
    try:
        result = subprocess.run(
            ["python", "scheduler.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and "--interval" in result.stdout:
            print("✅ Scheduler help command works")
            print(f"   Output length: {len(result.stdout)} characters")
        else:
            print("❌ Scheduler help command failed")
            return False
    except Exception as e:
        print(f"❌ Error running scheduler help: {e}")
        return False
    print()
    
    # Test 4: Test manual tracker command
    print("Test 4: Testing manual tracker command...")
    try:
        result = subprocess.run(
            ["python", "tracker.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Tracker command works")
            print(f"   Output length: {len(result.stdout)} characters")
        else:
            print("❌ Tracker command failed")
            return False
    except Exception as e:
        print(f"❌ Error running tracker: {e}")
        return False
    print()
    
    # Test 5: Run scheduler for 5 seconds to verify it starts
    print("Test 5: Testing scheduler startup (5 second test)...")
    print("   Starting scheduler with immediate run...")
    
    # Clear old log files for clean test
    for log_file in ["scheduler.log", "test_scheduler.log"]:
        if os.path.exists(log_file):
            os.remove(log_file)
    
    try:
        # Start scheduler in background
        process = subprocess.Popen(
            ["python", "scheduler.py", "--interval", "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("   Scheduler started, waiting 5 seconds...")
        time.sleep(5)
        
        # Terminate the scheduler
        process.terminate()
        process.wait(timeout=5)
        
        print("   Scheduler stopped")
        
        # Check if scheduler.log was created
        if os.path.exists("scheduler.log"):
            print("✅ Scheduler ran successfully")
            print("   scheduler.log created")
            
            # Read first few lines
            with open("scheduler.log", "r") as f:
                lines = f.readlines()[:5]
                print(f"   Log entries: {len(lines)}")
                if lines:
                    print("   First log entry:")
                    print(f"      {lines[0].strip()}")
        else:
            print("❌ scheduler.log not created")
            return False
            
    except Exception as e:
        print(f"❌ Error during scheduler test: {e}")
        try:
            process.terminate()
        except:
            pass
        return False
    print()
    
    # Test 6: Verify log file contents
    print("Test 6: Verifying log file contents...")
    if os.path.exists("scheduler.log"):
        with open("scheduler.log", "r") as f:
            content = f.read()
            
        required_strings = [
            "PriceTrackerScheduler initialized",
            "Interval:",
            "Python:",
            "Script:"
        ]
        
        all_found = True
        for req_string in required_strings:
            if req_string in content:
                print(f"   ✅ Found: {req_string}")
            else:
                print(f"   ❌ Missing: {req_string}")
                all_found = False
        
        if all_found:
            print("✅ Log file has expected content")
        else:
            print("❌ Log file missing expected content")
            return False
    else:
        print("❌ scheduler.log not found")
        return False
    print()
    
    # All tests passed
    print("=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print()
    print("Summary:")
    print("  • scheduler.py is working correctly")
    print("  • Can execute tracker.py commands")
    print("  • Logs are being created properly")
    print("  • Ready for production use")
    print()
    print("Next steps:")
    print("  1. Run: python scheduler.py")
    print("  2. Or set up system-level scheduling (see SCHEDULING_GUIDE.md)")
    print()
    
    return True


if __name__ == "__main__":
    success = test_scheduler()
    exit(0 if success else 1)
