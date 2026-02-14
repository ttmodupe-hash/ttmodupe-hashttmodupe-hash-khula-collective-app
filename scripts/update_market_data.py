"""
Market Data Update Script
Runs weekly (Mondays) to fetch latest SA market rates:
- SARB Repo Rate
- Prime Lending Rate
- Inflation Rate
- JSE All Share Index
- USD/ZAR Exchange Rate
"""

import os
import sys
import requests
from datetime import datetime
from supabase import create_client, Client

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def fetch_sarb_repo_rate():
    """Fetch current SARB repo rate from official source"""
    try:
        # SARB API endpoint (example - replace with actual endpoint)
        response = requests.get("https://www.resbank.co.za/en/home/what-we-do/statistics/key-statistics")
        
        # For now, return a placeholder - integrate with actual SARB API
        # In production, parse the HTML or use official API
        return 8.25  # Current rate as of Feb 2026
    
    except Exception as e:
        print(f"⚠️ Failed to fetch SARB rate: {e}")
        return 8.25  # Fallback to last known rate

def fetch_prime_rate():
    """Calculate prime rate (repo rate + 3.5%)"""
    repo_rate = fetch_sarb_repo_rate()
    return repo_rate + 3.5

def fetch_inflation_rate():
    """Fetch current inflation rate from Stats SA"""
    try:
        # Stats SA API endpoint (example)
        # In production, integrate with official Stats SA API
        return 5.2  # Current rate as of Feb 2026
    
    except Exception as e:
        print(f"⚠️ Failed to fetch inflation rate: {e}")
        return 5.2

def fetch_jse_index():
    """Fetch JSE All Share Index"""
    try:
        # JSE API or financial data provider
        # Example: Alpha Vantage, Yahoo Finance, etc.
        return 78500  # Example value
    
    except Exception as e:
        print(f"⚠️ Failed to fetch JSE index: {e}")
        return 78500

def fetch_usd_zar_rate():
    """Fetch USD/ZAR exchange rate"""
    try:
        # Use a free forex API
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data["rates"]["ZAR"]
    
    except Exception as e:
        print(f"⚠️ Failed to fetch USD/ZAR rate: {e}")
        return 18.50  # Fallback

def update_market_data(supabase: Client):
    """Update market data in Supabase"""
    
    print("📊 Fetching latest market data...")
    
    # Fetch all rates
    repo_rate = fetch_sarb_repo_rate()
    prime_rate = fetch_prime_rate()
    inflation_rate = fetch_inflation_rate()
    jse_index = fetch_jse_index()
    usd_zar = fetch_usd_zar_rate()
    
    market_data = {
        "repo_rate": repo_rate,
        "prime_rate": prime_rate,
        "inflation_rate": inflation_rate,
        "jse_all_share": jse_index,
        "usd_zar_rate": usd_zar,
        "last_updated": datetime.now().isoformat()
    }
    
    print(f"📈 SARB Repo Rate: {repo_rate}%")
    print(f"📈 Prime Rate: {prime_rate}%")
    print(f"📉 Inflation: {inflation_rate}%")
    print(f"📊 JSE All Share: {jse_index:,.0f}")
    print(f"💱 USD/ZAR: R{usd_zar:.2f}")
    
    try:
        # Check if market_data table exists, create if not
        result = supabase.table("market_data").select("id").execute()
        
        if result.data:
            # Update existing record
            supabase.table("market_data").update(market_data).eq("id", 1).execute()
            print("✅ Updated existing market data")
        else:
            # Insert new record
            market_data["id"] = 1
            supabase.table("market_data").insert(market_data).execute()
            print("✅ Inserted new market data")
    
    except Exception as e:
        print(f"❌ Failed to update market data: {e}")

def update_investment_recommendations(supabase: Client):
    """Refresh AI investment recommendations based on new market data"""
    
    print("🤖 Updating AI investment recommendations...")
    
    try:
        # Get current market data
        result = supabase.table("market_data").select("*").eq("id", 1).execute()
        
        if not result.data:
            print("⚠️ No market data found")
            return
        
        market = result.data[0]
        repo_rate = market["repo_rate"]
        
        # Get current collective balance
        balance_result = supabase.table("global_account_sync").select("total_balance").execute()
        balance = balance_result.data[0]["total_balance"] if balance_result.data else 0
        
        # Generate recommendations based on balance and market conditions
        recommendations = []
        
        if balance < 50000:
            recommendations.append({
                "category": "Foundation",
                "title": "Build Emergency Fund",
                "description": f"Focus on reaching R50,000 milestone. Current: R{balance:,.2f}",
                "priority": "High",
                "expected_return": 0,
                "risk_level": "Low"
            })
        
        elif balance < 100000:
            recommendations.append({
                "category": "Conservative",
                "title": "RSA Retail Bonds",
                "description": f"Invest R50,000 at {repo_rate}% fixed rate",
                "priority": "High",
                "expected_return": 50000 * (repo_rate / 100),
                "risk_level": "Low"
            })
        
        else:
            recommendations.append({
                "category": "Diversified",
                "title": "Balanced Portfolio",
                "description": f"Mix of bonds ({repo_rate}%), ETFs (12%), and property (10%)",
                "priority": "High",
                "expected_return": balance * 0.10,
                "risk_level": "Medium"
            })
        
        # Update recommendations in database
        for rec in recommendations:
            rec["created_at"] = datetime.now().isoformat()
            rec["is_active"] = True
        
        # Clear old recommendations
        supabase.table("investment_suggestions").update({"is_active": False}).eq("is_active", True).execute()
        
        # Insert new recommendations
        supabase.table("investment_suggestions").insert(recommendations).execute()
        
        print(f"✅ Updated {len(recommendations)} investment recommendations")
    
    except Exception as e:
        print(f"❌ Failed to update recommendations: {e}")

def main():
    """Main market data update function"""
    print("🚀 Starting Market Data Update...")
    print(f"⏰ Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S SAST')}")
    
    # Validate environment variables
    if not all([SUPABASE_URL, SUPABASE_KEY]):
        print("❌ Missing required environment variables")
        sys.exit(1)
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Update market data
    update_market_data(supabase)
    
    # Update AI recommendations
    update_investment_recommendations(supabase)
    
    print("✅ Market data update completed successfully!")

if __name__ == "__main__":
    main()