"""
Migration script to make api_key_encrypted nullable in providers table
"""
import sys
import os
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings


def migrate_api_key_nullable():
    """
    Make api_key_encrypted nullable in providers table.
    
    Note: SQLite doesn't support ALTER TABLE MODIFY COLUMN directly.
    We need to recreate the table with the new schema.
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
        
        # Find api_key_encrypted column
        api_key_col = None
        for col in columns:
            if col[1] == 'api_key_encrypted':
                api_key_col = col
                break
        
        if not api_key_col:
            print("[ERROR] api_key_encrypted column not found in providers table")
            return
        
        # Check if already nullable (notnull = 0 means nullable)
        if api_key_col[3] == 0:
            print("[INFO] api_key_encrypted is already nullable. No migration needed.")
            return
        
        print("[INFO] api_key_encrypted is NOT NULL. Starting migration...")
        
        # SQLite doesn't support ALTER TABLE MODIFY COLUMN
        # We need to recreate the table
        # Step 1: Create new table with nullable api_key_encrypted
        cursor.execute("""
            CREATE TABLE providers_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guid TEXT NOT NULL UNIQUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                api_key_encrypted TEXT,
                base_url TEXT,
                config TEXT,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                provider_specific_settings TEXT
            )
        """)
        
        # Step 2: Copy data from old table to new table
        cursor.execute("""
            INSERT INTO providers_new 
            (id, guid, created_at, updated_at, name, type, api_key_encrypted, base_url, config, is_active, provider_specific_settings)
            SELECT 
                id, guid, created_at, updated_at, name, type, api_key_encrypted, base_url, config, is_active, provider_specific_settings
            FROM providers
        """)
        
        # Step 3: Drop old table
        cursor.execute("DROP TABLE providers")
        
        # Step 4: Rename new table to original name
        cursor.execute("ALTER TABLE providers_new RENAME TO providers")
        
        # Step 5: Recreate indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_providers_guid ON providers(guid)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_providers_name ON providers(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_providers_type ON providers(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_providers_is_active ON providers(is_active)")
        
        conn.commit()
        print("[SUCCESS] Migration completed successfully!")
        print("[INFO] api_key_encrypted is now nullable in providers table")
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {str(e)}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    migrate_api_key_nullable()

