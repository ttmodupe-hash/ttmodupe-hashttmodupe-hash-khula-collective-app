"""
Monthly Reset Script
Runs on the 1st of every month to:
1. Archive previous month's Hall of Fame
2. Reset monthly targets
3. Create new contribution records for all members
"""

import os
import sys
from datetime import datetime, timedelta
from supabase import create_client, Client

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def archive_hall_of_fame(supabase: Client):
    """Archive previous month's top contributors"""
    
    # Get previous month
    today = datetime.now()
    first_of_month = today.replace(day=1)
    last_month = first_of_month - timedelta(days=1)
    month_str = last_month.strftime("%Y-%m")
    
    print(f"📦 Archiving Hall of Fame for {month_str}...")
    
    try:
        # Get all contributions for last month
        result = supabase.table("monthly_contributions").select("*").eq("month", month_str).eq("status", "Received").execute()
        
        if not result.data:
            print(f"⚠️ No contributions found for {month_str}")
            return
        
        # Calculate top 3 contributors
        contributions = result.data
        user_totals = {}
        
        for contrib in contributions:
            user_id = contrib["user_id"]
            amount = contrib["amount"]
            user_totals[user_id] = user_totals.get(user_id, 0) + amount
        
        # Sort by amount
        top_3 = sorted(user_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Get user details
        hall_of_fame = []
        for rank, (user_id, amount) in enumerate(top_3, 1):
            user_result = supabase.table("users").select("username, full_name").eq("id", user_id).execute()
            if user_result.data:
                user = user_result.data[0]
                hall_of_fame.append({
                    "month": month_str,
                    "rank": rank,
                    "user_id": user_id,
                    "username": user["username"],
                    "full_name": user.get("full_name", user["username"]),
                    "amount": amount,
                    "medal": ["🥇", "🥈", "🥉"][rank - 1]
                })
        
        # Insert into hall_of_fame table
        if hall_of_fame:
            supabase.table("hall_of_fame").insert(hall_of_fame).execute()
            print(f"✅ Archived {len(hall_of_fame)} top contributors")
            
            for entry in hall_of_fame:
                print(f"   {entry['medal']} {entry['full_name']}: R{entry['amount']:,.2f}")
    
    except Exception as e:
        print(f"❌ Failed to archive Hall of Fame: {e}")

def create_new_month_contributions(supabase: Client):
    """Create new contribution records for current month"""
    
    current_month = datetime.now().strftime("%Y-%m")
    print(f"📅 Creating contribution records for {current_month}...")
    
    try:
        # Get all active members
        result = supabase.table("users").select("id, username").eq("is_active", True).neq("role", "admin").execute()
        
        if not result.data:
            print("⚠️ No active members found")
            return
        
        members = result.data
        new_contributions = []
        
        for member in members:
            new_contributions.append({
                "user_id": member["id"],
                "month": current_month,
                "amount": 300,
                "status": "Pending",
                "created_at": datetime.now().isoformat()
            })
        
        # Insert new contributions
        supabase.table("monthly_contributions").insert(new_contributions).execute()
        print(f"✅ Created {len(new_contributions)} contribution records for {current_month}")
    
    except Exception as e:
        print(f"❌ Failed to create new contributions: {e}")

def reset_monthly_stats(supabase: Client):
    """Reset monthly statistics and targets"""
    
    print("🔄 Resetting monthly statistics...")
    
    try:
        # Update investment_goals table with new month
        current_month = datetime.now().strftime("%Y-%m")
        
        supabase.table("investment_goals").update({
            "current_month": current_month,
            "monthly_target": 6000,  # R300 x 20 members
            "monthly_collected": 0,
            "updated_at": datetime.now().isoformat()
        }).eq("id", 1).execute()
        
        print(f"✅ Reset monthly targets for {current_month}")
    
    except Exception as e:
        print(f"❌ Failed to reset monthly stats: {e}")

def send_monthly_summary(supabase: Client):
    """Send monthly summary to all members (via WhatsApp/Email)"""
    
    print("📧 Sending monthly summaries...")
    
    try:
        # Get last month's data
        today = datetime.now()
        first_of_month = today.replace(day=1)
        last_month = first_of_month - timedelta(days=1)
        month_str = last_month.strftime("%Y-%m")
        
        # Get total collected last month
        result = supabase.table("monthly_contributions").select("amount").eq("month", month_str).eq("status", "Received").execute()
        
        total_collected = sum(contrib["amount"] for contrib in result.data) if result.data else 0
        
        # Get current balance
        balance_result = supabase.table("global_account_sync").select("total_balance").execute()
        current_balance = balance_result.data[0]["total_balance"] if balance_result.data else 0
        
        summary = f"""
🎉 Khula Collective Monthly Summary - {last_month.strftime("%B %Y")}

💰 Last Month Collected: R{total_collected:,.2f}
💼 Current Total Balance: R{current_balance:,.2f}
👥 Active Members: 20

🏆 Hall of Fame archived!
📅 New month started: {today.strftime("%B %Y")}

Keep contributing R300/month to grow our collective pot! 🚀
        """
        
        print(summary)
        print("✅ Monthly summary prepared (WhatsApp integration pending)")
    
    except Exception as e:
        print(f"❌ Failed to send monthly summary: {e}")

def main():
    """Main monthly reset function"""
    print("🚀 Starting Monthly Reset...")
    print(f"⏰ Reset Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S SAST')}")
    
    # Validate environment variables
    if not all([SUPABASE_URL, SUPABASE_KEY]):
        print("❌ Missing required environment variables")
        sys.exit(1)
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Execute monthly tasks
    archive_hall_of_fame(supabase)
    create_new_month_contributions(supabase)
    reset_monthly_stats(supabase)
    send_monthly_summary(supabase)
    
    print("✅ Monthly reset completed successfully!")

if __name__ == "__main__":
    main()