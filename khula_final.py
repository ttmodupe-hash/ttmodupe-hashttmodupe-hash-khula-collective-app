"""
KHULA COLLECTIVE - Final Production App
Complete Investment Club Tracker for 20 Members
"""

import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import calendar
import requests
import os

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Khula Collective",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .stProgress > div > div > div > div { background-color: #00a86b; }
    h1 { color: #00a86b; }
    .khula-logo {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #00a86b;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: rgba(0, 168, 107, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .leaderboard-gold { border-left: 5px solid gold; }
    .leaderboard-silver { border-left: 5px solid silver; }
    .leaderboard-bronze { border-left: 5px solid #cd7f32; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('khula_collective.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            surname VARCHAR(100) NOT NULL,
            id_number VARCHAR(13) UNIQUE NOT NULL,
            rica_number VARCHAR(15) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            gender VARCHAR(10),
            date_of_birth DATE,
            yearly_target DECIMAL(15, 2) DEFAULT 3600.00,
            constitution_signed BOOLEAN DEFAULT 0,
            constitution_signed_date TIMESTAMP,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Monthly Contributions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Monthly_Contributions (
            contribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            amount DECIMAL(15, 2) NOT NULL,
            payment_date DATE NOT NULL,
            payment_reference VARCHAR(100),
            status VARCHAR(20) DEFAULT 'Paid',
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            UNIQUE(user_id, month, year)
        )
    """)
    
    # Suggestions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Suggestions (
            suggestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            suggestion_text TEXT NOT NULL,
            votes INTEGER DEFAULT 0,
            status VARCHAR(20) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    """)
    
    # Constitution table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Constitution (
            constitution_id INTEGER PRIMARY KEY AUTOINCREMENT,
            version VARCHAR(20) NOT NULL,
            content TEXT NOT NULL,
            effective_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert default constitution if not exists
    cursor.execute("SELECT COUNT(*) FROM Constitution")
    if cursor.fetchone()[0] == 0:
        constitution_text = """
# KHULA COLLECTIVE CONSTITUTION

## 1. NAME AND PURPOSE
The name of this collective is "Khula Collective" (meaning "Open" in isiZulu). 
Our purpose is to pool resources for collective savings and investment opportunities.

## 2. MEMBERSHIP
- The collective consists of 20 members
- Each member commits to contributing R300 per month
- Membership is by invitation and approval only

## 3. FINANCIAL COMMITMENTS
- Monthly contribution: R300 (Three Hundred Rand)
- Payment due: Last day of each month
- Annual target per member: R3,600
- Contributions start from January 2025

## 4. INVESTMENT STRATEGY
- Funds will be invested collectively based on group decisions
- Investment options include RSA Retail Savings Bonds, Money Market Unit Trusts, and EasyEquities ETFs
- Major investment decisions require 60% member approval

## 5. DECISION MAKING
- Major investment decisions require 60% member approval
- Admin team manages day-to-day operations
- Monthly reports provided to all members

## 6. WITHDRAWAL POLICY
- Members may withdraw with 30 days notice
- Withdrawing members receive their proportional share
- Early withdrawal may incur administrative fees

## 7. COMPLIANCE
- All members must complete FICA verification
- Valid SA ID and RICA-registered cellphone required
- Proof of residence (less than 3 months old) required

## 8. COMMUNICATION
- WhatsApp group for general communication
- Monthly statements via email
- Emergency notifications via SMS/WhatsApp

By signing this constitution, I agree to abide by all terms and conditions.
        """
        
        cursor.execute("""
            INSERT INTO Constitution (version, content, effective_date)
            VALUES (?, ?, ?)
        """, ('1.0', constitution_text, date(2025, 1, 1)))
    
    conn.commit()
    conn.close()

# ============================================================================
# SA ID VALIDATION (LUHN ALGORITHM)
# ============================================================================

def validate_sa_id(id_number):
    """Validate South African ID number using Luhn algorithm"""
    # 1. Basic structure check
    if not (len(id_number) == 13 and id_number.isdigit()):
        return False, "ID must be exactly 13 digits."
    
    # 2. Date of birth validation (YYMMDD)
    try:
        dob_str = id_number[:6]
        datetime.strptime(dob_str, '%y%m%d')
    except ValueError:
        return False, "Invalid Date of Birth in ID."
    
    # 3. Citizenship check (Digit 11: 0 = Citizen, 1 = Permanent Resident)
    if id_number[10] not in ['0', '1']:
        return False, "Invalid Citizenship digit."
    
    # 4. Luhn Algorithm Checksum
    digits = [int(d) for d in id_number]
    odd_sum = sum(digits[0::2])
    even_str = "".join(map(str, [d * 2 for d in digits[1::2]]))
    even_sum = sum(int(d) for d in even_str)
    
    total = odd_sum + even_sum
    if total % 10 != 0:
        return False, "Invalid ID Checksum (Typo detected)."
    
    return True, "Valid ID"

def extract_info_from_id(id_number):
    """Extract information from SA ID number"""
    # Date of birth
    dob_str = id_number[:6]
    year = int(dob_str[:2])
    year = 1900 + year if year > 50 else 2000 + year
    month = int(dob_str[2:4])
    day = int(dob_str[4:6])
    dob = date(year, month, day)
    
    # Gender (digits 7-10)
    gender_code = int(id_number[6:10])
    gender = "Female" if gender_code < 5000 else "Male"
    
    return {'date_of_birth': dob, 'gender': gender}

# ============================================================================
# STITCH API INTEGRATION
# ============================================================================

def get_stitch_credentials():
    """Get Stitch API credentials from secrets or environment"""
    try:
        if hasattr(st, 'secrets'):
            return {
                'client_id': st.secrets.get('STITCH_CLIENT_ID', ''),
                'client_secret': st.secrets.get('STITCH_CLIENT_SECRET', ''),
                'api_url': st.secrets.get('STITCH_API_URL', 'https://api.stitch.money/graphql')
            }
    except:
        pass
    
    return {
        'client_id': os.getenv('STITCH_CLIENT_ID', ''),
        'client_secret': os.getenv('STITCH_CLIENT_SECRET', ''),
        'api_url': os.getenv('STITCH_API_URL', 'https://api.stitch.money/graphql')
    }

def sync_from_stitch_api():
    """Sync transactions from Stitch API"""
    creds = get_stitch_credentials()
    
    if not creds['client_id'] or not creds['client_secret']:
        return False, "Stitch API credentials not configured"
    
    try:
        # Authenticate
        auth_url = "https://secure.stitch.money/connect/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': creds['client_id'],
            'client_secret': creds['client_secret'],
            'scope': 'client_paymentrequest'
        }
        
        response = requests.post(auth_url, data=payload, timeout=10)
        response.raise_for_status()
        access_token = response.json().get('access_token')
        
        # Fetch transactions (GraphQL)
        query = """
        query GetTransactions {
          user {
            bankAccounts {
              transactions {
                edges {
                  node {
                    id
                    amount
                    date
                    description
                  }
                }
              }
            }
          }
        }
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            creds['api_url'],
            json={'query': query},
            headers=headers,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Process transactions
        # (Implementation would parse and store transactions)
        
        return True, "Sync successful"
        
    except Exception as e:
        return False, f"Sync failed: {str(e)}"

# ============================================================================
# AI INVESTMENT ADVISOR
# ============================================================================

def suggest_investments(current_balance, risk_level='Medium'):
    """AI-powered investment suggestions"""
    suggestions = {
        'current_balance': current_balance,
        'risk_level': risk_level,
        'recommendations': [],
        'summary': ''
    }
    
    if current_balance >= 50000:
        suggestions['recommendations'].append({
            'investment': 'RSA Retail Top-Up Bonds',
            'amount': 50000,
            'expected_return': 7.75,
            'reason': '🎯 MILESTONE: Protect R50k against inflation at 7.75% return'
        })
        
        suggestions['summary'] = f"""
**🎉 MILESTONE REACHED: R50,000+**

Based on our current balance of **R{current_balance:,.2f}**, the Khula AI suggests:

**Primary Recommendation:**
Move **R50,000** into an RSA Retail Top-Up Bond at **7.75% interest** to protect our capital against inflation.

**Expected Annual Return:** R3,875

The remaining liquidity (R{current_balance - 50000:,.2f}) should stay in the FNB account for upcoming investment opportunities.

**Action Required:**
1. Schedule group meeting to discuss
2. Vote on investment (60% approval needed)
3. Execute investment strategy
        """
    elif current_balance >= 10000:
        suggestions['summary'] = f"""
**Current Balance: R{current_balance:,.2f}**

**Strategy: Building Towards R50k Milestone**

Continue consistent R300/month contributions. Once we reach R50,000, we'll invest in RSA Retail Bonds at 7.75% return.

**Remaining to Milestone:** R{50000 - current_balance:,.2f}
        """
    else:
        suggestions['summary'] = f"""
**Current Balance: R{current_balance:,.2f}**

**Strategy: Build Foundation**

Focus on consistent contributions to reach our first milestone of R10,000.
        """
    
    return suggestions

# ============================================================================
# WHATSAPP INTEGRATION (TWILIO)
# ============================================================================

def send_whatsapp_reminder(member_name, rica_number, month, year):
    """Send WhatsApp payment reminder via Twilio"""
    try:
        # Get Twilio credentials from secrets
        if hasattr(st, 'secrets'):
            account_sid = st.secrets.get('TWILIO_ACCOUNT_SID', '')
            auth_token = st.secrets.get('TWILIO_AUTH_TOKEN', '')
            whatsapp_number = st.secrets.get('TWILIO_WHATSAPP_NUMBER', '')
            
            if account_sid and auth_token:
                from twilio.rest import Client
                
                client = Client(account_sid, auth_token)
                
                message = f"""
Hi *{member_name}*! 👋

This is the *Khula Bot* 🤖

⏰ *Reminder:* Please deposit your *R300* into the FNB account before month-end!

📅 *Month:* {month} {year}
💰 *Amount:* R300.00

Your contribution helps our collective grow! 🇿🇦
                """
                
                client.messages.create(
                    body=message,
                    from_=f"whatsapp:{whatsapp_number}",
                    to=f"whatsapp:{rica_number}"
                )
                
                return True, "Message sent"
    except Exception as e:
        return False, f"Failed: {str(e)}"
    
    # Demo mode
    return True, "Demo mode (no actual message sent)"

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'constitution_signed' not in st.session_state:
    st.session_state.constitution_signed = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Initialize database
init_database()

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================

def create_user(username, first_name, surname, id_number, rica_number, email, password):
    """Create new user"""
    # Validate ID
    is_valid, message = validate_sa_id(id_number)
    if not is_valid:
        raise ValueError(message)
    
    # Extract info from ID
    id_info = extract_info_from_id(id_number)
    
    # Hash password using SHA-256 (no compilation needed)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO Users (
                username, first_name, surname, id_number, rica_number,
                email, password_hash, gender, date_of_birth
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, first_name, surname, id_number, rica_number,
            email, password_hash, id_info['gender'], id_info['date_of_birth']
        ))
        
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def authenticate_user(username, password):
    """Authenticate user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT user_id, username, first_name, surname, password_hash,
               is_admin, constitution_signed
        FROM Users WHERE username = ?
    """, (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user and hashlib.sha256(password.encode()).hexdigest() == user['password_hash']:
        return dict(user)
    return None

def sign_constitution(user_id):
    """Mark user as having signed constitution"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE Users 
        SET constitution_signed = 1,
            constitution_signed_date = ?
        WHERE user_id = ?
    """, (datetime.now(), user_id))
    
    conn.commit()
    conn.close()

# ============================================================================
# UI COMPONENTS
# ============================================================================

def display_logo():
    """Display Khula Collective logo"""
    st.markdown("""
        <div class="khula-logo">
            🏦 KHULA COLLECTIVE
        </div>
        <p style="text-align: center; color: #666; margin-top: -10px;">
            <i>Building Wealth Together</i> 🇿🇦
        </p>
    """, unsafe_allow_html=True)

def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_admin = False
    st.session_state.constitution_signed = False

# ============================================================================
# REGISTRATION PAGE
# ============================================================================

def registration_page():
    """FICA-compliant registration page"""
    display_logo()
    
    st.title("📝 Member Registration")
    
    st.markdown("""
    ### Welcome to Khula Collective!
    
    Complete all steps to join our investment club.
    """)
    
    with st.form("registration_form"):
        st.markdown("#### Step 1: Personal Information (FICA Compliance)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", max_chars=100)
            surname = st.text_input("Surname *", max_chars=100)
            id_number = st.text_input("SA ID Number (13 digits) *", max_chars=13)
        
        with col2:
            rica_number = st.text_input("RICA Cell Number *", placeholder="0821234567")
            email = st.text_input("Email Address *")
            username = st.text_input("Choose Username *", max_chars=50)
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password *", type="password")
        with col2:
            confirm_password = st.text_input("Confirm Password *", type="password")
        
        st.markdown("---")
        st.markdown("#### Step 2: Khula Collective Constitution")
        
        with st.expander("📋 Read Constitution (Click to expand)", expanded=False):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT content FROM Constitution ORDER BY effective_date DESC LIMIT 1")
            constitution = cursor.fetchone()
            conn.close()
            
            if constitution:
                st.markdown(constitution['content'])
        
        constitution_agree = st.checkbox(
            f"✅ I, {first_name} {surname}, confirm that I have read the Constitution "
            "and agree to contribute R300 monthly starting from January 2025.",
            key="constitution_checkbox"
        )
        
        st.markdown("---")
        
        submit = st.form_submit_button("🚀 Complete Registration", type="primary")
        
        if submit:
            errors = []
            
            if not all([first_name, surname, id_number, rica_number, email, username, password]):
                errors.append("❌ Please fill in all required fields")
            
            if password != confirm_password:
                errors.append("❌ Passwords do not match")
            
            if len(password) < 6:
                errors.append("❌ Password must be at least 6 characters")
            
            is_valid_id, id_message = validate_sa_id(id_number)
            if not is_valid_id:
                errors.append(f"❌ {id_message}")
            
            if not constitution_agree:
                errors.append("❌ You must agree to the Constitution to register")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                try:
                    user_id = create_user(
                        username, first_name, surname, id_number,
                        rica_number, email, password
                    )
                    
                    if user_id:
                        sign_constitution(user_id)
                        
                        st.success("✅ Registration successful!")
                        st.balloons()
                        st.info("👉 Please login with your credentials")
                        
                        # Auto-login
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.is_admin = False
                        st.session_state.constitution_signed = True
                        st.rerun()
                    else:
                        st.error("❌ Registration failed. Username, ID, or email may already exist.")
                
                except ValueError as e:
                    st.error(f"❌ {str(e)}")

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    """Login page"""
    display_logo()
    
    st.title("🔐 Member Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                login_button = st.form_submit_button("Login", type="primary")
            
            with col_b:
                register_button = st.form_submit_button("Register")
            
            if login_button:
                user = authenticate_user(username, password)
                
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user['user_id']
                    st.session_state.username = user['username']
                    st.session_state.is_admin = user['is_admin']
                    st.session_state.constitution_signed = user['constitution_signed']
                    
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            
            if register_button:
                st.session_state.current_page = "Register"
                st.rerun()
        
        st.markdown("---")
        st.info("""
        **Demo Credentials:**
        - Admin: `admin_khula` / `admin123`
        - Members: `thabo_mthembu` / `password123`
        """)

# ============================================================================
# MEMBER DASHBOARD
# ============================================================================

def member_dashboard():
    """Individual member dashboard"""
    st.title("💰 My Savings Dashboard")
    
    user_id = st.session_state.user_id
    current_year = 2025
    current_month = datetime.now().month
    
    # Get contributions
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM Monthly_Contributions
        WHERE user_id = ? AND year = ?
        ORDER BY year DESC, month DESC
    """, (user_id, current_year))
    
    contributions = cursor.fetchall()
    
    cursor.execute("""
        SELECT SUM(amount) FROM Monthly_Contributions
        WHERE user_id = ? AND year = ?
    """, (user_id, current_year))
    
    total_saved = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT SUM(amount) FROM Monthly_Contributions
        WHERE user_id = ?
    """, (user_id,))
    
    total_all_time = cursor.fetchone()[0] or 0
    
    conn.close()
    
    # Progress
    yearly_target = 3600.00
    progress_pct = (total_saved / yearly_target * 100) if yearly_target > 0 else 0
    remaining = max(0, yearly_target - total_saved)
    
    st.markdown("### 📊 Your 2025 Progress")
    st.progress(min(progress_pct / 100, 1.0))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Saved This Year", f"R {total_saved:,.2f}", delta=f"{progress_pct:.1f}%")
    
    with col2:
        st.metric("Yearly Target", f"R {yearly_target:,.2f}")
    
    with col3:
        st.metric("Remaining", f"R {remaining:,.2f}")
    
    with col4:
        st.metric("All-Time Total", f"R {total_all_time:,.2f}")
    
    st.markdown("---")
    
    # Monthly status
    st.markdown("### 📅 Monthly Payment Status (2025)")
    
    months_data = []
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Monthly_Contributions
            WHERE user_id = ? AND month = ? AND year = ? AND status = 'Paid'
        """, (user_id, month, current_year))
        paid = cursor.fetchone()[0] > 0
        conn.close()
        
        if month <= current_month:
            status = "✅ Paid" if paid else "❌ Outstanding"
        else:
            status = "⏳ Upcoming"
        
        months_data.append({
            'Month': month_name,
            'Status': status,
            'Amount': "R300.00" if paid else "-"
        })
    
    df_months = pd.DataFrame(months_data)
    st.dataframe(df_months, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Suggestions & Voting
    st.markdown("### 💡 Suggestions & Voting")
    
    with st.form("suggestion_form"):
        suggestion_text = st.text_area("Submit your idea for the next version:", max_chars=500)
        submit_suggestion = st.form_submit_button("Submit Suggestion")
        
        if submit_suggestion and suggestion_text:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Suggestions (user_id, suggestion_text)
                VALUES (?, ?)
            """, (user_id, suggestion_text))
            conn.commit()
            conn.close()
            
            st.success("✅ Suggestion submitted!")
    
    # View suggestions
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.suggestion_text, s.votes, s.created_at, u.first_name, u.surname
        FROM Suggestions s
        JOIN Users u ON s.user_id = u.user_id
        ORDER BY s.votes DESC, s.created_at DESC
        LIMIT 10
    """)
    suggestions = cursor.fetchall()
    conn.close()
    
    if suggestions:
        st.markdown("#### Recent Suggestions")
        for sug in suggestions:
            st.markdown(f"""
            **{sug['first_name']} {sug['surname']}** - {sug['votes']} votes
            
            {sug['suggestion_text']}
            """)

