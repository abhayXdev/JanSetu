import os
import sys
import argparse
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    from database import Base
    from models import User, Complaint, ComplaintActivity, ComplaintUpdate, ComplaintUpvote, EmailOTP
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    
    parser = argparse.ArgumentParser(description="Clean up JanSetu database")
    parser.add_argument("--url", help="Database URL")
    parser.add_argument("--force", action="store_true", help="Skip confirmation")
    args = parser.parse_args()

    db_url = args.url
    if not db_url:
        print("Database URL is required.")
        sys.exit(1)
        
    print(f"\nConnecting to database...")
    
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Check what users exist
        all_users = session.query(User).all()
        print(f"\n[INFO] Total users found in DB: {len(all_users)}")
        
        # Keep any user with role 'admin'
        admins = [u for u in all_users if u.role == "admin" or u.email.startswith("admin")]
        print(f"[INFO] Admins found (these will be KEPT): {[u.email for u in admins]}")
        
        if not args.force:
            confirm = input("\nThis will permanently CLEAR all complaints and non-admin users. Proceed? (y/N): ")
            if confirm.lower() != 'y':
                print("Cleanup cancelled.")
                sys.exit(0)

        # Remove Complaint references
        print("Clearing merged_into_id references...")
        session.execute(text("UPDATE complaints SET merged_into_id = NULL"))

        print("Deleting ComplaintActivities...")
        session.query(ComplaintActivity).delete(synchronize_session=False)
        
        print("Deleting ComplaintUpdates...")
        session.query(ComplaintUpdate).delete(synchronize_session=False)
        
        print("Deleting ComplaintUpvotes...")
        session.query(ComplaintUpvote).delete(synchronize_session=False)
        
        print("Deleting Complaints...")
        session.query(Complaint).delete(synchronize_session=False)
        
        print("Deleting EmailOTPs...")
        session.query(EmailOTP).delete(synchronize_session=False)
        
        # Now delete non-admin users
        print("Deleting citizen and officer Users...")
        admin_ids = [a.id for a in admins]
        if admin_ids:
            deleted_users = session.query(User).filter(User.id.notin_(admin_ids)).delete(synchronize_session=False)
        else:
            deleted_users = session.query(User).delete(synchronize_session=False)
            
        print(f"Deleted {deleted_users} dummy users.")
        
        session.commit()
        print("\nSUCCESS: Database cleared successfully! Only admin user(s) remain.")
    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
