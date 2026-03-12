import os
import sys
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add the BackEnd directory to sys.path to import application modules
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(script_dir, "../../BackEnd"))
sys.path.insert(0, backend_dir)

try:
    from models import User
    from database import Base
except ImportError:
    print(f"[ERROR] Could not import models.py or database.py from {backend_dir}")
    sys.exit(1)

def format_row(data, widths):
    return " | ".join(str(val).ljust(width) for val, width in zip(data, widths))

def display_table(headers, rows):
    if not rows:
        print("\n[INFO] No users found in the database.")
        return

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    # Print table
    separator = "-+-".join("-" * width for width in widths)
    print("\n" + format_row(headers, widths))
    print(separator)
    for row in rows:
        print(format_row(row, widths))
    print(f"\nTotal: {len(rows)} users\n")

def main():
    parser = argparse.ArgumentParser(description="Extract User Details from JanSetu Database")
    parser.add_argument("--url", help="Full Database URL (postgresql://...)")
    args = parser.parse_args()

    db_url = args.url
    if not db_url:
        print("\n[ERROR] Database URL is required.")
        print("Example: python extract_users.py --url \"postgresql://user:pass@host/dbname\"")
        sys.exit(1)

    print(f"\nConnecting to database...")
    try:
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test connection
        session.execute(text("SELECT 1"))
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
        sys.exit(1)

    try:
        users = session.query(User).all()
        if not users:
            print("\n[INFO] No users found.")
            return

        while True:
            print("========================================")
            print("   JanSetu USER EXTRACTION MENU")
            print("========================================")
            print("1. Display Basic Info (Name, Email, Role)")
            print("2. Display Professional Info (Ward, Dept, Points)")
            print("3. Display Account Status (Active, Suspended, Created)")
            print("4. Display All Details")
            print("5. Exit")
            print("========================================")
            
            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == '1':
                headers = ["Full Name", "Email", "Role"]
                rows = [[u.full_name, u.email, u.role] for u in users]
                display_table(headers, rows)
            elif choice == '2':
                headers = ["Full Name", "Ward", "Department", "Points"]
                rows = [[u.full_name, u.ward if u.ward else "N/A", u.department if u.department else "N/A", u.points] for u in users]
                display_table(headers, rows)
            elif choice == '3':
                headers = ["Full Name", "Is Active", "Is Suspended", "Joined At"]
                rows = [[u.full_name, u.is_active, u.is_suspended, u.created_at.strftime("%Y-%m-%d") if u.created_at else "N/A"] for u in users]
                display_table(headers, rows)
            elif choice == '4':
                headers = ["ID", "Full Name", "Email", "Role", "Ward", "Dept", "Points", "Active"]
                rows = [[u.id, u.full_name, u.email, u.role, u.ward if u.ward else "-", u.department if u.department else "-", u.points, "Yes" if u.is_active else "No"] for u in users]
                display_table(headers, rows)
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("\n[INVALID] Please enter a number between 1 and 5.")

    except Exception as e:
        print(f"\n[ERROR] An error occurred while fetching data: {e}")
        print("Tip: Make sure the URL is correct and the database is accessible.")
    finally:
        session.close()

if __name__ == "__main__":
    from sqlalchemy import text # Ensure text is imported for the check
    main()
