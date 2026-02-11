"""
Khula Collective Data Seeding Script
Populates database with 20 members and historical contributions
"""

import sqlite3
import random
from datetime import datetime, timedelta, date
from khula_database import KhulaDatabase


def generate_sa_id(birth_year, birth_month, birth_day, gender):
    """Generate a valid SA ID number with Luhn checksum"""
    # Format: YYMMDD SSSS C A Z
    yy = str(birth_year % 100).zfill(2)
    mm = str(birth_month).zfill(2)
    dd = str(birth_day).zfill(2)
    
    # Gender sequence (0000-4999 female, 5000-9999 male)
    if gender == "Female":
        ssss = str(random.randint(0, 4999)).zfill(4)
    else:
        ssss = str(random.randint(5000, 9999)).zfill(4)
    
    # Citizenship (0 = SA Citizen)
    c = "0"
    
    # Usually 8 for old IDs, but can be other
    a = "8"
    
    # Calculate Luhn checksum
    id_without_check = yy + mm + dd + ssss + c + a
    
    # Luhn algorithm
    digits = [int(d) for d in id_without_check]
    odd_sum = sum(digits[0::2])
    even_str = "".join(map(str, [d * 2 for d in digits[1::2]]))
    even_sum = sum(int(d) for d in even_str)
    
    total = odd_sum + even_sum
    check_digit = (10 - (total % 10)) % 10
    
    return id_without_check + str(check_digit)


