"""
Mock Data Generator for Review Mode
Generates realistic test data for 20 members without requiring live bank API
"""

from datetime import datetime, timedelta
import random

# 20 Member profiles with realistic SA names
MOCK_MEMBERS = [
    {"id": 1, "username": "admin_khula", "full_name": "Admin User", "role": "admin"},
    {"id": 2, "username": "thabo_mthembu", "full_name": "Thabo Mthembu", "role": "member"},
    {"id": 3, "username": "nomsa_dlamini", "full_name": "Nomsa Dlamini", "role": "member"},
    {"id": 4, "username": "sipho_khumalo", "full_name": "Sipho Khumalo", "role": "member"},
    {"id": 5, "username": "zanele_ndlovu", "full_name": "Zanele Ndlovu", "role": "member"},
    {"id": 6, "username": "mandla_zulu", "full_name": "Mandla Zulu", "role": "member"},
    {"id": 7, "username": "lindiwe_nkosi", "full_name": "Lindiwe Nkosi", "role": "member"},
    {"id": 8, "username": "bongani_mokoena", "full_name": "Bongani Mokoena", "role": "member"},
    {"id": 9, "username": "precious_mahlangu", "full_name": "Precious Mahlangu", "role": "member"},
    {"id": 10, "username": "tshepo_molefe", "full_name": "Tshepo Molefe", "role": "member"},
    {"id": 11, "username": "nandi_buthelezi", "full_name": "Nandi Buthelezi", "role": "member"},
    {"id": 12, "username": "sello_radebe", "full_name": "Sello Radebe", "role": "member"},
    {"id": 13, "username": "thandi_ngcobo", "full_name": "Thandi Ngcobo", "role": "member"},
    {"id": 14, "username": "mpho_sithole", "full_name": "Mpho Sithole", "role": "member"},
    {"id": 15, "username": "lerato_mabaso", "full_name": "Lerato Mabaso", "role": "member"},
    {"id": 16, "username": "jabu_shabalala", "full_name": "Jabu Shabalala", "role": "member"},
    {"id": 17, "username": "nokuthula_cele", "full_name": "Nokuthula Cele", "role": "member"},
    {"id": 18, "username": "vusi_dube", "full_name": "Vusi Dube", "role": "member"},
    {"id": 19, "username": "zinhle_mkhize", "full_name": "Zinhle Mkhize", "role": "member"},
    {"id": 20, "username": "andile_ntuli", "full_name": "Andile Ntuli", "role": "member"},
    {"id": 21, "username": "busisiwe_gumede", "full_name": "Busisiwe Gumede", "role": "member"},
]

def generate_mock_contributions():
    """Generate 14 months of contribution data (Jan 2025 - Feb 2026)"""
    contributions = []
    start_date = datetime(2025, 1, 1)
    
    for month_offset in range(14):
        current_date = start_date + timedelta(days=30 * month_offset)
        month_str = current_date.strftime("%Y-%m")
        
        for member in MOCK_MEMBERS:
            if member["role"] == "admin":
                continue  # Admin doesn't contribute
            
            # 90% payment compliance - some members miss payments
            payment_probability = 0.90
            
            if random.random() < payment_probability:
                status = "Received"
                payment_date = current_date + timedelta(days=random.randint(1, 25))
            else:
                status = "Pending"
                payment_date = None
            
            contributions.append({
                "user_id": member["id"],
                "username": member["username"],
                "full_name": member["full_name"],
                "month": month_str,
                "amount": 300,
                "status": status,
                "payment_date": payment_date.strftime("%Y-%m-%d") if payment_date else None
            })
    
    return contributions

def calculate_mock_balance():
    """Calculate total balance from mock contributions"""
    contributions = generate_mock_contributions()
    total = sum(c["amount"] for c in contributions if c["status"] == "Received")
    return total

def get_mock_member_stats(user_id):
    """Get individual member statistics"""
    contributions = generate_mock_contributions()
    member_contribs = [c for c in contributions if c["user_id"] == user_id]
    
    total_paid = sum(c["amount"] for c in member_contribs if c["status"] == "Received")
    total_pending = sum(c["amount"] for c in member_contribs if c["status"] == "Pending")
    months_paid = len([c for c in member_contribs if c["status"] == "Received"])
    
    return {
        "total_paid": total_paid,
        "total_pending": total_pending,
        "months_paid": months_paid,
        "total_months": len(member_contribs),
        "compliance_rate": (months_paid / len(member_contribs) * 100) if member_contribs else 0
    }

