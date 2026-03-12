import os
import sys
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    from database import Base
    from models import User
    from security import hash_password
    
    parser = argparse.ArgumentParser(description="Create Sudo User")
    parser.add_argument("--url", help="Database URL")
    args = parser.parse_args()

    db_url = args.url
    if not db_url:
        print("Database URL is required.")
        sys.exit(1)
        
    print(f"\nConnecting to database to ensure Sudo user exists...")
    
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check if sudo user exists
        sudo_email = "sudo@JanSetu.com"
        existing_sudo = session.query(User).filter(User.email == sudo_email).first()
        
        if existing_sudo:
            print(f"[INFO] Sudo user '{sudo_email}' already exists.")
            print("[INFO] Resetting password to 'adminpassword' just in case...")
            existing_sudo.password_hash = hash_password("adminpassword")
            existing_sudo.role = "sudo"
            existing_sudo.is_active = True
            session.commit()
            print("[SUCCESS] Sudo user password reset successfully!")
        else:
            print(f"[INFO] Sudo user '{sudo_email}' not found. Creating...")
            sudo_user = User(
                full_name="Sudo User",
                email=sudo_email,
                password_hash=hash_password("adminpassword"),
                role="sudo",
                is_active=True
            )
            session.add(sudo_user)
            session.commit()
            print("[SUCCESS] Successfully created Sudo account.")
            
        print("\nLogin Credentials:")
        print(f"Email: {sudo_email}")
        print("Password: adminpassword")
        print("Role Tab: Super Admin")
        
    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
