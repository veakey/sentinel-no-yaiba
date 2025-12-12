"""
Migration script to add access_token_encrypted and token_expires_at fields to providers table
"""
import sys
import os
import sqlite3
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings


def migrate_add_token_fields():
    """
    Add access_token_encrypted and token_expires_at fields to providers table.
    """
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    
    if not os.path.exists(db_path):
        print(f"[INFO] Database file {db_path} does not exist. No migration needed.")
        return
    
    print(f"[INFO] Starting migration for database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if migration is needed
        cursor.execute("PRAGMA table_info(providers)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'access_token_encrypted' in column_names and 'token_expires_at' in column_names:
            print("[INFO] access_token_encrypted and token_expires_at columns already exist. No migration needed.")
            return
        
        print("[INFO] Adding access_token_encrypted and token_expires_at columns...")
        
        # Add access_token_encrypted column
        if 'access_token_encrypted' not in column_names:
            cursor.execute("ALTER TABLE providers ADD COLUMN access_token_encrypted TEXT")
            print("[INFO] Added access_token_encrypted column")
        
        # Add token_expires_at column
        if 'token_expires_at' not in column_names:
            cursor.execute("ALTER TABLE providers ADD COLUMN token_expires_at DATETIME")
            print("[INFO] Added token_expires_at column")
        
        conn.commit()
        print("[SUCCESS] Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {str(e)}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    migrate_add_token_fields()