def seed_khula_data():
    """Seed the Khula Collective database"""
    
    print("🔧 Initializing Khula Collective Database...")
    
    db = KhulaDatabase()
    
    # Member names (20 members)
    members_data = [
        {"first_name": "Thabo", "surname": "Mthembu", "gender": "Male", "birth_year": 1990},
        {"first_name": "Nomsa", "surname": "Dlamini", "gender": "Female", "birth_year": 1992},
        {"first_name": "Sipho", "surname": "Khumalo", "gender": "Male", "birth_year": 1988},
        {"first_name": "Zanele", "surname": "Ndlovu", "gender": "Female", "birth_year": 1995},
        {"first_name": "Mandla", "surname": "Zulu", "gender": "Male", "birth_year": 1987},
        {"first_name": "Precious", "surname": "Mokoena", "gender": "Female", "birth_year": 1993},
        {"first_name": "Bongani", "surname": "Nkosi", "gender": "Male", "birth_year": 1991},
        {"first_name": "Lindiwe", "surname": "Sithole", "gender": "Female", "birth_year": 1994},
        {"first_name": "Themba", "surname": "Radebe", "gender": "Male", "birth_year": 1989},
        {"first_name": "Nokuthula", "surname": "Mahlangu", "gender": "Female", "birth_year": 1996},
        {"first_name": "Sello", "surname": "Molefe", "gender": "Male", "birth_year": 1990},
        {"first_name": "Thandi", "surname": "Buthelezi", "gender": "Female", "birth_year": 1992},
        {"first_name": "Jabu", "surname": "Ngcobo", "gender": "Male", "birth_year": 1988},
        {"first_name": "Zinhle", "surname": "Mkhize", "gender": "Female", "birth_year": 1994},
        {"first_name": "Mpho", "surname": "Maseko", "gender": "Male", "birth_year": 1991},
        {"first_name": "Ntombi", "surname": "Cele", "gender": "Female", "birth_year": 1993},
        {"first_name": "Vusi", "surname": "Shabalala", "gender": "Male", "birth_year": 1989},
        {"first_name": "Busisiwe", "surname": "Gumede", "gender": "Female", "birth_year": 1995},
        {"first_name": "Sandile", "surname": "Naidoo", "gender": "Male", "birth_year": 1990},
        {"first_name": "Nompumelelo", "surname": "Khoza", "gender": "Female", "birth_year": 1992},
    ]
    
    # Create admin user first
    print("\n👤 Creating admin user...")
    try:
        admin_id_number = generate_sa_id(1985, 5, 15, "Male")
        admin_id = db.create_user(
            username="admin_khula",
            first_name="Admin",
            surname="Khula",
            id_number=admin_id_number,
            rica_number="0821234567",
            email="admin@khulacollective.co.za",
            password="admin123",
            is_admin=True
        )
        if admin_id:
            db.sign_constitution(admin_id)
            print(f"  ✅ Created admin user (ID: {admin_id})")
    except Exception as e:
        print(f"  ⚠️  Admin user may already exist: {e}")
    
    # Create 20 members
    print("\n👥 Creating 20 members...")
    created_members = []
    
    for i, member_data in enumerate(members_data, 1):
        try:
            # Generate valid SA ID
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            id_number = generate_sa_id(
                member_data['birth_year'],
                birth_month,
                birth_day,
                member_data['gender']
            )
            
            # Generate username
            username = f"{member_data['first_name'].lower()}_{member_data['surname'].lower()}"
            
            # Generate RICA number
            rica_number = f"0{random.randint(60, 89)}{random.randint(1000000, 9999999)}"
            
            # Generate email
            email = f"{username}@example.com"
            
            user_id = db.create_user(
                username=username,
                first_name=member_data['first_name'],
                surname=member_data['surname'],
                id_number=id_number,
                rica_number=rica_number,
                email=email,
                password="password123"
            )
            
            if user_id:
                # Sign constitution
                db.sign_constitution(user_id)
                created_members.append(user_id)
                print(f"  ✅ Created: {member_data['first_name']} {member_data['surname']} (ID: {user_id})")
        except Exception as e:
            print(f"  ⚠️  Error creating {member_data['first_name']}: {e}")
    
    # Generate contributions from Jan 2025 to current month
    print("\n💰 Generating monthly contributions...")
    
    start_date = date(2025, 1, 1)
    current_date = date.today()
    
    total_contributions = 0
    
    # Iterate through each month
    current_month_date = start_date
    while current_month_date <= current_date:
        month = current_month_date.month
        year = current_month_date.year
        
        print(f"\n  📅 Processing {current_month_date.strftime('%B %Y')}...")
        
        for user_id in created_members:
            # 90% compliance rate (some members miss payments)
            if random.random() > 0.10:
                # Random payment date within the month (usually towards end)
                day_offset = random.randint(20, 28)
                payment_date = date(year, month, min(day_offset, 28))
                
                # Ensure payment date is not in the future
                if payment_date <= current_date:
                    db.record_contribution(
                        user_id=user_id,
                        month=month,
                        year=year,
                        amount=300.00,
                        payment_date=payment_date,
                        payment_reference=f"KHULA{year}{month:02d}{user_id:03d}"
                    )
                    total_contributions += 300.00
        
        # Move to next month
        if month == 12:
            current_month_date = date(year + 1, 1, 1)
        else:
            current_month_date = date(year, month + 1, 1)
    
    print(f"\n  ✅ Generated contributions totaling R{total_contributions:,.2f}")
    
    # Update global balance
    print("\n🌍 Updating global account balance...")
    total_pot = db.get_total_pot()
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO GlobalAccountSync (total_balance, last_updated)
        VALUES (?, ?)
    """, (total_pot, datetime.now()))
    conn.commit()
    conn.close()
    
    print(f"  ✅ Total Pot: R{total_pot:,.2f}")
    
    # Display summary
    print("\n" + "="*60)
    print("✅ KHULA COLLECTIVE DATABASE SEEDED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"  • Total Members: {len(created_members)} + 1 Admin")
    print(f"  • Total Contributions: R{total_pot:,.2f}")
    print(f"  • Average per Member: R{total_pot/len(created_members):,.2f}")
    print(f"  • Period: Jan 2025 - {current_date.strftime('%B %Y')}")
    
    print(f"\n🔐 Login Credentials:")
    print(f"  Admin:")
    print(f"    Username: admin_khula")
    print(f"    Password: admin123")
    print(f"\n  Members:")
    print(f"    Username: [firstname]_[surname] (e.g., thabo_mthembu)")
    print(f"    Password: password123")
    
    print(f"\n🚀 You can now run the Khula Collective app!")


if __name__ == "__main__":
    seed_khula_data()