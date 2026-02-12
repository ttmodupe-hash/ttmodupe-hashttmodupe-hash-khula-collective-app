"""
FNB Stitch API Sync Script
Automatically syncs transactions from FNB via Stitch API
Updates member contributions from 'Pending' to 'Received'
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from supabase import create_client, Client

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Stitch API Configuration
STITCH_CLIENT_ID = os.getenv("STITCH_CLIENT_ID")
STITCH_CLIENT_SECRET = os.getenv("STITCH_CLIENT_SECRET")
STITCH_API_URL = "https://api.stitch.money/graphql"

def get_stitch_token():
    """Get OAuth token from Stitch API"""
    try:
        response = requests.post(
            "https://secure.stitch.money/connect/token",
            data={
                "grant_type": "client_credentials",
                "client_id": STITCH_CLIENT_ID,
                "client_secret": STITCH_CLIENT_SECRET,
                "scope": "transactions"
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Failed to get Stitch token: {e}")
        return None

def fetch_fnb_transactions(token, days_back=7):
    """Fetch recent FNB transactions via Stitch GraphQL API"""
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    query = """
    query GetTransactions($accountId: ID!, $fromDate: Date!, $toDate: Date!) {
      node(id: $accountId) {
        ... on BankAccount {
          transactions(from: $fromDate, to: $toDate) {
            edges {
              node {
                id
                amount
                date
                description
                reference
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "accountId": os.getenv("FNB_ACCOUNT_ID"),
        "fromDate": start_date.strftime("%Y-%m-%d"),
        "toDate": end_date.strftime("%Y-%m-%d")
    }
    
    try:
        response = requests.post(
            STITCH_API_URL,
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            print(f"❌ GraphQL errors: {data['errors']}")
            return []
        
        transactions = data.get("data", {}).get("node", {}).get("transactions", {}).get("edges", [])
        return [edge["node"] for edge in transactions]
    
    except Exception as e:
        print(f"❌ Failed to fetch transactions: {e}")
        return []

def sync_contributions(supabase: Client, transactions):
    """Update pending contributions to 'Received' based on FNB transactions"""
    
    updated_count = 0
    
    for txn in transactions:
        amount = float(txn["amount"])
        description = txn.get("description", "").lower()
        reference = txn.get("reference", "").lower()
        txn_date = datetime.strptime(txn["date"], "%Y-%m-%d")
        
        # Filter for R300 deposits (Khula contributions)
        if amount != 300.0:
            continue
        
        # Look for pending contributions in the same month
        try:
            result = supabase.table("monthly_contributions").select("*").eq("status", "Pending").eq("amount", 300).execute()
            
            for contribution in result.data:
                contrib_date = datetime.strptime(contribution["month"], "%Y-%m")
                
                # Match by month and amount
                if contrib_date.year == txn_date.year and contrib_date.month == txn_date.month:
                    # Update to 'Received'
                    supabase.table("monthly_contributions").update({
                        "status": "Received",
                        "payment_date": txn["date"],
                        "transaction_reference": txn["id"]
                    }).eq("id", contribution["id"]).execute()
                    
                    updated_count += 1
                    print(f"✅ Updated contribution for {contribution['user_id']} - {contribution['month']}")
        
        except Exception as e:
            print(f"❌ Error updating contribution: {e}")
    
    return updated_count

def main():
    """Main sync function"""
    print("🚀 Starting FNB Stitch Sync...")
    print(f"⏰ Sync Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S SAST')}")
    
    # Validate environment variables
    if not all([SUPABASE_URL, SUPABASE_KEY, STITCH_CLIENT_ID, STITCH_CLIENT_SECRET]):
        print("❌ Missing required environment variables")
        sys.exit(1)
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Get Stitch token
    token = get_stitch_token()
    if not token:
        print("❌ Failed to authenticate with Stitch API")
        sys.exit(1)
    
    print("✅ Authenticated with Stitch API")
    
    # Fetch recent transactions (last 7 days)
    transactions = fetch_fnb_transactions(token, days_back=7)
    print(f"📊 Found {len(transactions)} transactions in last 7 days")
    
    # Sync contributions
    updated = sync_contributions(supabase, transactions)
    print(f"✅ Updated {updated} contributions from Pending → Received")
    
    # Update global account balance
    try:
        total_deposits = sum(float(txn["amount"]) for txn in transactions if float(txn["amount"]) > 0)
        
        if total_deposits > 0:
            result = supabase.table("global_account_sync").select("total_balance").execute()
            current_balance = result.data[0]["total_balance"] if result.data else 0
            
            new_balance = current_balance + total_deposits
            supabase.table("global_account_sync").update({
                "total_balance": new_balance,
                "last_sync": datetime.now().isoformat()
            }).eq("id", 1).execute()
            
            print(f"💰 Updated global balance: R{current_balance:,.2f} → R{new_balance:,.2f}")
    
    except Exception as e:
        print(f"❌ Failed to update global balance: {e}")
    
    print("✅ Sync completed successfully!")

if __name__ == "__main__":
    main()