import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sqlite3
import hashlib
import os

# ============================================================
# KHULA COLLECTIVE - THE APP YOUR MEMBERS DESERVE
# ============================================================

st.set_page_config(
    page_title="Khula Collective 💰",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# STYLING
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
        font-family: 'Inter', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .balance-hero {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 50%, #0984e3 100%);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        margin: 10px 0 30px 0;
        box-shadow: 0 20px 60px rgba(0, 184, 148, 0.3);
        position: relative;
        overflow: hidden;
    }
    .balance-hero::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: pulse 4s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    .balance-label {
        color: rgba(255,255,255,0.85);
        font-size: 16px; font-weight: 500;
        letter-spacing: 3px; text-transform: uppercase;
        margin-bottom: 8px;
    }
    .balance-amount {
        color: #ffffff;
        font-size: 72px; font-weight: 900;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin: 10px 0; line-height: 1;
    }
    .balance-sub {
        color: rgba(255,255,255,0.8);
        font-size: 16px; font-weight: 400;
    }
    .balance-growth {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 6px 16px; border-radius: 20px;
        color: #fff; font-weight: 600; font-size: 14px;
        margin-top: 12px;
    }
    
    .section-header {
        color: #ffffff;
        font-size: 24px; font-weight: 700;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(0, 184, 148, 0.3);
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1e1e30 0%, #2a2a40 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px; text-align: center;
    }
    .stat-number {
        font-size: 36px; font-weight: 800;
        background: linear-gradient(135deg, #00b894, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
    }
    .stat-label {
        color: rgba(255,255,255,0.6);
        font-size: 13px; font-weight: 500;
        text-transform: uppercase; letter-spacing: 1px;
    }
    
    .member-paid {
        background: linear-gradient(135deg, #1a3a2a 0%, #1e4d35 100%);
        border: 1px solid #00b894;
        border-radius: 12px;
        padding: 14px 16px; margin: 6px 0;
        display: flex; align-items: center; justify-content: space-between;
    }
    .member-unpaid {
        background: linear-gradient(135deg, #3a1a1a 0%, #4d1e1e 100%);
        border: 1px solid #e74c3c;
        border-radius: 12px;
        padding: 14px 16px; margin: 6px 0;
        display: flex; align-items: center; justify-content: space-between;
    }
    .member-name { color: #ffffff; font-weight: 600; font-size: 15px; }
    .paid-amount { color: #00b894; font-weight: 700; font-size: 15px; }
    .unpaid-amount { color: #e74c3c; font-weight: 700; font-size: 15px; }
    
    .invest-card {
        background: linear-gradient(135deg, #1e1e30 0%, #2a2a40 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px; margin: 12px 0;
    }
    .invest-card:hover { border-color: #00b894; }
    .invest-title { color: #ffffff; font-size: 20px; font-weight: 700; margin-bottom: 8px; }
    .invest-roi {
        display: inline-block;
        background: linear-gradient(135deg, #00b894, #00cec9);
        padding: 4px 14px; border-radius: 20px;
        color: #fff; font-weight: 700; font-size: 14px; margin: 8px 4px;
    }
    .invest-desc { color: rgba(255,255,255,0.7); font-size: 14px; line-height: 1.6; }
    .invest-risk {
        display: inline-block;
        padding: 3px 10px; border-radius: 8px;
        font-size: 12px; font-weight: 600; margin: 8px 4px;
    }
    .risk-low { background: rgba(0,184,148,0.2); color: #00b894; }
    .risk-medium { background: rgba(253,203,110,0.2); color: #fdcb6e; }
    .risk-high { background: rgba(231,76,60,0.2); color: #e74c3c; }
    
    .txn-row {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 12px 16px; margin: 4px 0;
        display: flex; justify-content: space-between; align-items: center;
        border-left: 3px solid #00b894;
    }
    .txn-date { color: rgba(255,255,255,0.5); font-size: 13px; }
    .txn-name { color: #ffffff; font-weight: 600; font-size: 14px; }
    .txn-amount { color: #00b894; font-weight: 700; font-size: 15px; }
    
    .logo-text {
        font-size: 28px; font-weight: 900;
        background: linear-gradient(135deg, #00b894, #00cec9, #0984e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .logo-sub {
        color: rgba(255,255,255,0.5);
        font-size: 12px; letter-spacing: 4px; text-transform: uppercase;
    }
    
    .progress-outer {
        background: rgba(255,255,255,0.08);
        border-radius: 12px; height: 24px; overflow: hidden; margin: 12px 0;
    }
    .progress-inner {
        height: 100%; border-radius: 12px;
        background: linear-gradient(90deg, #00b894, #00cec9, #0984e3);
        display: flex; align-items: center; justify-content: center;
        font-size: 12px; font-weight: 700; color: #fff;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00b894, #0984e3) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 10px 24px !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,184,148,0.4) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background: rgba(30,30,48,0.8);
        border-radius: 12px; padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; color: rgba(255,255,255,0.6); font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00b894, #0984e3);
        color: white !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE FUNCTIONS - Matching REAL schema
# ============================================================

def get_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'khula_collective.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user['password_hash'] == hash_password(password):
        return dict(user)
    return None

def get_total_balance():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM Monthly_Contributions WHERE status = 'Paid'")
    total = cursor.fetchone()['total']
    if total == 0:
        cursor.execute("SELECT total_balance FROM GlobalAccountSync LIMIT 1")
        row = cursor.fetchone()
        total = row['total_balance'] if row else 0
    conn.close()
    return float(total)

def get_all_members():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE is_admin = 0 ORDER BY first_name, surname")
    members = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return members

def get_monthly_totals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT year, month, 
               SUM(amount) as total,
               COUNT(DISTINCT user_id) as members_paid
        FROM Monthly_Contributions
        WHERE status = 'Paid'
        GROUP BY year, month
        ORDER BY year, month
    """)
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def get_current_month_payments():
    now = datetime.now()
    current_month = now.month
    current_year = now.year
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, first_name, surname FROM Users WHERE is_admin = 0 ORDER BY first_name, surname")
    members = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("""
        SELECT user_id, SUM(amount) as paid
        FROM Monthly_Contributions
        WHERE month = ? AND year = ? AND status = 'Paid'
        GROUP BY user_id
    """, (current_month, current_year))
    payments = {row['user_id']: row['paid'] for row in cursor.fetchall()}
    
    conn.close()
    
    paid = []
    unpaid = []
    for m in members:
        m['full_name'] = f"{m['first_name']} {m['surname']}"
        if m['user_id'] in payments:
            m['amount_paid'] = payments[m['user_id']]
            paid.append(m)
        else:
            m['amount_paid'] = 0
            unpaid.append(m)
    
    return paid, unpaid

def get_member_totals():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.user_id, u.first_name, u.surname, u.username,
               COALESCE(SUM(mc.amount), 0) as total_contributed,
               COUNT(mc.contribution_id) as months_paid
        FROM Users u
        LEFT JOIN Monthly_Contributions mc ON u.user_id = mc.user_id AND mc.status = 'Paid'
        WHERE u.is_admin = 0
        GROUP BY u.user_id
        ORDER BY total_contributed DESC
    """)
    data = [dict(row) for row in cursor.fetchall()]
    for d in data:
        d['full_name'] = f"{d['first_name']} {d['surname']}"
    conn.close()
    return data

def get_recent_deposits(limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT mc.payment_date, mc.amount, mc.payment_reference, mc.month, mc.year,
               u.first_name, u.surname
        FROM Monthly_Contributions mc
        JOIN Users u ON mc.user_id = u.user_id
        WHERE mc.status = 'Paid'
        ORDER BY mc.payment_date DESC
        LIMIT ?
    """, (limit,))
    data = [dict(row) for row in cursor.fetchall()]
    for d in data:
        d['full_name'] = f"{d['first_name']} {d['surname']}"
    conn.close()
    return data

def get_member_contributions(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Monthly_Contributions 
        WHERE user_id = ? AND status = 'Paid'
        ORDER BY year DESC, month DESC
    """, (user_id,))
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data


# ============================================================
# INVESTMENT OPPORTUNITIES
# ============================================================

INVESTMENTS = [
    {
        "name": "🔌 Load Shedding Inverter Installation Business",
        "cat": "Energy Crisis", "cost": 60000,
        "revenue": "R37,000/month", "roi": "652%", "risk": "Low", "risk_pct": 15,
        "desc": "Install inverter + battery systems in homes and businesses. SA has 30M+ households desperate for backup power. Buy inverters wholesale from China at R4,500, install for R15,000-R25,000. 3 installations per week = R37k/month.",
        "why": "Load shedding is getting WORSE. Every household needs this. Market is R50 BILLION and growing.",
        "action": "Register company → Import 10 inverter kits → Hire 1 electrician → Start marketing on Facebook Marketplace"
    },
    {
        "name": "💧 Borehole Drilling & Water Solutions",
        "cat": "Water Crisis", "cost": 85000,
        "revenue": "R115,000/month", "roi": "1,523%", "risk": "Medium", "risk_pct": 30,
        "desc": "Municipal water is failing across SA. Drill boreholes for homes, farms, and businesses. One borehole costs R8k to drill, charge R25k-R45k. JoJo tank installations as add-on revenue.",
        "why": "Cape Town, Gauteng, KZN all facing water crises. Municipalities are collapsing. This is a 20-year opportunity.",
        "action": "Buy drilling equipment → Get water use license → Target estates and farms → Partner with plumbers"
    },
    {
        "name": "🌿 Cannabis Cultivation (Legal)",
        "cat": "New Legal Market", "cost": 55000,
        "revenue": "R38,000/month", "roi": "736%", "risk": "Medium", "risk_pct": 35,
        "desc": "Cannabis is now legal for private use in SA. Grow premium indoor cannabis. 4 harvests per year, each producing 2-4kg. Sell to dispensaries and private buyers at R80-R120/gram.",
        "why": "New Cannabis for Private Purposes Act 2024. First movers will dominate. R28 BILLION market opportunity.",
        "action": "Set up indoor grow room → Source genetics → First harvest in 10-12 weeks → Build buyer network"
    },
    {
        "name": "🕳️ Pothole Repair & Road Maintenance",
        "cat": "Municipal Failure", "cost": 45000,
        "revenue": "R42,000/month", "roi": "1,020%", "risk": "Low", "risk_pct": 12,
        "desc": "SA municipalities can't fix roads. Private companies and estates PAY for pothole repair. Cold asphalt mix costs R200/bag, fix one pothole for R1,500-R3,000. Fix 20 potholes/day.",
        "why": "Roads are getting worse every day. Body corporates, shopping centres, and private estates are desperate.",
        "action": "Buy bakkie + cold asphalt + compactor → Market to body corporates → Get municipal subcontracts"
    },
    {
        "name": "🧂 Spice & Food Import Replacement",
        "cat": "Import Replacement", "cost": 40000,
        "revenue": "R65,000/month", "roi": "1,850%", "risk": "Low", "risk_pct": 18,
        "desc": "SA imports R2.1 BILLION in spices annually. Blend and package locally at 70% less cost. Supply spaza shops, restaurants, and supermarkets. Margins of 300-400%.",
        "why": "Weak Rand makes imports expensive. Local production is 70% cheaper. Massive untapped market.",
        "action": "Source raw spices in bulk → Set up blending facility → Register with health dept → Supply local shops"
    },
    {
        "name": "❄️ Mobile Cold Storage",
        "cat": "Agriculture", "cost": 70000,
        "revenue": "R28,000/month", "roi": "380%", "risk": "Low", "risk_pct": 20,
        "desc": "SA loses 30% of fresh produce due to lack of cold storage. Convert shipping containers into mobile cold rooms. Rent to farmers, caterers, and event companies at R800-R1,500/day.",
        "why": "Post-harvest losses cost SA R61 BILLION/year. Farmers are desperate for affordable cold storage.",
        "action": "Buy used container → Install refrigeration unit → Market to farmers markets and events"
    },
    {
        "name": "🏠 RSA Retail Savings Bonds",
        "cat": "Safe Investment", "cost": 50000,
        "revenue": "R344/month", "roi": "8.25%", "risk": "Very Low", "risk_pct": 2,
        "desc": "Government-backed bonds. Zero risk. Fixed 8.25% return for 5 years. R50,000 invested = R4,125/year guaranteed. Can invest up to R5 million. Tax-free up to R23,800/year.",
        "why": "Interest rates are high. Lock in 8.25% before rates drop. 100% guaranteed by SA government.",
        "action": "Open RSA Retail Bonds account online → Invest R50,000 → Earn R344/month guaranteed"
    },
    {
        "name": "📈 Satrix Top 40 ETF",
        "cat": "Stock Market", "cost": 10000,
        "revenue": "Variable", "roi": "12-15%", "risk": "Medium", "risk_pct": 35,
        "desc": "Invest in SA's top 40 companies (Naspers, Anglo, FirstRand, etc.) through one ETF. Average 12-15% annual return over 10 years. Low fees (0.1%). Can start with R10,000.",
        "why": "JSE is undervalued. SA stocks are cheap compared to global markets. Great entry point.",
        "action": "Open EasyEquities account → Buy Satrix Top 40 → Set up monthly contributions"
    }
]


# ============================================================
# LOGIN SCREEN
# ============================================================

def show_login():
    st.markdown("""
    <div style="text-align: center; padding: 60px 0 30px 0;">
        <div class="logo-text">💰 KHULA COLLECTIVE</div>
        <div class="logo-sub">Building Wealth Together</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e30, #2a2a40); 
                    border-radius: 20px; padding: 40px; 
                    border: 1px solid rgba(255,255,255,0.08);
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);">
            <h3 style="color: #fff; text-align: center; margin-bottom: 5px;">Welcome Back</h3>
            <p style="color: rgba(255,255,255,0.5); text-align: center; font-size: 14px;">Sign in to view your collective</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("🔓 Sign In", use_container_width=True):
            user = authenticate(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; color: rgba(255,255,255,0.4); font-size: 13px;">
            <strong>Demo Access:</strong><br>
            Admin: admin_khula / admin123<br>
            Member: thabo_mthembu / password123
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_dashboard():
    user = st.session_state['user']
    full_name = f"{user['first_name']} {user['surname']}"
    is_admin = user['is_admin'] == 1
    
    # Top Bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 16px; padding: 10px 0;">
            <div class="logo-text">💰 KHULA COLLECTIVE</div>
            <div style="color: rgba(255,255,255,0.4);">|</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 14px;">Welcome, <strong style="color: #00b894;">{full_name}</strong></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # ========== THE BIG NUMBER ==========
    total_balance = get_total_balance()
    monthly_totals = get_monthly_totals()
    members = get_all_members()
    total_members = len(members)
    
    # Growth calc
    if len(monthly_totals) >= 2:
        last = monthly_totals[-1]['total']
        prev = monthly_totals[-2]['total']
        growth = last - prev
        growth_pct = (growth / prev * 100) if prev > 0 else 0
    else:
        growth = 0
        growth_pct = 0
    
    st.markdown(f"""
    <div class="balance-hero">
        <div class="balance-label">💰 FNB Collective Account Balance</div>
        <div class="balance-amount">R{total_balance:,.2f}</div>
        <div class="balance-sub">{total_members} members contributing R300/month</div>
        <div class="balance-growth">📈 +R{growth:,.0f} last month ({growth_pct:+.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== QUICK STATS ==========
    paid_this_month, unpaid_this_month = get_current_month_payments()
    months_active = len(monthly_totals)
    avg_monthly = total_balance / months_active if months_active > 0 else 0
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-label">Members</div>
            <div class="stat-number">{total_members}</div>
            <div class="stat-label">Active Contributors</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        compliance = (len(paid_this_month)/total_members*100) if total_members > 0 else 0
        st.markdown(f"""<div class="stat-card">
            <div class="stat-label">Paid This Month</div>
            <div class="stat-number">{len(paid_this_month)}/{total_members}</div>
            <div class="stat-label">{compliance:.0f}% Compliance</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-label">Months Active</div>
            <div class="stat-number">{months_active}</div>
            <div class="stat-label">Since Jan 2025</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-card">
            <div class="stat-label">Avg Monthly</div>
            <div class="stat-number">R{avg_monthly:,.0f}</div>
            <div class="stat-label">Collective Deposits</div>
        </div>""", unsafe_allow_html=True)
    
    # ========== TABS ==========
    if is_admin:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Dashboard", "✅ Payment Tracker", "🏆 Leaderboard",
            "💡 Investments", "🏦 Bank Deposits", "⚙️ Admin"
        ])
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", "✅ Payment Tracker", "🏆 Leaderboard",
            "💡 Investments", "🏦 Bank Deposits"
        ])
    
    # ========== TAB 1: DASHBOARD ==========
    with tab1:
        st.markdown('<div class="section-header">📈 Collective Pot Growth</div>', unsafe_allow_html=True)
        
        if monthly_totals:
            df = pd.DataFrame(monthly_totals)
            month_labels = []
            for _, row in df.iterrows():
                try:
                    dt = datetime(int(row['year']), int(row['month']), 1)
                    month_labels.append(dt.strftime('%b %Y'))
                except:
                    month_labels.append(f"{row['month']}/{row['year']}")
            df['label'] = month_labels
            df['cumulative'] = df['total'].cumsum()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['label'], y=df['cumulative'],
                fill='tozeroy', fillcolor='rgba(0, 184, 148, 0.15)',
                line=dict(color='#00b894', width=3),
                name='Total Balance',
                hovertemplate='<b>%{x}</b><br>Balance: R%{y:,.0f}<extra></extra>'
            ))
            fig.add_trace(go.Bar(
                x=df['label'], y=df['total'],
                name='Monthly Deposits',
                marker_color='rgba(9, 132, 227, 0.6)',
                hovertemplate='<b>%{x}</b><br>Deposits: R%{y:,.0f}<extra></extra>'
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='rgba(255,255,255,0.7)', family='Inter'),
                height=400, margin=dict(l=20, r=20, t=20, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickangle=-45),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickprefix='R', tickformat=',.'),
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Target Progress
        yearly_target = total_members * 300 * 12
        progress_pct = min((total_balance / yearly_target) * 100, 100) if yearly_target > 0 else 0
        
        st.markdown(f'<div class="section-header">🎯 Yearly Target: R{yearly_target:,.0f}</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="progress-outer">
            <div class="progress-inner" style="width: {progress_pct}%">{progress_pct:.1f}%</div>
        </div>
        <div style="color: rgba(255,255,255,0.5); font-size: 13px; text-align: center;">
            R{total_balance:,.0f} of R{yearly_target:,.0f} — R{max(0, yearly_target - total_balance):,.0f} remaining
        </div>
        """, unsafe_allow_html=True)
        
        # Members per month chart
        if monthly_totals:
            st.markdown('<div class="section-header">👥 Members Paying Each Month</div>', unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df['label'], y=df['members_paid'],
                marker_color=['#00b894' if mp >= total_members * 0.8 else '#fdcb6e' if mp >= total_members * 0.5 else '#e74c3c' for mp in df['members_paid']],
                hovertemplate='<b>%{x}</b><br>Members: %{y}<extra></extra>'
            ))
            fig2.add_hline(y=total_members, line_dash="dash", line_color="rgba(255,255,255,0.3)",
                          annotation_text=f"Target: {total_members}", annotation_font_color="rgba(255,255,255,0.5)")
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='rgba(255,255,255,0.7)', family='Inter'),
                height=300, margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickangle=-45),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Members')
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Personal summary for non-admin
        if not is_admin:
            st.markdown('<div class="section-header">👤 Your Contribution History</div>', unsafe_allow_html=True)
            my_contributions = get_member_contributions(user['user_id'])
            if my_contributions:
                my_total = sum(c['amount'] for c in my_contributions)
                my_months = len(my_contributions)
                st.markdown(f"""
                <div class="stat-card" style="margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-around;">
                        <div>
                            <div class="stat-label">Your Total</div>
                            <div class="stat-number">R{my_total:,.0f}</div>
                        </div>
                        <div>
                            <div class="stat-label">Months Paid</div>
                            <div class="stat-number">{my_months}</div>
                        </div>
                        <div>
                            <div class="stat-label">Your Share</div>
                            <div class="stat-number">{(my_total/total_balance*100) if total_balance > 0 else 0:.1f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Monthly payment grid
                month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                paid_months = {(c['year'], c['month']) for c in my_contributions}
                
                for year in sorted(set(c['year'] for c in my_contributions), reverse=True):
                    st.markdown(f"**{year}**")
                    cols = st.columns(12)
                    for i, col in enumerate(cols):
                        m = i + 1
                        with col:
                            if (year, m) in paid_months:
                                st.markdown(f"<div style='text-align:center;background:#1a3a2a;border:1px solid #00b894;border-radius:8px;padding:6px;'><div style='color:#00b894;font-size:10px;'>{month_names[i]}</div><div style='color:#00b894;font-size:14px;'>✅</div></div>", unsafe_allow_html=True)
                            else:
                                now = datetime.now()
                                if year > now.year or (year == now.year and m > now.month):
                                    st.markdown(f"<div style='text-align:center;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:8px;padding:6px;'><div style='color:rgba(255,255,255,0.3);font-size:10px;'>{month_names[i]}</div><div style='color:rgba(255,255,255,0.2);font-size:14px;'>—</div></div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div style='text-align:center;background:#3a1a1a;border:1px solid #e74c3c;border-radius:8px;padding:6px;'><div style='color:#e74c3c;font-size:10px;'>{month_names[i]}</div><div style='color:#e74c3c;font-size:14px;'>❌</div></div>", unsafe_allow_html=True)
            else:
                st.info("No contributions recorded yet.")
    
    # ========== TAB 2: PAYMENT TRACKER ==========
    with tab2:
        now = datetime.now()
        st.markdown(f'<div class="section-header">✅ {now.strftime("%B %Y")} Payment Status</div>', unsafe_allow_html=True)
        
        total_paid_amount = sum(m['amount_paid'] for m in paid_this_month)
        expected = total_members * 300
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="stat-card">
                <div style="font-size: 40px;">✅</div>
                <div class="stat-number">{len(paid_this_month)}</div>
                <div class="stat-label">Members Paid</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="stat-card">
                <div style="font-size: 40px;">❌</div>
                <div class="stat-number" style="background: linear-gradient(135deg, #e74c3c, #fd79a8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{len(unpaid_this_month)}</div>
                <div class="stat-label">Still Outstanding</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="stat-card">
                <div style="font-size: 40px;">💰</div>
                <div class="stat-number">R{total_paid_amount:,.0f}</div>
                <div class="stat-label">of R{expected:,.0f} Expected</div>
            </div>""", unsafe_allow_html=True)
        
        month_pct = (total_paid_amount / expected * 100) if expected > 0 else 0
        bar_bg = 'linear-gradient(90deg, #00b894, #00cec9)' if month_pct >= 80 else 'linear-gradient(90deg, #fdcb6e, #e17055)' if month_pct >= 50 else 'linear-gradient(90deg, #e74c3c, #fd79a8)'
        st.markdown(f"""
        <div class="progress-outer">
            <div class="progress-inner" style="width: {month_pct}%; background: {bar_bg};">{month_pct:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        col_paid, col_unpaid = st.columns(2)
        
        with col_paid:
            st.markdown(f"### ✅ Paid ({len(paid_this_month)})")
            for m in paid_this_month:
                st.markdown(f"""<div class="member-paid">
                    <span class="member-name">✅ {m['full_name']}</span>
                    <span class="paid-amount">R{m['amount_paid']:,.0f}</span>
                </div>""", unsafe_allow_html=True)
            if not paid_this_month:
                st.markdown("<div style='color:rgba(255,255,255,0.4);text-align:center;padding:20px;'>No payments yet this month</div>", unsafe_allow_html=True)
        
        with col_unpaid:
            st.markdown(f"### ❌ Outstanding ({len(unpaid_this_month)})")
            if unpaid_this_month:
                for m in unpaid_this_month:
                    st.markdown(f"""<div class="member-unpaid">
                        <span class="member-name">❌ {m['full_name']}</span>
                        <span class="unpaid-amount">R300 due</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div style="text-align: center; padding: 40px; color: #00b894;">
                    <div style="font-size: 48px;">🎉</div>
                    <div style="font-size: 18px; font-weight: 700;">Everyone has paid!</div>
                </div>""", unsafe_allow_html=True)
    
    # ========== TAB 3: LEADERBOARD ==========
    with tab3:
        st.markdown('<div class="section-header">🏆 Contribution Leaderboard</div>', unsafe_allow_html=True)
        
        member_totals = get_member_totals()
        medals = ['🥇', '🥈', '🥉']
        
        for i, m in enumerate(member_totals):
            rank = medals[i] if i < 3 else f"#{i+1}"
            consistency = (m['months_paid'] / months_active * 100) if months_active > 0 else 0
            
            bg = "rgba(0, 184, 148, 0.08)" if i < 3 else "rgba(255,255,255,0.03)"
            border = "1px solid rgba(0, 184, 148, 0.3)" if i < 3 else "1px solid rgba(255,255,255,0.05)"
            
            st.markdown(f"""
            <div style="background: {bg}; border: {border}; border-radius: 12px; padding: 14px 18px; margin: 6px 0; display: flex; align-items: center; gap: 14px;">
                <div style="font-size: 24px; width: 40px; text-align: center;">{rank}</div>
                <div style="flex: 1;">
                    <div style="color: #ffffff; font-weight: 600; font-size: 15px;">{m['full_name']}</div>
                    <div style="color: rgba(255,255,255,0.4); font-size: 12px;">{m['months_paid']} months paid • {consistency:.0f}% consistency</div>
                </div>
                <div style="color: #00b894; font-weight: 700; font-size: 16px;">R{m['total_contributed']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Chart
        st.markdown('<div class="section-header">📊 Contribution Distribution</div>', unsafe_allow_html=True)
        df_l = pd.DataFrame(member_totals[:10])
        if not df_l.empty:
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                x=df_l['full_name'], y=df_l['total_contributed'],
                marker_color=['#00b894' if i < 3 else '#0984e3' if i < 7 else '#636e72' for i in range(len(df_l))],
                hovertemplate='<b>%{x}</b><br>Total: R%{y:,.0f}<extra></extra>'
            ))
            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='rgba(255,255,255,0.7)', family='Inter'),
                height=350, margin=dict(l=20, r=20, t=20, b=80),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickangle=-45),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickprefix='R', tickformat=',.')
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    # ========== TAB 4: INVESTMENTS ==========
    with tab4:
        st.markdown(f'<div class="section-header">💡 What Can We Do With R{total_balance:,.0f}?</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e1e30, #2a2a40); border-radius: 16px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(0,184,148,0.2);">
            <div style="color: #00b894; font-weight: 700; font-size: 16px;">💰 Our Collective Pot: R{total_balance:,.0f}</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 14px; margin-top: 8px;">
                With {total_members} members contributing R300/month, we add R{total_members * 300:,.0f} every month. 
                Every crisis in South Africa is an opportunity for us.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        affordable = [o for o in INVESTMENTS if o['cost'] <= total_balance]
        stretch = [o for o in INVESTMENTS if o['cost'] > total_balance]
        
        if affordable:
            st.markdown("### 🟢 We Can Start NOW")
            for opp in affordable:
                rc = 'risk-low' if opp['risk_pct'] <= 20 else 'risk-medium' if opp['risk_pct'] <= 40 else 'risk-high'
                st.markdown(f"""
                <div class="invest-card">
                    <div class="invest-title">{opp['name']}</div>
                    <span class="invest-roi">📈 {opp['roi']} Annual ROI</span>
                    <span class="invest-risk {rc}">⚠️ Risk: {opp['risk_pct']}%</span>
                    <div class="invest-desc" style="margin-top: 12px;">
                        <strong>💰 Startup:</strong> R{opp['cost']:,} | <strong>📊 Revenue:</strong> {opp['revenue']}<br><br>
                        {opp['desc']}<br><br>
                        <strong>🔥 Why Now:</strong> {opp['why']}<br><br>
                        <strong>📋 Action Plan:</strong> {opp['action']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if stretch:
            st.markdown("### 🟡 Save A Bit More For These")
            for opp in stretch:
                months_needed = max(1, int((opp['cost'] - total_balance) / (total_members * 300)) + 1)
                rc = 'risk-low' if opp['risk_pct'] <= 20 else 'risk-medium' if opp['risk_pct'] <= 40 else 'risk-high'
                st.markdown(f"""
                <div class="invest-card" style="opacity: 0.85;">
                    <div class="invest-title">{opp['name']}</div>
                    <span class="invest-roi">📈 {opp['roi']} Annual ROI</span>
                    <span class="invest-risk {rc}">⚠️ Risk: {opp['risk_pct']}%</span>
                    <span style="background: rgba(253,203,110,0.2); color: #fdcb6e; padding: 3px 10px; border-radius: 8px; font-size: 12px; font-weight: 600;">⏳ ~{months_needed} months away</span>
                    <div class="invest-desc" style="margin-top: 12px;">
                        <strong>💰 Startup:</strong> R{opp['cost']:,} | <strong>📊 Revenue:</strong> {opp['revenue']}<br><br>
                        {opp['desc']}<br><br>
                        <strong>🔥 Why Now:</strong> {opp['why']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Calculator
        st.markdown('<div class="section-header">🧮 Investment Calculator</div>', unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        with cc1:
            invest_amount = st.number_input("Investment Amount (R)", value=int(total_balance), step=5000)
            annual_return = st.slider("Expected Annual Return (%)", 5, 100, 25)
        with cc2:
            years = st.slider("Investment Period (Years)", 1, 10, 3)
            future_value = invest_amount * (1 + annual_return/100) ** years
            total_return = future_value - invest_amount
            per_member = total_return / total_members if total_members > 0 else 0
            
            st.markdown(f"""
            <div class="stat-card" style="margin-top: 10px;">
                <div class="stat-label">After {years} Years</div>
                <div class="stat-number">R{future_value:,.0f}</div>
                <div style="color: #00b894; font-size: 16px; font-weight: 600;">+R{total_return:,.0f} profit</div>
                <div style="color: rgba(255,255,255,0.5); font-size: 13px; margin-top: 8px;">= R{per_member:,.0f} per member</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========== TAB 5: BANK DEPOSITS ==========
    with tab5:
        st.markdown('<div class="section-header">🏦 Recent Bank Deposits</div>', unsafe_allow_html=True)
        
        recent = get_recent_deposits(50)
        
        if recent:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e1e30, #2a2a40); border-radius: 16px; padding: 20px; margin-bottom: 20px; border: 1px solid rgba(0,184,148,0.2);">
                <div style="color: rgba(255,255,255,0.6); font-size: 14px;">
                    Last {len(recent)} deposits into the FNB Collective Account. Each R300 deposit is a member's monthly contribution.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            for txn in recent:
                try:
                    dt = datetime.strptime(txn['payment_date'], '%Y-%m-%d')
                    date_str = dt.strftime('%d %b %Y')
                except:
                    date_str = str(txn['payment_date'])
                
                ref = txn.get('payment_reference', '') or ''
                st.markdown(f"""
                <div class="txn-row">
                    <div>
                        <div class="txn-name">{txn['full_name']}</div>
                        <div class="txn-date">{date_str} • {ref}</div>
                    </div>
                    <div class="txn-amount">+R{txn['amount']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Monthly summary
        st.markdown('<div class="section-header">📅 Monthly Deposit Summary</div>', unsafe_allow_html=True)
        
        if monthly_totals:
            for mt in reversed(monthly_totals):
                try:
                    dt = datetime(int(mt['year']), int(mt['month']), 1)
                    month_str = dt.strftime('%B %Y')
                except:
                    month_str = f"{mt['month']}/{mt['year']}"
                
                pct = (mt['members_paid'] / total_members * 100) if total_members > 0 else 0
                color = '#00b894' if pct >= 80 else '#fdcb6e' if pct >= 50 else '#e74c3c'
                
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); border-radius: 10px; padding: 14px 18px; margin: 4px 0; display: flex; justify-content: space-between; align-items: center; border-left: 3px solid {color};">
                    <div>
                        <div style="color: #ffffff; font-weight: 600; font-size: 15px;">{month_str}</div>
                        <div style="color: rgba(255,255,255,0.4); font-size: 12px;">{mt['members_paid']}/{total_members} members ({pct:.0f}%)</div>
                    </div>
                    <div style="color: #00b894; font-weight: 700; font-size: 16px;">R{mt['total']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # ========== TAB 6: ADMIN ==========
    if is_admin:
        with tab6:
            st.markdown('<div class="section-header">⚙️ Admin Panel</div>', unsafe_allow_html=True)
            
            # All members table
            st.markdown("### 👥 All Members")
            member_data = get_member_totals()
            
            admin_df = pd.DataFrame([{
                'Name': m['full_name'],
                'Username': m['username'],
                'Total Contributed': f"R{m['total_contributed']:,.0f}",
                'Months Paid': m['months_paid'],
                'Consistency': f"{(m['months_paid']/months_active*100) if months_active > 0 else 0:.0f}%"
            } for m in member_data])
            
            st.dataframe(admin_df, use_container_width=True, hide_index=True)
            
            # Export
            st.markdown("### 📥 Export Data")
            if st.button("📥 Download Member Report (CSV)"):
                csv_data = admin_df.to_csv(index=False)
                st.download_button(
                    label="💾 Save CSV",
                    data=csv_data,
                    file_name=f"khula_members_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            # Quick stats
            st.markdown("### 📊 Admin Stats")
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                perfect = sum(1 for m in member_data if m['months_paid'] == months_active)
                st.metric("Perfect Attendance", f"{perfect}/{total_members}")
            with ac2:
                avg_contrib = sum(m['total_contributed'] for m in member_data) / total_members if total_members > 0 else 0
                st.metric("Avg Contribution", f"R{avg_contrib:,.0f}")
            with ac3:
                total_possible = total_members * months_active * 300
                overall_rate = (total_balance / total_possible * 100) if total_possible > 0 else 0
                st.metric("Overall Collection Rate", f"{overall_rate:.1f}%")


# ============================================================
# MAIN
# ============================================================

def main():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        show_login()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()