#!/usr/bin/env python
import os
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backup settings
BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', 7))
DATABASE_URL = os.getenv('DATABASE_URL')

def create_backup():
    # Create backup directory if it doesn't exist
    Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'backup_{timestamp}.sql')
    
    try:
        # Parse DATABASE_URL
        db_url = DATABASE_URL.split('/')
        db_name = db_url[-1]
        db_user = db_url[2].split(':')[0]
        
        # Create backup using pg_dump
        subprocess.run([
            'pg_dump',
            '-Fc',  # Custom format
            '-Z9',  # Maximum compression
            '-f', backup_file,
            '-d', db_name,
            '-U', db_user
        ], check=True)
        
        print(f"Backup created successfully: {backup_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")
        return False

def cleanup_old_backups():
    """Remove backups older than RETENTION_DAYS."""
    retention_date = datetime.now() - timedelta(days=RETENTION_DAYS)
    
    for backup_file in Path(BACKUP_DIR).glob('backup_*.sql'):
        # Get file creation time
        file_time = datetime.fromtimestamp(os.path.getctime(backup_file))
        
        # Remove if older than retention period
        if file_time < retention_date:
            backup_file.unlink()
            print(f"Removed old backup: {backup_file}")

if __name__ == '__main__':
    print("Starting database backup...")
    if create_backup():
        cleanup_old_backups()
        print("Backup process completed successfully.")
    else:
        sys.exit(1)
