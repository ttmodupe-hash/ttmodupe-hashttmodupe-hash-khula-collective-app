import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import hashlib
import os

# ============================================================
# KHULA COLLECTIVE - MOBILE-FIRST FICA-COMPLIANT APP
# ============================================================

st.set_page_config(
    page_title="Khula Collective 🇿🇦",
    page_icon="🇿🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MOBILE-FIRST RESPONSIVE STYLING
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Mobile-first base */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Mobile-optimized hero */
    .balance-hero {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 50%, #0984e3 100%);
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        margin: 10px 0 20px 0;
        box-shadow: 0 15px 40px rgba(0, 184, 148, 0.3);
    }
    .balance-amount {
        color: #ffffff;
        font-size: clamp(48px, 10vw, 72px);
        font-weight: 900;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin: 10px 0;
        line-height: 1;
    }
    .balance-label {
        color: rgba(255,255,255,0.85);
        font-size: clamp(12px, 3vw, 16px);
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Mobile-friendly metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1e30 0%, #2a2a40 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        min-height: 120px;
    }
    .metric-number {
        font-size: clamp(28px, 6vw, 36px);
        font-weight: 800;
        background: linear-gradient(135deg, #00b894, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
    }
    .metric-label {
        color: rgba(255,255,255,0.6);
        font-size: clamp(11px, 2.5vw, 13px);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Touch-friendly buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00b894, #0984e3) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        min-height: 50px !important;
        touch-action: manipulation !important;
    }
    
    /* Voted button style */
    .stButton > button[disabled] {
        background: linear-gradient(135deg, #636e72, #2d3436) !important;
        opacity: 0.6 !important;
    }
    
    /* AI reasoning box */
    .ai-reason {
        background: rgba(9, 132, 227, 0.1);
        border-left: 4px solid #0984e3;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: rgba(255,255,255,0.8);
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Investment card */
    .invest-card {
        background: linear-gradient(135deg, #1e1e30 0%, #2a2a40 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
    }
    .invest-title {
        color: #ffffff;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    /* Vote badge */
    .vote-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        margin: 5px 0;
    }
    
    /* Already voted badge */
    .voted-badge {
        display: inline-block;
        background: rgba(100, 100, 100, 0.3);
        color: rgba(255,255,255,0.6);
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 13px;
        margin: 5px 0;
    }
    
    /* Section headers */
    .section-header {
        color: #ffffff;
        font-size: clamp(20px, 5vw, 24px);
        font-weight: 700;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(0, 184, 148, 0.3);
    }
    
    /* Tabs - mobile friendly */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(30,30,48,0.8);
        border-radius: 12px;
        padding: 6px;
        overflow-x: auto;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: rgba(255,255,255,0.6);
        font-weight: 600;
        padding: 12px 16px;
        white-space: nowrap;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00b894, #0984e3);
        color: white !important;
    }
    
    /* Constitution viewer */
    .constitution-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        max-height: 400px;
        overflow-y: auto;
    }
    .constitution-text {
        color: rgba(255,255,255,0.8);
        font-size: 14px;
        line-height: 1.8;
    }
    
    /* Responsive containers */
    @media (max-width: 768px) {
        .balance-hero {
            padding: 25px 15px;
        }
        .metric-card {
            padding: 15px;
            min-height: 100px;
        }
        .invest-card {
            padding: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_db():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'khula_collective.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_votes_table():
    """Create Votes table if it doesn't exist"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Votes (
            vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            suggestion_id INTEGER NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (suggestion_id) REFERENCES Suggestions(suggestion_id),
            UNIQUE(user_id, suggestion_id)
        )
    """)
    conn.commit()
    conn.close()

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

def save_constitution_signature(user_id, full_name):
    conn = get_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        UPDATE Users 
        SET constitution_signed = 1, 
            constitution_signed_date = ?
        WHERE user_id = ?
    """, (timestamp, user_id))
    conn.commit()
    conn.close()
    return timestamp

def get_votes():
    """Get all investment suggestions with vote counts and details"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ensure votes column exists in Suggestions
    cursor.execute("PRAGMA table_info(Suggestions)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'votes' not in columns:
        try:
            cursor.execute("ALTER TABLE Suggestions ADD COLUMN votes INTEGER DEFAULT 0")
            conn.commit()
        except:
            pass
    
    # Get suggestions with vote counts from Votes table
    cursor.execute("""
        SELECT 
            s.suggestion_id,
            s.suggestion_text,
            s.created_at,
            COUNT(v.vote_id) as vote_count
        FROM Suggestions s
        LEFT JOIN Votes v ON s.suggestion_id = v.suggestion_id
        GROUP BY s.suggestion_id
        ORDER BY vote_count DESC, s.created_at DESC
    """)
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

def user_has_voted(user_id, suggestion_id):
    """Check if user has already voted for this suggestion"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) as count FROM Votes 
        WHERE user_id = ? AND suggestion_id = ?
    """, (user_id, suggestion_id))
    result = cursor.fetchone()
    conn.close()
    return result['count'] > 0

def cast_vote(user_id, suggestion_id):
    """Cast a vote for a suggestion (one vote per user per suggestion)"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Votes (user_id, suggestion_id, voted_at)
            VALUES (?, ?, ?)
        """, (user_id, suggestion_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        # User already voted
        success = False
    conn.close()
    return success

def add_investment_suggestion(text, user_id):
    """Add a new investment suggestion"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Suggestions (user_id, suggestion_text, created_at)
        VALUES (?, ?, ?)
    """, (user_id, text, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    suggestion_id = cursor.lastrowid
    conn.close()
    return suggestion_id


# ============================================================
# AI ADVISOR WITH MARKET INTELLIGENCE
# ============================================================

class KhulaAI:
    """AI Advisor with South African market awareness"""
    
    # Current SA economic indicators (Feb 2026)
    REPO_RATE = 8.25  # SARB Repo Rate
    PRIME_RATE = 11.75  # Prime lending rate (Repo + 3.5%)
    INFLATION = 5.2  # CPI inflation
    
    @staticmethod
    def get_market_sentiment():
        """Analyze current market conditions"""
        return {
            'repo_rate': KhulaAI.REPO_RATE,
            'prime_rate': KhulaAI.PRIME_RATE,
            'inflation': KhulaAI.INFLATION,
            'trend': 'stable',
            'outlook': 'Rates expected to remain stable through 2026 as inflation moderates.'
        }
    
    @staticmethod
    def project_future_balance(current_balance, monthly_totals, members_count):
        """Project balance 12 months into future based on consistency"""
        if len(monthly_totals) < 3:
            avg_monthly = 300 * members_count * 0.85
            return {
                'projected_balance': current_balance + (avg_monthly * 12),
                'monthly_avg': avg_monthly,
                'consistency': 85.0,
                'growth': avg_monthly * 12
            }
        
        recent = monthly_totals[-6:]
        avg_monthly = sum(m['total'] for m in recent) / len(recent)
        consistency_rates = [m['members_paid'] / members_count for m in recent]
        avg_consistency = sum(consistency_rates) / len(consistency_rates)
        
        projected_monthly = avg_monthly * 1.02
        projected_balance = current_balance + (projected_monthly * 12)
        
        return {
            'projected_balance': projected_balance,
            'monthly_avg': projected_monthly,
            'consistency': avg_consistency * 100,
            'growth': projected_balance - current_balance
        }
    
    @staticmethod
    def get_investment_recommendation(balance, market_sentiment):
        """Get AI recommendation based on balance and market conditions"""
        repo = market_sentiment['repo_rate']
        
        recommendations = []
        
        if balance < 50000:
            recommendations.append({
                'name': '💰 FNB Money Market Fund',
                'type': 'Liquid Savings',
                'amount': balance,
                'return': f"{repo + 0.5:.2f}%",
                'risk': 'Very Low',
                'liquidity': 'Instant access',
                'why': f"With repo rate at {repo}%, money market funds offer {repo + 0.5:.2f}% return with instant access. Perfect for building your emergency fund before locking into fixed investments.",
                'action': 'Open FNB Money Market account → Transfer R{:,.0f} → Earn monthly interest'.format(balance)
            })
        
        elif balance >= 50000 and balance < 100000:
            bond_rate = 8.75
            recommendations.append({
                'name': '🏛️ RSA Retail Savings Bonds (5-year)',
                'type': 'Fixed Income',
                'amount': 50000,
                'return': f"{bond_rate}%",
                'risk': 'Very Low',
                'liquidity': '5-year lock-in',
                'why': f"Current repo rate is {repo}%. RSA Bonds offer {bond_rate}% FIXED for 5 years - guaranteed by government. Lock in this rate before it drops. R50,000 = R4,375/year guaranteed.",
                'action': 'Visit RSARBonds.gov.za → Register → Invest R50,000 → Earn R365/month'
            })
            
            if balance > 50000:
                remainder = balance - 50000
                recommendations.append({
                    'name': '💰 FNB Money Market (Remainder)',
                    'type': 'Liquid Savings',
                    'amount': remainder,
                    'return': f"{repo + 0.5:.2f}%",
                    'risk': 'Very Low',
                    'liquidity': 'Instant access',
                    'why': f"Keep R{remainder:,.0f} liquid in money market for opportunities and emergencies. Earns {repo + 0.5:.2f}% while staying accessible.",
                    'action': 'FNB Money Market → R{:,.0f} → Instant access + interest'.format(remainder)
                })
        
        else:
            recommendations.append({
                'name': '🏛️ RSA Retail Bonds (50%)',
                'type': 'Fixed Income',
                'amount': balance * 0.5,
                'return': '8.75%',
                'risk': 'Very Low',
                'liquidity': '5-year lock-in',
                'why': f"Lock in 8.75% on R{balance * 0.5:,.0f} before rates drop. Government-backed, zero risk. Generates R{balance * 0.5 * 0.0875 / 12:,.0f}/month.",
                'action': 'RSA Bonds → R{:,.0f} @ 8.75% fixed'.format(balance * 0.5)
            })
            
            recommendations.append({
                'name': '📈 Satrix Top 40 ETF (30%)',
                'type': 'Equity Growth',
                'amount': balance * 0.3,
                'return': '12-15%',
                'risk': 'Medium',
                'liquidity': 'Sell anytime',
                'why': f"JSE Top 40 companies (Naspers, Anglo, etc.). Historical 12-15% returns. R{balance * 0.3:,.0f} could grow to R{balance * 0.3 * 1.13:,.0f} in 1 year.",
                'action': 'EasyEquities → Buy Satrix Top 40 → R{:,.0f}'.format(balance * 0.3)
            })
            
            recommendations.append({
                'name': '💰 Money Market (20%)',
                'type': 'Liquid Reserve',
                'amount': balance * 0.2,
                'return': f"{repo + 0.5:.2f}%",
                'risk': 'Very Low',
                'liquidity': 'Instant access',
                'why': f"Emergency fund + opportunity capital. R{balance * 0.2:,.0f} stays liquid earning {repo + 0.5:.2f}% for quick deployment.",
                'action': 'FNB Money Market → R{:,.0f} → Instant access'.format(balance * 0.2)
            })
        
        return recommendations


# ============================================================
# CONSTITUTION DOCUMENT
# ============================================================

CONSTITUTION_TEXT = """
# KHULA COLLECTIVE CONSTITUTION

## 1. NAME AND PURPOSE
This collective shall be known as "Khula Collective" (meaning "to grow" in isiZulu). 
Our purpose is to pool resources for collective investment and wealth creation.

## 2. MEMBERSHIP
- Membership is open to all South African citizens over 18 years of age
- Each member must complete FICA verification (ID, RICA, proof of residence)
- Members must sign this constitution digitally to confirm understanding and agreement

## 3. CONTRIBUTIONS
- Monthly contribution: R300 per member
- Due date: 25th of each month
- Payment method: EFT to designated FNB account
- Late payments: Grace period of 5 days, then member marked as non-compliant

## 4. COLLECTIVE POT
- All contributions go into a single collective pot
- No individual accounts - we invest as ONE collective
- Returns are distributed proportionally based on total contributions
- Minimum balance of R50,000 required before first investment

## 5. INVESTMENT DECISIONS
- All investments require 60% member approval via voting
- Voting period: 7 days for each proposal
- AI Advisor provides recommendations, but members decide
- No single investment can exceed 40% of total pot

## 6. RETURNS AND WITHDRAWALS
- Returns are reinvested unless 70% of members vote to distribute
- Emergency withdrawals: Allowed with 2-week notice and 10% penalty
- Planned withdrawals: Quarterly, proportional to contributions
- Exit: Member can exit with 30-day notice, receives proportional share

## 7. GOVERNANCE
- Democratic voting on all major decisions
- Admin manages operations but cannot make investment decisions alone
- Annual general meeting (virtual) to review performance
- Transparency: All transactions visible to all members

## 8. RISK AND LIABILITY
- Investments carry risk - no guaranteed returns
- Members understand they may lose capital
- Collective is not a registered financial institution
- Members invest at their own risk

## 9. DISPUTE RESOLUTION
- Disputes resolved by majority vote
- Mediation before legal action
- South African law applies

## 10. AMENDMENTS
- Constitution can be amended with 75% member approval
- Proposed amendments must be circulated 14 days before vote

## DIGITAL SIGNATURE
By checking the box below and entering your full name, you:
- Confirm you have read and understood this constitution
- Agree to abide by all terms and conditions
- Acknowledge the risks involved in collective investing
- Consent to FICA verification and data storage

Date: {date}
Version: 1.0
"""


# ============================================================
# LOGIN SCREEN
# ============================================================

def show_login():
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 20px 0;">
        <div style="font-size: clamp(32px, 8vw, 48px); font-weight: 900; 
                    background: linear-gradient(135deg, #00b894, #00cec9, #0984e3);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🇿🇦 KHULA COLLECTIVE
        </div>
        <div style="color: rgba(255,255,255,0.5); font-size: clamp(10px, 2.5vw, 12px); 
                    letter-spacing: 3px; text-transform: uppercase; margin-top: 8px;">
            Building Wealth Together
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.5, 2, 0.5])
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e1e30, #2a2a40); 
                    border-radius: 20px; padding: 30px 20px; 
                    border: 1px solid rgba(255,255,255,0.08);
                    box-shadow: 0 20px 60px rgba(0,0,0,0.5);">
            <h3 style="color: #fff; text-align: center; margin-bottom: 5px;">Welcome Back</h3>
            <p style="color: rgba(255,255,255,0.5); text-align: center; font-size: 14px;">Sign in to access your collective</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
        
        if st.button("🔓 Sign In", use_container_width=True, key="login_btn"):
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
# MAIN DASHBOARD - MOBILE OPTIMIZED
# ============================================================

def show_dashboard():
    # Initialize votes table
    initialize_votes_table()
    
    user = st.session_state['user']
    full_name = f"{user['first_name']} {user['surname']}"
    is_admin = user['is_admin'] == 1
    
    # Sidebar - Constitution & Profile
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 24px; font-weight: 900; 
                        background: linear-gradient(135deg, #00b894, #00cec9);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🇿🇦 KHULA
            </div>
            <div style="color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 5px;">
                {full_name}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        # Constitution Section
        st.markdown("### 📜 Digital Constitution")
        
        if user['constitution_signed'] == 0:
            st.warning("⚠️ Sign to vote on investments")
            
            with st.expander("📖 Read Constitution", expanded=False):
                constitution_html = CONSTITUTION_TEXT.replace('\n', '<br>').format(
                    date=datetime.now().strftime('%d %B %Y')
                )
                st.markdown(f'<div class="constitution-box"><div class="constitution-text">{constitution_html}</div></div>', 
                           unsafe_allow_html=True)
            
            st.markdown("### ✍️ Digital Signature")
            agree = st.checkbox("I agree to the constitution", key="const_agree")
            signature_name = st.text_input("Your full name", placeholder=full_name, key="const_name")
            
            if st.button("📝 Sign Constitution", use_container_width=True, disabled=not agree or not signature_name):
                if signature_name.strip().lower() == full_name.lower():
                    timestamp = save_constitution_signature(user['user_id'], signature_name)
                    st.success(f"✅ Signed at {timestamp}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Name must match your registered name")
        else:
            st.success("✅ Constitution Signed")
            st.caption(f"Signed: {user['constitution_signed_date']}")
            
            with st.expander("📖 View Constitution"):
                constitution_html = CONSTITUTION_TEXT.replace('\n', '<br>').format(
                    date=datetime.now().strftime('%d %B %Y')
                )
                st.markdown(f'<div class="constitution-box"><div class="constitution-text">{constitution_html}</div></div>', 
                           unsafe_allow_html=True)
    
    # Main Content
    total_balance = get_total_balance()
    monthly_totals = get_monthly_totals()
    members = get_all_members()
    total_members = len(members)
    
    # Hero Balance Card
    st.markdown(f"""
    <div class="balance-hero">
        <div class="balance-label">💰 COLLECTIVE POT</div>
        <div class="balance-amount">R{total_balance:,.2f}</div>
        <div class="balance-label">{total_members} Members • Since Jan 2025</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Metrics
    col1, col2 = st.columns(2)
    with col1:
        months_active = len(monthly_totals)
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Months Active</div>
            <div class="metric-number">{months_active}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        avg_monthly = total_balance / months_active if months_active > 0 else 0
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Avg Monthly</div>
            <div class="metric-number">R{avg_monthly:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs(["📊 Dashboard", "🗳️ Member Voice", "💡 AI Advisor", "👤 Profile"])
    
    # TAB 1: DASHBOARD
    with tabs[0]:
        st.markdown('<div class="section-header">📈 Growth Over Time</div>', unsafe_allow_html=True)
        
        if monthly_totals:
            df = pd.DataFrame(monthly_totals)
            month_labels = []
            for _, row in df.iterrows():
                try:
                    dt = datetime(int(row['year']), int(row['month']), 1)
                    month_labels.append(dt.strftime('%b %y'))
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
                hovertemplate='<b>%{x}</b><br>R%{y:,.0f}<extra></extra>'
            ))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='rgba(255,255,255,0.7)', family='Inter'),
                height=300, margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickprefix='R', tickformat=',.'),
                hovermode='x unified',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 12-Month Projection
        st.markdown('<div class="section-header">🔮 12-Month Projection</div>', unsafe_allow_html=True)
        
        ai = KhulaAI()
        projection = ai.project_future_balance(total_balance, monthly_totals, total_members)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Projected (Feb 2027)</div>
                <div class="metric-number">R{projection['projected_balance']:,.0f}</div>
                <div class="metric-label">+R{projection['growth']:,.0f} growth</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Consistency</div>
                <div class="metric-number">{projection['consistency']:.0f}%</div>
                <div class="metric-label">R{projection['monthly_avg']:,.0f}/month</div>
            </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="ai-reason">
            <strong>🤖 AI Analysis:</strong> Based on {projection['consistency']:.0f}% payment consistency 
            and R{projection['monthly_avg']:,.0f} average monthly contributions, your pot will grow to 
            R{projection['projected_balance']:,.0f} by Feb 2027. That's R{projection['growth']:,.0f} in new capital!
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 2: MEMBER VOICE (LIVE VOTING DASHBOARD)
    with tabs[1]:
        st.markdown('<div class="section-header">🗳️ Live Voting Dashboard</div>', unsafe_allow_html=True)
        
        if user['constitution_signed'] == 0:
            st.warning("⚠️ Sign the constitution in sidebar to vote")
        else:
            market = KhulaAI().get_market_sentiment()
            recommendations = KhulaAI().get_investment_recommendation(total_balance, market)
            
            st.markdown(f"""
            <div class="ai-reason">
                <strong>📊 Market Context (Feb 2026):</strong><br>
                • SARB Repo Rate: {market['repo_rate']}%<br>
                • Prime Rate: {market['prime_rate']}%<br>
                • Inflation: {market['inflation']}%<br>
                • {market['outlook']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🤖 AI Recommended Investments")
            st.caption("Vote for your preferred option. Each member gets ONE vote per proposal. Requires 60% approval.")
            
            # Get current votes
            all_votes = get_votes()
            vote_map = {v['suggestion_text']: v for v in all_votes}
            
            # Add AI recommendations to database if they don't exist
            for rec in recommendations:
                if rec['name'] not in vote_map:
                    suggestion_id = add_investment_suggestion(rec['name'], 1)  # Admin user_id = 1
                    vote_map[rec['name']] = {
                        'suggestion_id': suggestion_id,
                        'suggestion_text': rec['name'],
                        'vote_count': 0
                    }
            
            # Refresh votes after adding
            all_votes = get_votes()
            vote_map = {v['suggestion_text']: v for v in all_votes}
            
            # Display each recommendation with voting
            for i, rec in enumerate(recommendations):
                vote_data = vote_map.get(rec['name'])
                if not vote_data:
                    continue
                
                suggestion_id = vote_data['suggestion_id']
                current_votes = vote_data['vote_count']
                has_voted = user_has_voted(user['user_id'], suggestion_id)
                vote_pct = (current_votes / total_members * 100) if total_members > 0 else 0
                
                with st.container():
                    st.markdown(f"""
                    <div class="invest-card">
                        <div class="invest-title">{rec['name']}</div>
                        <div style="margin: 10px 0;">
                            <span style="background: rgba(0,184,148,0.2); color: #00b894; padding: 4px 12px; 
                                       border-radius: 12px; font-size: 13px; font-weight: 600; margin-right: 8px;">
                                {rec['return']} return
                            </span>
                            <span style="background: rgba(253,203,110,0.2); color: #fdcb6e; padding: 4px 12px; 
                                       border-radius: 12px; font-size: 13px; font-weight: 600;">
                                {rec['risk']} risk
                            </span>
                        </div>
                        <div style="color: rgba(255,255,255,0.7); font-size: 14px; margin: 12px 0;">
                            <strong>Amount:</strong> R{rec['amount']:,.0f}<br>
                            <strong>Liquidity:</strong> {rec['liquidity']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="ai-reason">
                        <strong>🤖 Why this investment?</strong><br>
                        {rec['why']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        if has_voted:
                            st.markdown(f'<div class="voted-badge">✅ You voted for this</div>', unsafe_allow_html=True)
                        else:
                            if st.button(f"👍 Vote for this", key=f"vote_{suggestion_id}", use_container_width=True):
                                if cast_vote(user['user_id'], suggestion_id):
                                    st.success("✅ Vote recorded!")
                                    st.rerun()
                                else:
                                    st.error("❌ You already voted")
                    with col2:
                        st.markdown(f'<div class="vote-badge">{current_votes} votes</div>', unsafe_allow_html=True)
                    with col3:
                        st.metric("Approval", f"{vote_pct:.0f}%")
                    
                    st.markdown("---")
            
            # Live Voting Results Chart
            if all_votes:
                st.markdown('<div class="section-header">📊 Live Voting Results</div>', unsafe_allow_html=True)
                
                # Prepare data for chart
                vote_df = pd.DataFrame([{
                    'Investment': v['suggestion_text'][:35] + '...' if len(v['suggestion_text']) > 35 else v['suggestion_text'],
                    'Votes': v['vote_count'],
                    'Percentage': (v['vote_count'] / total_members * 100) if total_members > 0 else 0
                } for v in all_votes[:8]])  # Top 8 options
                
                # Create horizontal bar chart
                fig2 = px.bar(
                    vote_df, 
                    x='Votes', 
                    y='Investment', 
                    orientation='h',
                    color='Percentage',
                    color_continuous_scale='Tealgrn',
                    text='Votes',
                    labels={'Votes': 'Total Votes', 'Investment': ''}
                )
                
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='rgba(255,255,255,0.7)', family='Inter'),
                    height=400,
                    margin=dict(l=10, r=10, t=10, b=10),
                    showlegend=False,
                    xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
                )
                fig2.update_traces(textposition='outside', textfont_size=14)
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Approval status
                max_votes = max(v['vote_count'] for v in all_votes)
                approval_pct = (max_votes / total_members * 100) if total_members > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Votes Cast", sum(v['vote_count'] for v in all_votes))
                with col2:
                    st.metric("Leading Option", f"{approval_pct:.0f}%")
                with col3:
                    threshold_met = approval_pct >= 60
                    st.metric("60% Threshold", "✅ MET" if threshold_met else "❌ Not Yet")
                
                if approval_pct >= 60:
                    st.success(f"🎉 Leading option has {approval_pct:.0f}% approval - READY TO PROCEED!")
                else:
                    st.info(f"📊 Leading option has {approval_pct:.0f}% approval - Need 60% to proceed ({int(total_members * 0.6)} votes)")
    
    # TAB 3: AI ADVISOR
    with tabs[2]:
        st.markdown('<div class="section-header">🤖 AI Investment Advisor</div>', unsafe_allow_html=True)
        
        market = KhulaAI().get_market_sentiment()
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Market Conditions (Feb 2026)</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 14px; margin: 15px 0; text-align: left;">
                <strong>SARB Repo Rate:</strong> {market['repo_rate']}%<br>
                <strong>Prime Rate:</strong> {market['prime_rate']}%<br>
                <strong>Inflation:</strong> {market['inflation']}%<br>
                <strong>Trend:</strong> {market['trend'].title()}<br><br>
                <strong>Outlook:</strong> {market['outlook']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Strategic Recommendations")
        
        recommendations = KhulaAI().get_investment_recommendation(total_balance, market)
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="invest-card">
                <div class="invest-title">{rec['name']}</div>
                <div style="margin: 10px 0;">
                    <span style="background: rgba(0,184,148,0.2); color: #00b894; padding: 4px 12px; 
                               border-radius: 12px; font-size: 13px; font-weight: 600; margin-right: 8px;">
                        {rec['return']} return
                    </span>
                    <span style="background: rgba(253,203,110,0.2); color: #fdcb6e; padding: 4px 12px; 
                               border-radius: 12px; font-size: 13px; font-weight: 600;">
                        {rec['risk']} risk
                    </span>
                </div>
                <div style="color: rgba(255,255,255,0.7); font-size: 14px; margin: 12px 0;">
                    <strong>Amount:</strong> R{rec['amount']:,.0f}<br>
                    <strong>Type:</strong> {rec['type']}<br>
                    <strong>Liquidity:</strong> {rec['liquidity']}
                </div>
                <div class="ai-reason">
                    <strong>🤖 AI Reasoning:</strong><br>
                    {rec['why']}
                </div>
                <div style="color: rgba(255,255,255,0.6); font-size: 13px; margin-top: 12px;">
                    <strong>Action:</strong> {rec['action']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 4: MY PROFILE
    with tabs[3]:
        st.markdown('<div class="section-header">👤 My Profile</div>', unsafe_allow_html=True)
        
        my_contributions = get_member_contributions(user['user_id'])
        my_total = sum(c['amount'] for c in my_contributions)
        my_months = len(my_contributions)
        my_share = (my_total / total_balance * 100) if total_balance > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">My Total</div>
                <div class="metric-number">R{my_total:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Months Paid</div>
                <div class="metric-number">{my_months}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">My Share</div>
                <div class="metric-number">{my_share:.1f}%</div>
            </div>""", unsafe_allow_html=True)
        
        # Payment history
        st.markdown('<div class="section-header">📅 Payment History</div>', unsafe_allow_html=True)
        
        if my_contributions:
            month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            paid_months = {(c['year'], c['month']) for c in my_contributions}
            
            for year in sorted(set(c['year'] for c in my_contributions), reverse=True):
                st.markdown(f"**{year}**")
                cols = st.columns(6)
                for i in range(12):
                    m = i + 1
                    with cols[i % 6]:
                        if (year, m) in paid_months:
                            st.markdown(f"<div style='text-align:center;background:#1a3a2a;border:1px solid #00b894;border-radius:8px;padding:8px;margin:2px;'><div style='color:#00b894;font-size:10px;'>{month_names[i]}</div><div style='color:#00b894;font-size:16px;'>✅</div></div>", unsafe_allow_html=True)
                        else:
                            now = datetime.now()
                            if year > now.year or (year == now.year and m > now.month):
                                st.markdown(f"<div style='text-align:center;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.05);border-radius:8px;padding:8px;margin:2px;'><div style='color:rgba(255,255,255,0.3);font-size:10px;'>{month_names[i]}</div><div style='color:rgba(255,255,255,0.2);font-size:16px;'>—</div></div>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<div style='text-align:center;background:#3a1a1a;border:1px solid #e74c3c;border-radius:8px;padding:8px;margin:2px;'><div style='color:#e74c3c;font-size:10px;'>{month_names[i]}</div><div style='color:#e74c3c;font-size:16px;'>❌</div></div>", unsafe_allow_html=True)
        else:
            st.info("No contributions yet")


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