"""
SQLite to Supabase Migration Script
Migrates all data from local khula_collective.db to Supabase PostgreSQL
"""

import os
import sys
import sqlite3
from datetime import datetime
from supabase import create_client, Client

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# SQLite Database Path
SQLITE_DB = "khula_collective.db"

def create_supabase_tables(supabase: Client):
    """Create all necessary tables in Supabase"""
    
    print("📋 Creating Supabase tables...")
    
    # Note: Supabase tables should be created via SQL Editor in Supabase Dashboard
    # This function documents the schema
    
    tables_sql = """
    -- Users Table
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(100),
        email VARCHAR(100),
        phone VARCHAR(20),
        sa_id_number VARCHAR(13),
        role VARCHAR(20) DEFAULT 'member',
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW()
    );

    -- Monthly Contributions Table
    CREATE TABLE IF NOT EXISTS monthly_contributions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        month VARCHAR(7) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending',
        payment_date DATE,
        transaction_reference VARCHAR(100),
        created_at TIMESTAMP DEFAULT NOW()
    );

    -- Global Account Sync Table
    CREATE TABLE IF NOT EXISTS global_account_sync (
        id SERIAL PRIMARY KEY,
        total_balance DECIMAL(15, 2) DEFAULT 0,
        last_sync TIMESTAMP,
        fnb_account_id VARCHAR(100)
    );

    -- Investment Goals Table
    CREATE TABLE IF NOT EXISTS investment_goals (
        id SERIAL PRIMARY KEY,
        current_month VARCHAR(7),
        monthly_target DECIMAL(10, 2),
        monthly_collected DECIMAL(10, 2),
        yearly_target DECIMAL(15, 2),
        updated_at TIMESTAMP DEFAULT NOW()
    );

    -- Votes Table
    CREATE TABLE IF NOT EXISTS votes (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        suggestion_id INTEGER,
        vote_type VARCHAR(20),
        created_at TIMESTAMP DEFAULT NOW(),
        UNIQUE(user_id, suggestion_id)
    );

    -- Investment Suggestions Table
    CREATE TABLE IF NOT EXISTS investment_suggestions (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        category VARCHAR(50),
        expected_return DECIMAL(10, 2),
        risk_level VARCHAR(20),
        priority VARCHAR(20),
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW()
    );

    -- Hall of Fame Table (for monthly archives)
    CREATE TABLE IF NOT EXISTS hall_of_fame (
        id SERIAL PRIMARY KEY,
        month VARCHAR(7) NOT NULL,
        rank INTEGER NOT NULL,
        user_id INTEGER REFERENCES users(id),
        username VARCHAR(50),
        full_name VARCHAR(100),
        amount DECIMAL(10, 2),
        medal VARCHAR(10),
        created_at TIMESTAMP DEFAULT NOW()
    );

    -- Market Data Table
    CREATE TABLE IF NOT EXISTS market_data (
        id SERIAL PRIMARY KEY,
        repo_rate DECIMAL(5, 2),
        prime_rate DECIMAL(5, 2),
        inflation_rate DECIMAL(5, 2),
        jse_all_share DECIMAL(10, 2),
        usd_zar_rate DECIMAL(6, 2),
        last_updated TIMESTAMP DEFAULT NOW()
    );

    -- Member Signatures Table (FICA Compliance)
    CREATE TABLE IF NOT EXISTS member_signatures (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        signature_name VARCHAR(100),
        signed_at TIMESTAMP DEFAULT NOW(),
        ip_address VARCHAR(50),
        constitution_version VARCHAR(20)
    );

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_contributions_user_month ON monthly_contributions(user_id, month);
    CREATE INDEX IF NOT EXISTS idx_votes_user_suggestion ON votes(user_id, suggestion_id);
    CREATE INDEX IF NOT EXISTS idx_hall_of_fame_month ON hall_of_fame(month);
    """
    
    print("✅ Table schema documented (create via Supabase SQL Editor)")
    print("\n📝 Copy the SQL above to Supabase Dashboard > SQL Editor")
    
    return tables_sql

def migrate_users(sqlite_conn, supabase: Client):
    """Migrate users table"""
    
    print("👥 Migrating users...")
    
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    
    migrated = 0
    for user in users:
        user_dict = dict(zip(columns, user))
        
        # Remove SQLite-specific id (Supabase will auto-generate)
        user_dict.pop('id', None)
        
        try:
            supabase.table("users").insert(user_dict).execute()
            migrated += 1
        except Exception as e:
            print(f"⚠️ Failed to migrate user {user_dict.get('username')}: {e}")
    
    print(f"✅ Migrated {migrated}/{len(users)} users")

def migrate_contributions(sqlite_conn, supabase: Client):
    """Migrate monthly contributions"""
    
    print("💰 Migrating contributions...")
    
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT * FROM monthly_contributions")
    contributions = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    
    migrated = 0
    for contrib in contributions:
        contrib_dict = dict(zip(columns, contrib))
        contrib_dict.pop('id', None)
        
        try:
            supabase.table("monthly_contributions").insert(contrib_dict).execute()
            migrated += 1
        except Exception as e:
            print(f"⚠️ Failed to migrate contribution: {e}")
    
    print(f"✅ Migrated {migrated}/{len(contributions)} contributions")

