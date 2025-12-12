"""
Script to create a default admin user in the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.database.models import User, UserRole
from app.database.base import Base
from app.auth.password import hash_password


def create_admin_user(username: str = "admin", password: str = "admin123", email: str = "admin@example.com"):
    """
    Create a default admin user in the database.
    
    Args:
        username: Admin username (default: "admin")
        password: Admin password (default: "admin123")
        email: Admin email (default: "admin@example.com")
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            print(f"[ERROR] User with username '{username}' or email '{email}' already exists!")
            print(f"   GUID: {existing_user.guid}")
            print(f"   Role: {existing_user.role}")
            if existing_user.role != UserRole.ADMIN.value:
                print(f"   [WARNING] User exists but is not an admin. Updating role to admin...")
                existing_user.role = UserRole.ADMIN.value
                existing_user.is_active = True
                db.commit()
                print(f"[SUCCESS] User role updated to admin!")
            return existing_user
        
        # Create new admin user
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=UserRole.ADMIN.value,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"[SUCCESS] Admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   GUID: {admin_user.guid}")
        print(f"   Role: {admin_user.role}")
        print(f"\n[WARNING] Default password: {password}")
        print(f"   Please change this password after first login!")
        
        return admin_user
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error creating admin user: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create a default admin user")
    parser.add_argument("--username", default="admin", help="Admin username (default: admin)")
    parser.add_argument("--password", default="admin123", help="Admin password (default: admin123)")
    parser.add_argument("--email", default="admin@example.com", help="Admin email (default: admin@example.com)")
    
    args = parser.parse_args()
    
    create_admin_user(
        username=args.username,
        password=args.password,
        email=args.email
    )

