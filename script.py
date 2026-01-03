import logging
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Configuration
LOG_FILE_PATH = Path("log.txt")
START_HOUR = 8   # 08:00 UTC
END_HOUR = 22    # 22:00 UTC
PROBABILITY = 0.20 # 20% chance per run

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command: list) -> None:
    """Executes a shell command with error handling."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {' '.join(command)}")
        sys.exit(1)

def git_commit_and_push(file_path: Path) -> None:
    """Stages, commits, and pushes changes to the repository."""
    # Configure git specific to this run (idempotent)
    run_command(["git", "config", "user.name", "github-actions[bot]"])
    run_command(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    
    run_command(["git", "add", str(file_path)])
    
    commit_messages = [
        "Update daily log",
        "Log entry",
        "Daily update", 
        "Routine check",
        "Update status",
        "Automated log"
    ]
    message = random.choice(commit_messages)
    
    try:
        subprocess.run(["git", "commit", "-m", message], check=True)
        # Explicitly push to origin main to avoid detached head issues
        subprocess.run(["git", "push", "origin", "master"], check=True)
        logging.info(f"Commit successful: {message}")
    except subprocess.CalledProcessError:
        logging.warning("Nothing to commit or push failed. Checking logic recommended.")

def should_commit(current_hour: int, has_committed: bool) -> bool:
    """Decides whether to commit based on time and probability."""
    if has_committed:
        logging.info("Already committed today. Skipping.")
        return False

    if current_hour >= END_HOUR:
        logging.info("Last chance of the day. Forcing commit.")
        return True
    
    if current_hour < START_HOUR:
        logging.info("Outside valid hours. Skipping.")
        return False
        
    if random.random() < PROBABILITY:
        logging.info("Random check passed. Proceeding with commit.")
        return True
    
    logging.info("Random check failed. Waiting for next schedule.")
    return False

def main():
    # Use UTC explicitly as GitHub Actions runs in UTC
    now = datetime.utcnow()
    current_hour = now.hour
    today_str = now.strftime("%Y-%m-%d")

    # Ensure log file exists
    if not LOG_FILE_PATH.exists():
        LOG_FILE_PATH.touch()

    content = LOG_FILE_PATH.read_text(encoding="utf-8")
    has_committed = today_str in content

    if should_commit(current_hour, has_committed):
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        # Append mode 'a' ensures file modifications are always detected by git
        with LOG_FILE_PATH.open("a", encoding="utf-8") as f:
            f.write(f"{timestamp}\n")
        
        git_commit_and_push(LOG_FILE_PATH)

if __name__ == "__main__":
    main()
