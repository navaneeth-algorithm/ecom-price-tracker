# 📅 Price Tracker Scheduling Guide

Complete guide for setting up automated price tracking runs.

## Table of Contents
- [Option 1: Python Scheduler (Recommended)](#option-1-python-scheduler-recommended)
- [Option 2: System-Level Scheduling](#option-2-system-level-scheduling)
  - [macOS/Linux (Cron)](#macoslinux-cron)
  - [Windows (Task Scheduler)](#windows-task-scheduler)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Option 1: Python Scheduler (Recommended) ⭐

The easiest way to schedule automated runs is using the included `scheduler.py` script.

### Installation

1. **Install the schedule library:**
   ```bash
   pip install schedule
   ```

2. **Verify installation:**
   ```bash
   python scheduler.py --help
   ```

### Basic Usage

**Run every 6 hours (default):**
```bash
python scheduler.py
```

**Run every 3 hours:**
```bash
python scheduler.py --interval 3
```

**Run every 12 hours without immediate execution:**
```bash
python scheduler.py --interval 12 --no-immediate
```

### Running in Background

**macOS/Linux (using nohup):**
```bash
nohup python scheduler.py > scheduler_output.log 2>&1 &
```

**macOS/Linux (using screen):**
```bash
screen -dmS price-tracker python scheduler.py
# To reattach: screen -r price-tracker
```

**macOS/Linux (using tmux):**
```bash
tmux new -d -s price-tracker 'python scheduler.py'
# To reattach: tmux attach -t price-tracker
```

### Logs and Monitoring

The scheduler creates two log files:
- **`scheduler.log`** - Scheduler activity and execution status
- **`app.log`** - Detailed application logs from tracker runs

**Monitor logs in real-time:**
```bash
# Watch scheduler logs
tail -f scheduler.log

# Watch application logs
tail -f app.log
```

### Stopping the Scheduler

**If running in foreground:**
- Press `Ctrl+C`

**If running in background:**
```bash
# Find the process ID
ps aux | grep scheduler.py

# Kill the process
kill <PID>
```

---

## Option 2: System-Level Scheduling

### macOS/Linux (Cron)

Cron is a time-based job scheduler in Unix-like operating systems.

#### Setup Steps

1. **Get the full paths:**
   ```bash
   # Python interpreter path
   which python3
   # Output example: /usr/local/bin/python3
   
   # Project directory path
   pwd
   # Output example: /Users/username/Desktop/programming/React Projects/ecom-price-tracker
   ```

2. **Open crontab editor:**
   ```bash
   crontab -e
   ```

3. **Add cron job (every 6 hours):**
   ```cron
   0 */6 * * * cd /Users/username/Desktop/programming/React\ Projects/ecom-price-tracker && /usr/local/bin/python3 tracker.py check >> cron.log 2>&1
   ```

4. **Alternative schedules:**
   ```cron
   # Every 3 hours
   0 */3 * * * cd /path/to/project && /usr/local/bin/python3 tracker.py check >> cron.log 2>&1
   
   # Every 12 hours (midnight and noon)
   0 0,12 * * * cd /path/to/project && /usr/local/bin/python3 tracker.py check >> cron.log 2>&1
   
   # Daily at 9 AM
   0 9 * * * cd /path/to/project && /usr/local/bin/python3 tracker.py check >> cron.log 2>&1
   
   # Twice daily (9 AM and 9 PM)
   0 9,21 * * * cd /path/to/project && /usr/local/bin/python3 tracker.py check >> cron.log 2>&1
   ```

5. **Save and exit:**
   - In `vi`/`vim`: Press `Esc`, then type `:wq` and press `Enter`
   - In `nano`: Press `Ctrl+X`, then `Y`, then `Enter`

#### Cron Syntax Explained

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
│ │ │ │ │
* * * * * command to execute
```

**Examples:**
- `0 */6 * * *` - Every 6 hours at minute 0
- `0 0,6,12,18 * * *` - At 12am, 6am, 12pm, 6pm
- `*/30 * * * *` - Every 30 minutes

#### Managing Cron Jobs

**List all cron jobs:**
```bash
crontab -l
```

**Remove all cron jobs:**
```bash
crontab -r
```

**Edit cron jobs:**
```bash
crontab -e
```

#### Verification

**Check if cron service is running:**
```bash
# macOS
sudo launchctl list | grep cron

# Linux
systemctl status cron
```

**View cron execution logs:**
```bash
# macOS
log show --predicate 'process == "cron"' --last 1d

# Linux
grep CRON /var/log/syslog
```

**Check your cron.log file:**
```bash
tail -f cron.log
```

---

### Windows (Task Scheduler)

Task Scheduler is Windows' built-in task automation tool.

#### Setup Steps (GUI Method)

1. **Open Task Scheduler:**
   - Press `Win+R`, type `taskschd.msc`, press `Enter`

2. **Create Basic Task:**
   - Click "Create Basic Task..." in the right panel
   - Name: `Price Tracker - Every 6 Hours`
   - Description: `Automated price tracking for e-commerce products`
   - Click "Next"

3. **Set Trigger:**
   - Select "Daily"
   - Click "Next"
   - Set start time (e.g., 12:00 AM)
   - Recur every: 1 days
   - Click "Next"

4. **Set Action:**
   - Select "Start a program"
   - Click "Next"
   - Program/script: `C:\Python311\python.exe` (your Python path)
   - Add arguments: `tracker.py check`
   - Start in: `C:\Users\YourName\Desktop\programming\React Projects\ecom-price-tracker`
   - Click "Next"

5. **Configure Advanced Settings:**
   - Check "Open the Properties dialog for this task when I click Finish"
   - Click "Finish"
   - In Properties dialog:
     - Go to "Triggers" tab
     - Double-click the trigger
     - Check "Repeat task every:" and select "6 hours"
     - Set duration to: "Indefinitely"
     - Click "OK"

6. **Configure Additional Options:**
   - In Properties dialog, "Settings" tab:
     - Check "Allow task to be run on demand"
     - Check "Run task as soon as possible after a scheduled start is missed"
     - Check "If the task fails, restart every: 10 minutes"
     - Click "OK"

#### Setup Steps (PowerShell Method)

```powershell
# Define variables
$TaskName = "PriceTrackerEvery6Hours"
$PythonPath = "C:\Python311\python.exe"
$ScriptPath = "C:\Users\YourName\Desktop\programming\React Projects\ecom-price-tracker\tracker.py"
$WorkingDir = "C:\Users\YourName\Desktop\programming\React Projects\ecom-price-tracker"

# Create action
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "tracker.py check" -WorkingDirectory $WorkingDir

# Create trigger (repeat every 6 hours)
$Trigger = New-ScheduledTaskTrigger -Daily -At 12:00AM
$Trigger.Repetition = $(New-ScheduledTaskTrigger -Once -At 12:00AM -RepetitionInterval (New-TimeSpan -Hours 6) -RepetitionDuration ([TimeSpan]::MaxValue)).Repetition

# Create settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Register task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Description "E-commerce Price Tracker - Runs every 6 hours"

# Enable task
Enable-ScheduledTask -TaskName $TaskName
```

#### Managing Tasks

**Run task immediately:**
```powershell
Start-ScheduledTask -TaskName "PriceTrackerEvery6Hours"
```

**Check task status:**
```powershell
Get-ScheduledTask -TaskName "PriceTrackerEvery6Hours" | Get-ScheduledTaskInfo
```

**View task history:**
- In Task Scheduler GUI
- Select the task
- Click "History" tab (enable if disabled)

**Delete task:**
```powershell
Unregister-ScheduledTask -TaskName "PriceTrackerEvery6Hours" -Confirm:$false
```

---

## Verification

### Immediate Test

**Python Scheduler:**
```bash
# Run with immediate execution (default)
python scheduler.py --interval 6
```

**Cron (macOS/Linux):**
```bash
# Manually trigger the command
cd /path/to/project && python3 tracker.py check
```

**Task Scheduler (Windows):**
- Right-click the task in Task Scheduler
- Select "Run"

### Check for Updates

**View latest log entries:**
```bash
# Last 20 lines of app.log
tail -n 20 app.log

# Last 20 lines of scheduler.log (if using Python scheduler)
tail -n 20 scheduler.log

# Last 20 lines of cron.log (if using cron)
tail -n 20 cron.log
```

**Check for new product data:**
```bash
# View products.csv
cat products.csv

# Check last modified time
ls -la products.csv
```

**Monitor in real-time:**
```bash
# Watch app.log
tail -f app.log

# Watch scheduler.log
tail -f scheduler.log
```

### Verify Scheduled Execution

**After 6 hours, check:**

1. **Log files updated:**
   ```bash
   ls -lt *.log
   ```

2. **New price entries in CSV:**
   ```bash
   tail products.csv
   ```

3. **Log entries show successful runs:**
   ```bash
   grep "completed successfully" app.log
   ```

4. **Check for price drop alerts:**
   ```bash
   grep "PRICE DROP" app.log
   ```

---

## Troubleshooting

### Common Issues

#### 1. Python Not Found

**Error:** `command not found: python3`

**Solution:**
```bash
# Find Python path
which python3
# or
which python

# Use full path in cron/task
/usr/local/bin/python3 tracker.py check
```

#### 2. Script Not Found

**Error:** `No such file or directory: tracker.py`

**Solution:**
- Always use absolute paths
- Include `cd /path/to/project &&` before command
- For Task Scheduler, set "Start in" directory

#### 3. Virtual Environment Not Activated

**Error:** `ModuleNotFoundError: No module named 'playwright'`

**Solution (Cron/Task Scheduler):**
```bash
# Use virtual environment's Python directly
/path/to/project/.venv/bin/python tracker.py check
```

**Solution (Python Scheduler):**
```bash
# Activate venv first
source .venv/bin/activate
python scheduler.py
```

#### 4. Permission Denied

**Error:** `Permission denied`

**Solution:**
```bash
# Make scripts executable
chmod +x tracker.py
chmod +x scheduler.py

# Check file permissions
ls -la tracker.py
```

#### 5. Cron Not Running

**Solution:**
```bash
# Start cron service (Linux)
sudo systemctl start cron
sudo systemctl enable cron

# Check cron status
systemctl status cron
```

#### 6. No Output in Logs

**Problem:** Log files are empty

**Solution:**
1. Verify command runs manually:
   ```bash
   cd /path/to/project && python3 tracker.py check
   ```

2. Check cron job syntax:
   ```bash
   crontab -l
   ```

3. Verify log file path is writable:
   ```bash
   touch cron.log
   ls -la cron.log
   ```

4. Check stderr output:
   ```bash
   # Redirect both stdout and stderr
   command >> output.log 2>&1
   ```

#### 7. Task Scheduler Task Not Running

**Solution:**
1. Check task history for errors
2. Verify Python path is correct
3. Test command in Command Prompt:
   ```cmd
   cd C:\path\to\project
   C:\Python311\python.exe tracker.py check
   ```
4. Run Task Scheduler as Administrator
5. Ensure "Run whether user is logged on or not" is configured correctly

---

## Best Practices

### 1. Use Virtual Environment
Always use your virtual environment's Python interpreter:
```bash
/path/to/project/.venv/bin/python
```

### 2. Log Output
Always redirect output to log files:
```bash
command >> output.log 2>&1
```

### 3. Use Absolute Paths
Never use relative paths in scheduled tasks:
```bash
# ❌ Bad
python tracker.py check

# ✅ Good
cd /absolute/path/to/project && /absolute/path/to/python tracker.py check
```

### 4. Test Before Scheduling
Always test the command manually before scheduling:
```bash
# Run the exact command that will be scheduled
cd /path/to/project && /path/to/python tracker.py check
```

### 5. Monitor Logs
Regularly check log files for errors:
```bash
# Set up log rotation to prevent files from growing too large
# Use logrotate (Linux) or configure in app
```

### 6. Handle Failures
Configure retry logic and notifications for failures:
- Python scheduler has built-in error handling
- Cron: Add email notifications
- Task Scheduler: Configure restart on failure

---

## Scheduling Recommendations

### Frequency Guidelines

| Interval | Use Case |
|----------|----------|
| **1-2 hours** | Flash sales, limited-time offers |
| **6 hours** | Regular price monitoring (recommended) |
| **12 hours** | Stable products with infrequent changes |
| **24 hours** | Products with weekly/monthly price cycles |

### Consider:
- **API rate limits** - Some sites may block frequent requests
- **Server load** - Space out checks to avoid detection
- **Battery/resources** - Longer intervals for laptops
- **Data freshness** - How quickly you need to know about changes

---

## Summary

### Quick Start Commands

**Python Scheduler (Recommended):**
```bash
pip install schedule
python scheduler.py
```

**Cron (macOS/Linux):**
```bash
crontab -e
# Add: 0 */6 * * * cd /path/to/project && python3 tracker.py check >> cron.log 2>&1
```

**Task Scheduler (Windows):**
```powershell
# See PowerShell method above or use GUI
```

### Verification Checklist

- ✅ Command runs manually without errors
- ✅ Log files are being created and updated
- ✅ products.csv shows new entries after each run
- ✅ Scheduler/cron/task is enabled and active
- ✅ No error messages in logs
- ✅ System has sufficient resources

---

## Additional Resources

- [Crontab.guru](https://crontab.guru/) - Cron expression generator
- [Python schedule documentation](https://schedule.readthedocs.io/)
- [Windows Task Scheduler documentation](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)

---

**Need help?** Check the troubleshooting section or review the log files for detailed error messages.