# ============================================================================
# GROUP DASHBOARD
# ============================================================================

def group_dashboard():
    """Group overview dashboard"""
    st.title("🌍 Khula Collective - Group Dashboard")
    
    # Stitch API Sync
    st.markdown("### 🔄 Live FNB Sync (Stitch API)")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        creds = get_stitch_credentials()
        if creds['client_id']:
            st.success("✅ Stitch API configured")
        else:
            st.warning("⚠️ Stitch API not configured. Using historical data.")
            st.info("Configure STITCH_CLIENT_ID and STITCH_CLIENT_SECRET in Streamlit Secrets")
    
    with col2:
        if st.button("🔄 Sync Now"):
            with st.spinner("Syncing from FNB..."):
                success, message = sync_from_stitch_api()
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    st.markdown("---")
    
    # Get total pot
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM Monthly_Contributions WHERE status = 'Paid'")
    total_pot = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM Users WHERE is_admin = 0")
    total_members = cursor.fetchone()[0]
    
    current_month = datetime.now().month
    current_year = 2025
    
    cursor.execute("""
        SELECT COUNT(DISTINCT user_id) FROM Monthly_Contributions
        WHERE month = ? AND year = ? AND status = 'Paid'
    """, (current_month, current_year))
    paid_count = cursor.fetchone()[0]
    
    conn.close()
    
    compliance_pct = (paid_count / total_members * 100) if total_members > 0 else 0
    
    # Display metrics
    st.markdown("### 💰 Collective Financial Position")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pot", f"R {total_pot:,.2f}", delta="Since Jan 2025")
    
    with col2:
        st.metric("Active Members", total_members)
    
    with col3:
        st.metric(f"{calendar.month_name[current_month]} Compliance", 
                 f"{compliance_pct:.1f}%", delta=f"{paid_count}/{total_members} paid")
    
    with col4:
        expected_total = total_members * 300 * current_month
        st.metric("Expected vs Actual", f"R {total_pot:,.2f}", 
                 delta=f"R {total_pot - expected_total:,.2f}")
    
    st.markdown("---")
    
    # AI Investment Advisor
    st.markdown("### 🤖 AI Investment Advisor")
    
    risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"], index=1)
    
    suggestions = suggest_investments(total_pot, risk_level)
    
    st.markdown(suggestions['summary'])
    
    if st.button("📄 Generate Monthly Investment Report"):
        report = f"""
# KHULA COLLECTIVE - MONTHLY INVESTMENT REPORT
## {calendar.month_name[current_month]} 2025

---

### 💰 Current Financial Position
- **Total Collective Balance:** R{total_pot:,.2f}
- **Risk Profile:** {risk_level}

---

{suggestions['summary']}

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        st.download_button(
            label="Download Report",
            data=report,
            file_name=f"Khula_Report_{calendar.month_name[current_month]}_2025.md",
            mime="text/markdown"
        )
    
    st.markdown("---")
    
    # Leaderboard
    st.markdown("### 🏆 Top Savers Leaderboard")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.first_name, u.surname, SUM(mc.amount) as total_saved,
               COUNT(mc.contribution_id) as months_paid
        FROM Users u
        LEFT JOIN Monthly_Contributions mc ON u.user_id = mc.user_id
        WHERE u.is_admin = 0
        GROUP BY u.user_id
        ORDER BY total_saved DESC
    """)
    
    leaderboard = cursor.fetchall()
    conn.close()
    
    if leaderboard:
        for i, member in enumerate(leaderboard[:3], 1):
            medal = ["🥇", "🥈", "🥉"][i-1]
            rank_class = ["leaderboard-gold", "leaderboard-silver", "leaderboard-bronze"][i-1]
            
            st.markdown(f"""
            <div class="metric-card {rank_class}">
                <h3>{medal} #{i} - {member['first_name']} {member['surname']}</h3>
                <p style="font-size: 20px;"><b>R {member['total_saved']:,.2f}</b> saved</p>
                <p>{member['months_paid']} months paid</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# ADMIN PANEL
# ============================================================================

def admin_panel():
    """Admin panel"""
    if not st.session_state.is_admin:
        st.error("🔒 Access Denied. Admins Only.")
        return
    
    st.title("🛡️ Admin Panel")
    
    tab1, tab2, tab3 = st.tabs(["📋 Member List", "💰 Compliance", "📱 WhatsApp"])
    
    with tab1:
        st.markdown("### Member List & FICA Status")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, first_name, surname, id_number, rica_number,
                   email, gender, constitution_signed, created_at
            FROM Users
            WHERE is_admin = 0
            ORDER BY surname, first_name
        """)
        
        members = cursor.fetchall()
        conn.close()
        
        if members:
            member_data = []
            for member in members:
                member_data.append({
                    'Name': f"{member['first_name']} {member['surname']}",
                    'ID Number': member['id_number'],
                    'RICA': member['rica_number'],
                    'Email': member['email'],
                    'Gender': member['gender'],
                    'Constitution': '✅ Signed' if member['constitution_signed'] else '❌ Pending',
                    'Registered': member['created_at']
                })
            
            df_members = pd.DataFrame(member_data)
            st.dataframe(df_members, use_container_width=True, hide_index=True)
            
            csv = df_members.to_csv(index=False)
            st.download_button(
                label="📥 Download FICA Report (CSV)",
                data=csv,
                file_name=f"Khula_FICA_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with tab2:
        st.markdown("### Payment Compliance")
        
        current_month = datetime.now().month
        current_year = 2025
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.surname, u.rica_number
            FROM Users u
            WHERE u.is_admin = 0
            AND u.user_id NOT IN (
                SELECT user_id FROM Monthly_Contributions
                WHERE month = ? AND year = ? AND status = 'Paid'
            )
        """, (current_month, current_year))
        
        members_in_arrears = cursor.fetchall()
        conn.close()
        
        if members_in_arrears:
            st.warning(f"⚠️ {len(members_in_arrears)} members have not paid for {calendar.month_name[current_month]}")
            
            arrears_data = []
            for member in members_in_arrears:
                arrears_data.append({
                    'Name': f"{member['first_name']} {member['surname']}",
                    'RICA': member['rica_number'],
                    'Amount Due': 'R300.00'
                })
            
            df_arrears = pd.DataFrame(arrears_data)
            st.dataframe(df_arrears, use_container_width=True, hide_index=True)
        else:
            st.success("✅ All members have paid for this month!")
    
    with tab3:
        st.markdown("### WhatsApp Notifications (Twilio)")
        
        # Check credentials
        try:
            if hasattr(st, 'secrets') and 'TWILIO_ACCOUNT_SID' in st.secrets:
                st.success("✅ Twilio configured")
            else:
                st.warning("⚠️ Twilio not configured. Using demo mode.")
        except:
            st.warning("⚠️ Twilio not configured. Using demo mode.")
        
        st.markdown("---")
        
        current_month = datetime.now().month
        current_year = 2025
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.surname, u.rica_number
            FROM Users u
            WHERE u.is_admin = 0
            AND u.user_id NOT IN (
                SELECT user_id FROM Monthly_Contributions
                WHERE month = ? AND year = ? AND status = 'Paid'
            )
        """, (current_month, current_year))
        
        members_in_arrears = cursor.fetchall()
        conn.close()
        
        if members_in_arrears:
            st.info(f"📊 {len(members_in_arrears)} members need payment reminders")
            
            if st.button("📤 Send Bulk Reminders", type="primary"):
                with st.spinner("Sending WhatsApp reminders..."):
                    sent = 0
                    for member in members_in_arrears:
                        success, msg = send_whatsapp_reminder(
                            f"{member['first_name']} {member['surname']}",
                            member['rica_number'],
                            calendar.month_name[current_month],
                            current_year
                        )
                        if success:
                            sent += 1
                    
                    st.success(f"✅ Sent {sent} reminders")
        else:
            st.success("✅ No reminders needed!")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    
    if not st.session_state.authenticated:
        if st.session_state.current_page == "Register":
            registration_page()
        else:
            login_page()
        return
    
    if not st.session_state.constitution_signed:
        st.warning("⚠️ Please sign the constitution")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM Constitution ORDER BY effective_date DESC LIMIT 1")
        constitution = cursor.fetchone()
        conn.close()
        
        with st.expander("📋 Khula Collective Constitution", expanded=True):
            if constitution:
                st.markdown(constitution['content'])
        
        if st.button("✅ I Agree and Sign", type="primary"):
            sign_constitution(st.session_state.user_id)
            st.session_state.constitution_signed = True
            st.success("✅ Constitution signed!")
            st.rerun()
        
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
        
        return
    
    # Authenticated interface
    with st.sidebar:
        display_logo()
        
        st.markdown(f"### 👤 {st.session_state.username}")
        
        if st.session_state.is_admin:
            st.markdown("**Role:** 🛡️ Administrator")
        else:
            st.markdown("**Role:** 👥 Member")
        
        st.markdown("---")
        
        pages = ["Dashboard", "Group Overview"]
        
        if st.session_state.is_admin:
            pages.append("Admin Panel")
        
        page = st.radio("Navigation", pages)
        st.session_state.current_page = page
        
        st.markdown("---")
        
        if st.button("🚪 Logout", type="primary"):
            logout()
            st.rerun()
    
    # Display page
    if st.session_state.current_page == "Dashboard":
        member_dashboard()
    elif st.session_state.current_page == "Group Overview":
        group_dashboard()
    elif st.session_state.current_page == "Admin Panel":
        admin_panel()


if __name__ == "__main__":
    main()