def get_mock_leaderboard():
    """Get top 5 contributors"""
    leaderboard = []
    
    for member in MOCK_MEMBERS:
        if member["role"] == "admin":
            continue
        
        stats = get_mock_member_stats(member["id"])
        leaderboard.append({
            "username": member["username"],
            "full_name": member["full_name"],
            "total_paid": stats["total_paid"],
            "compliance_rate": stats["compliance_rate"]
        })
    
    # Sort by total paid, then by compliance rate
    leaderboard.sort(key=lambda x: (x["total_paid"], x["compliance_rate"]), reverse=True)
    
    return leaderboard[:5]

def get_mock_monthly_totals():
    """Get monthly collection totals"""
    contributions = generate_mock_contributions()
    monthly_totals = {}
    
    for contrib in contributions:
        if contrib["status"] == "Received":
            month = contrib["month"]
            if month not in monthly_totals:
                monthly_totals[month] = 0
            monthly_totals[month] += contrib["amount"]
    
    # Convert to list format
    result = []
    for month, total in sorted(monthly_totals.items()):
        year, month_num = month.split("-")
        result.append({
            "year": int(year),
            "month": int(month_num),
            "total": total
        })
    
    return result

def get_mock_investment_opportunities():
    """Get mock investment opportunities with votes"""
    opportunities = [
        {
            "id": 1,
            "title": "Load Shedding Inverter Installation",
            "description": "Install and maintain inverter systems for homes and businesses",
            "investment": 72000,
            "annual_return": 444000,
            "roi_percentage": 652,
            "risk_level": "Medium",
            "category": "Crisis Solution",
            "votes_for": 15,
            "votes_against": 3,
            "total_votes": 18
        },
        {
            "id": 2,
            "title": "Borehole Drilling Service",
            "description": "Drill boreholes for water-scarce communities",
            "investment": 72000,
            "annual_return": 1380000,
            "roi_percentage": 1523,
            "risk_level": "Medium",
            "category": "Water Crisis",
            "votes_for": 12,
            "votes_against": 5,
            "total_votes": 17
        },
        {
            "id": 3,
            "title": "Cannabis Cultivation",
            "description": "Legal cannabis farming for medicinal purposes",
            "investment": 55000,
            "annual_return": 460000,
            "roi_percentage": 736,
            "risk_level": "Medium",
            "category": "Agriculture",
            "votes_for": 8,
            "votes_against": 9,
            "total_votes": 17
        },
        {
            "id": 4,
            "title": "RSA Retail Bonds",
            "description": "Government-backed bonds with guaranteed returns",
            "investment": 50000,
            "annual_return": 4125,
            "roi_percentage": 8.25,
            "risk_level": "Low",
            "category": "Conservative",
            "votes_for": 18,
            "votes_against": 1,
            "total_votes": 19
        },
        {
            "id": 5,
            "title": "Satrix Top 40 ETF",
            "description": "Diversified JSE Top 40 index fund",
            "investment": 50000,
            "annual_return": 6750,
            "roi_percentage": 13.5,
            "risk_level": "Medium",
            "category": "Stock Market",
            "votes_for": 16,
            "votes_against": 2,
            "total_votes": 18
        }
    ]
    
    return opportunities

def get_mock_market_data():
    """Get current SA market data"""
    return {
        "repo_rate": 8.25,
        "prime_rate": 11.75,
        "inflation_rate": 5.2,
        "jse_all_share": 78500,
        "usd_zar_rate": 18.50,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_mock_member_votes(user_id):
    """Get votes cast by a specific member"""
    # Simulate some random votes
    opportunities = get_mock_investment_opportunities()
    votes = []
    
    for opp in opportunities[:3]:  # Member voted on first 3 opportunities
        votes.append({
            "suggestion_id": opp["id"],
            "vote_type": "For" if random.random() > 0.3 else "Against"
        })
    
    return votes

# Export functions
__all__ = [
    'MOCK_MEMBERS',
    'generate_mock_contributions',
    'calculate_mock_balance',
    'get_mock_member_stats',
    'get_mock_leaderboard',
    'get_mock_monthly_totals',
    'get_mock_investment_opportunities',
    'get_mock_market_data',
    'get_mock_member_votes'
]