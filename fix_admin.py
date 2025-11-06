"""
Script to create or reset admin user with password '1024'
Run this if you're having trouble logging in as admin.
"""
import sys
from werkzeug.security import generate_password_hash
import models

def fix_admin():
    """Create or update admin user with password '1024'"""
    try:
        # Check if admin exists
        admin_user = models.get_user_by_username('admin')
        
        if admin_user:
            # Update existing admin password
            print("Admin user exists. Updating password...")
            pw_hash = generate_password_hash('1024')
            # Update password
            models.update_password(admin_user['id'], pw_hash)
            print("[SUCCESS] Admin password updated successfully!")
            print("   Username: admin")
            print("   Password: 1024")
        else:
            # Create new admin user
            print("Creating new admin user...")
            pw_hash = generate_password_hash('1024')
            models.add_user('admin', pw_hash, 'admin@internship.com', role='admin')
            print("[SUCCESS] Admin user created successfully!")
            print("   Username: admin")
            print("   Password: 1024")
            
    except Exception as e:
        print(f"[ERROR] {e}")
        print("\nMake sure:")
        print("1. MySQL server is running")
        print("2. Database 'internship_db' exists")
        print("3. Your MySQL credentials in config.py are correct")
        sys.exit(1)

if __name__ == '__main__':
    print("=" * 50)
    print("Admin User Fix Script")
    print("=" * 50)
    fix_admin()
    print("=" * 50)

