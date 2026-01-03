import os
import random
import datetime
import subprocess

# Config
LOG_FILE = "log.txt"
START_HOUR = 8   # 08:00 UTC
END_HOUR = 22    # 22:00 UTC

def git_commit():
    """Performs the git add, commit, and push operations."""
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        
        subprocess.run(["git", "add", LOG_FILE], check=True)
        
        messages = [
            "Update daily log",
            "Log entry",
            "Daily update", 
            "Routine check",
            "Update status",
            "Automated log"
        ]
        commit_message = random.choice(messages)
        
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print(f"✅ Commit successful: {commit_message}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during git operation: {e}")
        exit(1)

def main():
    now = datetime.datetime.utcnow()
    current_hour = now.hour
    today_str = now.strftime("%Y-%m-%d")

    # 1. Read last commit date
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("2000-01-01 00:00:00")
    
    with open(LOG_FILE, "r") as f:
        last_content = f.read().strip()
    
    # Check if already committed today
    if today_str in last_content:
        print("⏭️  Already committed today. Skipping.")
        exit(0)

    # 2. Logic to decide whether to commit NOW
    # If it's the last chance (>= END_HOUR), force commit.
    should_commit = False
    
    if current_hour >= END_HOUR:
        print("⚠️  Last chance of the day! Forcing commit.")
        should_commit = True
    elif current_hour < START_HOUR:
        print("💤 Too early. Sleeping.")
        should_commit = False
    else:
        # Probability check
        # chance increases as hours go by? OR just flat chance?
        # If we run every hour from 8 to 22 (15 runs).
        # We need at least one success.
        # Simple random: 20% chance per hour is usually enough to hit once.
        if random.random() < 0.20:
             print("🎲 Random check passed! Committing.")
             should_commit = True
        else:
             print("🎲 Random check failed. Waiting for next hour.")

    # 3. Execute Commit
    if should_commit:
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "w") as f:
            f.write(timestamp)
        
        git_commit()

if __name__ == "__main__":
    main()