def migrate_global_sync(sqlite_conn, supabase: Client):
    """Migrate global account sync"""
    
    print("🌍 Migrating global account sync...")
    
    cursor = sqlite_conn.cursor()
    cursor.execute("SELECT * FROM global_account_sync")
    sync_data = cursor.fetchone()
    
    if sync_data:
        columns = [desc[0] for desc in cursor.description]
        sync_dict = dict(zip(columns, sync_data))
        sync_dict.pop('id', None)
        
        try:
            supabase.table("global_account_sync").insert(sync_dict).execute()
            print(f"✅ Migrated global balance: R{sync_dict.get('total_balance', 0):,.2f}")
        except Exception as e:
            print(f"⚠️ Failed to migrate global sync: {e}")

def migrate_votes(sqlite_conn, supabase: Client):
    """Migrate votes"""
    
    print("🗳️ Migrating votes...")
    
    cursor = sqlite_conn.cursor()
    
    # Check if votes table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='votes'")
    if not cursor.fetchone():
        print("⚠️ Votes table doesn't exist in SQLite, skipping...")
        return
    
    cursor.execute("SELECT * FROM votes")
    votes = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    
    migrated = 0
    for vote in votes:
        vote_dict = dict(zip(columns, vote))
        vote_dict.pop('id', None)
        
        try:
            supabase.table("votes").insert(vote_dict).execute()
            migrated += 1
        except Exception as e:
            print(f"⚠️ Failed to migrate vote: {e}")
    
    print(f"✅ Migrated {migrated}/{len(votes)} votes")

def migrate_suggestions(sqlite_conn, supabase: Client):
    """Migrate investment suggestions"""
    
    print("💡 Migrating investment suggestions...")
    
    cursor = sqlite_conn.cursor()
    
    # Check if suggestions table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='suggestions'")
    if not cursor.fetchone():
        print("⚠️ Suggestions table doesn't exist in SQLite, skipping...")
        return
    
    cursor.execute("SELECT * FROM suggestions")
    suggestions = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description]
    
    migrated = 0
    for suggestion in suggestions:
        suggestion_dict = dict(zip(columns, suggestion))
        suggestion_dict.pop('id', None)
        
        try:
            supabase.table("investment_suggestions").insert(suggestion_dict).execute()
            migrated += 1
        except Exception as e:
            print(f"⚠️ Failed to migrate suggestion: {e}")
    
    print(f"✅ Migrated {migrated}/{len(suggestions)} suggestions")

def verify_migration(sqlite_conn, supabase: Client):
    """Verify migration success"""
    
    print("\n🔍 Verifying migration...")
    
    # Count records in SQLite
    cursor = sqlite_conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    sqlite_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM monthly_contributions")
    sqlite_contributions = cursor.fetchone()[0]
    
    # Count records in Supabase
    supabase_users = len(supabase.table("users").select("id").execute().data)
    supabase_contributions = len(supabase.table("monthly_contributions").select("id").execute().data)
    
    print(f"👥 Users: SQLite={sqlite_users}, Supabase={supabase_users}")
    print(f"💰 Contributions: SQLite={sqlite_contributions}, Supabase={supabase_contributions}")
    
    if sqlite_users == supabase_users and sqlite_contributions == supabase_contributions:
        print("✅ Migration verified successfully!")
        return True
    else:
        print("⚠️ Migration counts don't match - please review")
        return False

def main():
    """Main migration function"""
    print("🚀 Starting SQLite to Supabase Migration...")
    print(f"⏰ Migration Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Validate environment variables
    if not all([SUPABASE_URL, SUPABASE_KEY]):
        print("❌ Missing SUPABASE_URL or SUPABASE_KEY environment variables")
        print("\n📝 Set them in your environment:")
        print("   export SUPABASE_URL='https://your-project.supabase.co'")
        print("   export SUPABASE_KEY='your-anon-key'")
        sys.exit(1)
    
    # Check SQLite database exists
    if not os.path.exists(SQLITE_DB):
        print(f"❌ SQLite database not found: {SQLITE_DB}")
        sys.exit(1)
    
    # Initialize connections
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print(f"✅ Connected to SQLite: {SQLITE_DB}")
    print(f"✅ Connected to Supabase: {SUPABASE_URL}")
    
    # Create tables schema (for documentation)
    tables_sql = create_supabase_tables(supabase)
    
    # Save SQL to file
    with open("supabase_schema.sql", "w") as f:
        f.write(tables_sql)
    print("✅ Saved schema to supabase_schema.sql")
    
    print("\n⚠️ IMPORTANT: Before proceeding, create tables in Supabase:")
    print("   1. Go to Supabase Dashboard > SQL Editor")
    print("   2. Copy contents of supabase_schema.sql")
    print("   3. Run the SQL to create tables")
    print("   4. Press Enter to continue migration...")
    
    input()
    
    # Migrate data
    try:
        migrate_users(sqlite_conn, supabase)
        migrate_contributions(sqlite_conn, supabase)
        migrate_global_sync(sqlite_conn, supabase)
        migrate_votes(sqlite_conn, supabase)
        migrate_suggestions(sqlite_conn, supabase)
        
        # Verify migration
        verify_migration(sqlite_conn, supabase)
        
        print("\n✅ Migration completed successfully!")
        print("\n📝 Next Steps:")
        print("   1. Update app.py to use Supabase instead of SQLite")
        print("   2. Add SUPABASE_URL and SUPABASE_KEY to Streamlit secrets")
        print("   3. Test the application with cloud database")
        print("   4. Deploy to Streamlit Cloud")
    
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
    
    finally:
        sqlite_conn.close()

if __name__ == "__main__":
    main()