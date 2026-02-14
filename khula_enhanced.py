"""
Khula Collective - Enhanced Investment Club Platform
Advanced version designed to attract and engage new members
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Khula Collective - Grow Together, Prosper Together",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional, attractive design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.5em;
        font-weight: 300;
        margin-bottom: 30px;
        opacity: 0.95;
    }
    
    .hero-cta {
        background: white;
        color: #667eea;
        padding: 15px 40px;
        border-radius: 50px;
        font-size: 1.2em;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
        text-decoration: none;
    }
    
    .hero-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-number {
        font-size: 3em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .stats-label {
        font-size: 1.1em;
        opacity: 0.9;
    }
    
    /* Benefits Section */
    .benefit-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        transition: all 0.3s;
    }
    
    .benefit-card:hover {
        transform: translateX(10px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    .benefit-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    
    .benefit-title {
        font-size: 1.5em;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .benefit-description {
        font-size: 1.1em;
        color: #666;
        line-height: 1.6;
    }
    
    /* Testimonial Cards */
    .testimonial-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .testimonial-text {
        font-size: 1.2em;
        font-style: italic;
        margin-bottom: 15px;
        color: #333;
    }
    
    .testimonial-author {
        font-weight: 600;
        color: #667eea;
        font-size: 1.1em;
    }
    
    /* Progress Bars */
    .progress-container {
        background: #f0f0f0;
        border-radius: 50px;
        height: 30px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        transition: width 1s ease-in-out;
    }
    
    /* Call to Action Boxes */
    .cta-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 40px 0;
    }
    
    .cta-box h2 {
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    
    .cta-box p {
        font-size: 1.3em;
        margin-bottom: 30px;
        opacity: 0.95;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .feature-item {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s;
    }
    
    .feature-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .metric-label {
        font-size: 1.1em;
        color: #666;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.1em;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.2em;
        font-weight: 600;
    }
    
    /* Timeline */
    .timeline-item {
        position: relative;
        padding-left: 40px;
        margin-bottom: 30px;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #667eea;
        border: 4px solid white;
        box-shadow: 0 0 0 2px #667eea;
    }
    
    .timeline-item::after {
        content: '';
        position: absolute;
        left: 9px;
        top: 20px;
        width: 2px;
        height: calc(100% + 10px);
        background: #667eea;
    }
    
    .timeline-item:last-child::after {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///khula_collective.db')
Session = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Initialize global account sync if it doesn't exist
def initialize_database():
    """Initialize database with default values"""
    session = Session()
    try:
        # Check if global_account_sync exists
        sync = session.query(GlobalAccountSync).first()
        if not sync:
            sync = GlobalAccountSync(total_balance=71700.0)
            session.add(sync)
            session.commit()
    except:
        session.rollback()
    finally:
        session.close()

# Initialize on startup
initialize_database()

# Database Models (same as before)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    sa_id_number = Column(String(13))
    date_of_birth = Column(String(10))
    gender = Column(String(10))
    citizenship = Column(String(20))
    rica_verified = Column(Boolean, default=False)
    id_document_path = Column(String(255))
    proof_of_residence_path = Column(String(255))
    constitution_signed = Column(Boolean, default=False)
    constitution_signed_date = Column(DateTime)
    role = Column(String(20), default='member')
    stitch_token = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class MonthlyContribution(Base):
    __tablename__ = 'monthly_contributions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    amount = Column(Float, default=0.0)
    paid = Column(Boolean, default=False)
    payment_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

class InvestmentGoal(Base):
    __tablename__ = 'investment_goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    target_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

class GlobalAccountSync(Base):
    __tablename__ = 'global_account_sync'
    id = Column(Integer, primary_key=True)
    total_balance = Column(Float, default=0.0)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

def get_user(username):
    """Get user from database"""
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        return user
    finally:
        session.close()

def get_total_pot():
    """Get total pot balance"""
    session = Session()
    try:
        sync = session.query(GlobalAccountSync).first()
        return sync.total_balance if sync else 0.0
    finally:
        session.close()

def get_member_count():
    """Get total member count"""
    session = Session()
    try:
        count = session.query(User).filter_by(role='member').count()
        return count
    finally:
        session.close()

def calculate_average_savings():
    """Calculate average savings per member"""
    total_pot = get_total_pot()
    member_count = get_member_count()
    return total_pot / member_count if member_count > 0 else 0

def landing_page():
    """Enhanced landing page to attract new members"""
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🌱 Khula Collective</div>
        <div class="hero-subtitle">Grow Together, Prosper Together</div>
        <p style="font-size: 1.2em; margin-bottom: 30px;">
            Join 20+ members pooling R6,000/month for collective investment opportunities.
            Your R300 contribution becomes part of R72,000/year - accessing investments 
            we couldn't reach alone. Together we invest, together we prosper.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_pot = get_total_pot()
    member_count = get_member_count()
    avg_savings = calculate_average_savings()
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">R{total_pot:,.0f}</div>
            <div class="stats-label">Total Pot</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stats-number">{member_count}</div>
            <div class="stats-label">Active Members</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="stats-number">R{avg_savings:,.0f}</div>
            <div class="stats-label">Avg Per Member</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stats-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
            <div class="stats-number">8-11%</div>
            <div class="stats-label">Expected Returns</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Why Join Section
    st.markdown("## 🎯 Why Pool Our Money Together?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="benefit-card">
            <div class="benefit-icon">💰</div>
            <div class="benefit-title">Access Premium Investments</div>
            <div class="benefit-description">
                R300 alone = savings account (5% return). R6,000 together = RSA Bonds, 
                ETFs, Money Market (8-11% returns). We pool to access what individuals can't.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-card">
            <div class="benefit-icon">🤝</div>
            <div class="benefit-title">Collective Bargaining Power</div>
            <div class="benefit-description">
                Together we negotiate better rates, lower fees, and access institutional 
                investment opportunities. Our R72,000/year collective pot opens doors.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-card">
            <div class="benefit-icon">📊</div>
            <div class="benefit-title">Shared Returns, Shared Success</div>
            <div class="benefit-description">
                All investment returns are distributed proportionally based on contributions.
                When the collective earns 9%, everyone benefits fairly.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="benefit-card">
            <div class="benefit-icon">📈</div>
            <div class="benefit-title">Group Decision Making</div>
            <div class="benefit-description">
                Major investment decisions made together. Your voice matters in how 
                our collective pot is invested. Democracy meets finance.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-card">
            <div class="benefit-icon">🔒</div>
            <div class="benefit-title">Transparent & Accountable</div>
            <div class="benefit-description">
                See exactly where our collective pot is invested. Track returns in real-time.
                Full transparency on every rand invested and earned.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-card">
            <div class="benefit-icon">🌍</div>
            <div class="benefit-title">Community Support System</div>
            <div class="benefit-description">
                Struggling one month? The community supports you. We grow together,
                prosper together, and help each other stay consistent.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Investment Calculator
    st.markdown("## 🧮 See Our Collective Growth Potential")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        num_members = st.slider(
            "Number of Members",
            min_value=10,
            max_value=50,
            value=20,
            step=5
        )
        
        monthly_contribution = st.slider(
            "Monthly Contribution per Member (R)",
            min_value=300,
            max_value=500,
            value=300,
            step=50
        )
        
        years = st.slider(
            "Investment Period (Years)",
            min_value=1,
            max_value=10,
            value=5
        )
        
        return_rate = st.select_slider(
            "Expected Collective Return",
            options=[6, 7, 8, 9, 10, 11, 12],
            value=9,
            format_func=lambda x: f"{x}%"
        )
    
    with col2:
        # Calculate collective projections
        monthly_collective = monthly_contribution * num_members
        months = years * 12
        monthly_rate = return_rate / 100 / 12
        
        # Future value of collective pot
        if monthly_rate > 0:
            collective_future = monthly_collective * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        else:
            collective_future = monthly_collective * months
        
        total_contributed = monthly_collective * months
        collective_returns = collective_future - total_contributed
        
        # Your share (assuming you contribute monthly_contribution)
        your_contribution = monthly_contribution * months
        your_share_percentage = your_contribution / total_contributed
        your_share_value = collective_future * your_share_percentage
        your_share_returns = collective_returns * your_share_percentage
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">R{collective_future:,.0f}</div>
            <div class="metric-label">Collective Pot Value</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="margin-top: 20px;">
            <div class="metric-value" style="color: #43e97b;">R{collective_returns:,.0f}</div>
            <div class="metric-label">Collective Returns</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card" style="margin-top: 20px; background: #f8f9fa;">
            <div class="metric-value" style="color: #667eea; font-size: 1.8em;">R{your_share_value:,.0f}</div>
            <div class="metric-label">Your Share ({your_share_percentage*100:.1f}%)</div>
            <small style="color: #666;">Based on R{your_contribution:,.0f} contribution</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Create collective projection chart
    projection_data = []
    for month in range(1, months + 1):
        if monthly_rate > 0:
            collective_value = monthly_collective * (((1 + monthly_rate) ** month - 1) / monthly_rate)
        else:
            collective_value = monthly_collective * month
        collective_contributed = monthly_collective * month
        your_share = collective_value * your_share_percentage
        projection_data.append({
            'Month': month,
            'Collective Value': collective_value,
            'Collective Contributed': collective_contributed,
            'Your Share': your_share
        })
    
    df_projection = pd.DataFrame(projection_data)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_projection['Month'],
        y=df_projection['Collective Value'],
        name='Collective Pot Value',
        fill='tonexty',
        line=dict(color='#667eea', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=df_projection['Month'],
        y=df_projection['Collective Contributed'],
        name='Total Contributions',
        fill='tozeroy',
        line=dict(color='#43e97b', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df_projection['Month'],
        y=df_projection['Your Share'],
        name=f'Your Share ({your_share_percentage*100:.1f}%)',
        line=dict(color='#ffd43b', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f"Our Collective {years}-Year Investment Journey ({num_members} Members)",
        xaxis_title="Months",
        yaxis_title="Amount (R)",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation
    st.info(f"""
    💡 **How It Works**: {num_members} members each contribute R{monthly_contribution:,}/month = R{monthly_collective:,}/month collective pot.
    Over {years} years, the collective invests R{total_contributed:,} and earns R{collective_returns:,} in returns ({return_rate}% annually).
    Your R{your_contribution:,} contribution ({your_share_percentage*100:.1f}% of pot) becomes worth R{your_share_value:,.0f} - 
    that's R{your_share_returns:,.0f} in returns! **Together we achieve more than alone.**
    """)
    
    # Success Stories
    st.markdown("## 🌟 Community Success Stories")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="testimonial-card">
            <div class="testimonial-text">
                "Alone, my R300 would just sit in a savings account earning 5%. Together with 
                19 others, we pooled R72,000 and invested in RSA Bonds earning 8.25%. 
                My share of returns doubled!"
            </div>
            <div class="testimonial-author">- Thabo M., Founding Member</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="testimonial-card" style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
            <div class="testimonial-text">
                "When I struggled for 2 months, the community supported me. They didn't judge, 
                they helped. Now I'm back on track and our collective pot is stronger than ever!"
            </div>
            <div class="testimonial-author">- Nomsa D., Community Member</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="testimonial-card" style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
            <div class="testimonial-text">
                "We voted together on where to invest our R100k pot. Everyone's voice mattered. 
                That's true collective power - democracy meets finance!"
            </div>
            <div class="testimonial-author">- Sipho K., Active Voter</div>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.markdown("## 📋 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-item">
            <div style="font-size: 3em; margin-bottom: 15px;">1️⃣</div>
            <h3>Sign Up</h3>
            <p>Complete FICA verification and join the collective in minutes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-item">
            <div style="font-size: 3em; margin-bottom: 15px;">2️⃣</div>
            <h3>Contribute</h3>
            <p>Start with R300/month and watch your savings grow automatically</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-item">
            <div style="font-size: 3em; margin-bottom: 15px;">3️⃣</div>
            <h3>Invest</h3>
            <p>Collective pot invested in high-return opportunities guided by AI</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-item">
            <div style="font-size: 3em; margin-bottom: 15px;">4️⃣</div>
            <h3>Prosper</h3>
            <p>Track growth, earn returns, and achieve financial freedom together</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("""
    <div class="cta-box">
        <h2>Ready to Pool Your R300 with Us?</h2>
        <p>Join 20+ members pooling R6,000/month for collective investment opportunities. 
        Together we access RSA Bonds, ETFs, and returns of 8-11%. Your R300 becomes powerful when combined!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🚀 Join Now", use_container_width=True):
            st.session_state.page = 'register'
            st.rerun()
    
    with col2:
        if st.button("👀 Explore Demo", use_container_width=True):
            st.session_state.page = 'demo'
            st.rerun()
    
    with col3:
        if st.button("🔐 Member Login", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
    
    # FAQ Section
    st.markdown("## ❓ Frequently Asked Questions")
    
    with st.expander("💰 How much do I need to contribute?"):
        st.write("""
        Just R300 per month to join the collective pot! That's R10 per day - less than a coffee. 
        Your R300 combines with 19+ other members to create a R6,000/month collective investment fund.
        Together we access opportunities that require R50k+ minimums.
        """)
    
    with st.expander("🔒 Is our collective pot safe?"):
        st.write("""
        Yes! Khula Collective is FICA-compliant with bank-grade security. 
        All collective investments are tracked transparently. You can see exactly where OUR money is invested,
        what returns we're earning, and your proportional share at all times.
        """)
    
    with st.expander("📈 What returns does the collective earn?"):
        st.write("""
        Our collective pot earns 8-11% annual returns through pooled investments in RSA Bonds, ETFs, and Money Market funds.
        This is significantly higher than individual savings accounts (4-6%). Returns are distributed proportionally 
        based on each member's contribution. If you contribute R3,600/year and the collective earns 9%, 
        your share of returns is calculated based on your percentage of the total pot.
        """)
    
    with st.expander("🤝 How does collective investing work?"):
        st.write("""
        All members contribute R300/month to ONE shared pot. When our collective pot reaches milestones 
        (R50k, R80k, R100k+), we vote together on where to invest. Investments are made in the collective's name,
        and returns are distributed proportionally to all members based on their contributions. 
        Your R300 alone can't access RSA Bonds (R50k minimum), but our R72k/year collective pot can!
        """)
    
    with st.expander("📱 Can I track the collective pot?"):
        st.write("""
        Absolutely! You see the total collective pot size, where it's invested, what returns we're earning,
        and your proportional share. You also see your contribution history and percentage of the collective.
        Full transparency on every rand invested and earned by the collective.
        """)
    
    with st.expander("🚪 Can I withdraw my share?"):
        st.write("""
        Withdrawals affect the entire collective, so terms are outlined in our constitution. 
        We encourage 12+ month commitment for meaningful collective growth. Early withdrawal may require 
        community approval to ensure it doesn't harm the collective's investment strategy.
        Remember: we grow together, prosper together.
        """)
    
    with st.expander("👥 Who can join the collective?"):
        st.write("""
        Any South African citizen or permanent resident over 18 years old who commits to R300/month 
        can join our collective. You'll need a valid SA ID, RICA-verified cellphone number, and proof of residence.
        Most importantly, you must believe in collective power and community support.
        """)
    
    with st.expander("🎓 Do I need investment experience?"):
        st.write("""
        Not at all! That's the beauty of collective investing. Our AI advisor recommends where to invest 
        OUR collective pot, and we vote together on major decisions. You learn from experienced members,
        and everyone's voice matters equally. We grow our knowledge together as we grow our wealth together.
        """)
    
    with st.expander("🗳️ How are investment decisions made?"):
        st.write("""
        Major investment decisions are made democratically. When our collective pot reaches a milestone,
        the AI advisor provides recommendations, members discuss options, and we vote together.
        Your R300 contribution gives you an equal vote - this is true collective power!
        """)
    
    with st.expander("💪 What if I miss a month?"):
        st.write("""
        Life happens! The community supports members who struggle. Missing one month doesn't remove you
        from the collective - your share just reflects your total contributions. We encourage consistency
        but understand challenges. That's why we're a community, not just an investment platform.
        """)

def demo_mode():
    """Interactive demo mode for prospects"""
    st.markdown("""
    <div class="hero-section" style="padding: 40px;">
        <h1>🎮 Interactive Demo</h1>
        <p style="font-size: 1.2em;">See how our collective pot grows together - no login required!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("---")
    
    # Demo Dashboard
    st.markdown("## 📊 Collective Dashboard Preview")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Your Contribution", "R3,600", "+R300")
    with col2:
        st.metric("Collective Pot", "R71,700", "+R6,000")
    with col3:
        st.metric("Your Share", "5.0%", "")
    with col4:
        st.metric("Collective Returns", "9.0%", "+0.5%")
    
    # Sample progress chart
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    contributions = [300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300]
    cumulative = [sum(contributions[:i+1]) for i in range(len(contributions))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=contributions,
        name='Monthly',
        marker_color='#667eea'
    ))
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative,
        name='Cumulative',
        line=dict(color='#43e97b', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Your Contribution History",
        yaxis=dict(title="Monthly (R)"),
        yaxis2=dict(title="Cumulative (R)", overlaying='y', side='right'),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Group Overview
    st.markdown("## 🌍 Collective Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">R71,700</div>
            <div class="metric-label">Total Collective Pot</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Leaderboard
        st.markdown("### 💪 Most Consistent Contributors")
        leaderboard_data = {
            'Member': ['Thabo M.', 'You (Nomsa D.)', 'Sipho K.', 'Zanele N.', 'Mandla Z.'],
            'Contribution': ['R3,900', 'R3,600', 'R3,600', 'R3,300', 'R3,300'],
            'Share of Pot': ['5.4%', '5.0%', '5.0%', '4.6%', '4.6%'],
            'Consistency': ['14/14 ✅', '12/14 ✅', '12/14 ✅', '11/14', '11/14']
        }
        st.dataframe(leaderboard_data, use_container_width=True, hide_index=True)
        
        st.info("💡 Everyone's contribution matters! Together we build the collective pot.")
    
    with col2:
        # AI Investment Recommendations
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 25px; border-radius: 15px; color: white;">
            <h3>🤖 Collective Investment Strategy</h3>
            <p style="font-size: 1.1em; margin-top: 15px;">
                <strong>Our Collective Pot:</strong> R71,700<br>
                <strong>Current Investment:</strong><br>
                • R50,000 in RSA Retail Bonds (8.25%)<br>
                • R20,000 in Money Market (7.5%)<br>
                • R1,700 emergency buffer
            </p>
            <div style="background: rgba(255,255,255,0.2); padding: 15px; 
                        border-radius: 10px; margin-top: 15px;">
                <strong>💡 Expected Collective Returns:</strong><br>
                R6,625/year (9.2% average)<br>
                <small>Your 5% share = R331/year</small>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 15px; 
                        border-radius: 10px; margin-top: 15px;">
                <strong>🎯 Next Milestone: R80,000</strong><br>
                <small>R8,300 away from full diversification</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Community Health
        st.markdown("### 💚 Collective Health")
        st.progress(0.85)
        st.write("**85% contribution rate** - Strong collective! 🎉")
        st.caption("When we all contribute consistently, our collective pot grows faster!")
    
    # Call to Action
    st.markdown("""
    <div class="cta-box" style="margin-top: 40px;">
        <h2>Ready to Add Your R300 to Our Collective?</h2>
        <p>This is just a preview. Join now to contribute to our collective pot and share in the returns!<br>
        <strong>Together we invest in opportunities worth R50k+. Alone we can't. That's collective power!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Join Our Collective", use_container_width=True):
            st.session_state.page = 'register'
            st.rerun()

def login_page():
    """Login page"""
    st.markdown("""
    <div class="hero-section" style="padding: 40px;">
        <h1>🔐 Member Login</h1>
        <p>Welcome back! Enter your credentials to access your dashboard.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("Login", use_container_width=True)
            with col_b:
                demo_btn = st.form_submit_button("Try Demo Instead", use_container_width=True)
            
            if demo_btn:
                st.session_state.page = 'demo'
                st.rerun()
            
            if submit:
                if username and password:
                    user = get_user(username)
                    if user and verify_password(password, user.password_hash):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_role = user.role
                        st.session_state.page = 'dashboard'
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p>Don't have an account?</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Join Khula Collective", use_container_width=True):
            st.session_state.page = 'register'
            st.rerun()

def register_page():
    """Enhanced registration page"""
    st.markdown("""
    <div class="hero-section" style="padding: 40px;">
        <h1>🚀 Join Our Collective</h1>
        <p>Add your R300/month to our collective pot - together we invest, together we prosper!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    
    st.markdown("---")
    
    # Registration form (simplified for demo)
    st.markdown("## 📝 Quick Registration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("registration_form"):
            st.markdown("### Personal Information")
            full_name = st.text_input("Full Name *", placeholder="e.g., John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            phone = st.text_input("Phone Number *", placeholder="0821234567")
            
            st.markdown("### Account Details")
            username = st.text_input("Choose Username *", placeholder="johndoe")
            password = st.text_input("Create Password *", type="password")
            confirm_password = st.text_input("Confirm Password *", type="password")
            
            st.markdown("### FICA Compliance")
            sa_id = st.text_input("SA ID Number *", placeholder="9001015009087")
            
            st.markdown("### Agreement")
            constitution = st.checkbox("I have read and agree to the Khula Collective Constitution *")
            
            submit = st.form_submit_button("🎉 Complete Registration", use_container_width=True)
            
            if submit:
                if not all([full_name, email, phone, username, password, sa_id, constitution]):
                    st.error("Please fill in all required fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(sa_id) != 13 or not sa_id.isdigit():
                    st.error("Invalid SA ID number")
                else:
                    st.markdown("""
                    <div class="success-message">
                        🎉 Registration Successful! Welcome to Khula Collective!
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    st.info("In production, your account would be created here. For demo purposes, please use existing login credentials.")
                    if st.button("Go to Login"):
                        st.session_state.page = 'login'
                        st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 25px; border-radius: 15px; margin-top: 40px;">
            <h3>✅ As a Collective Member</h3>
            <ul style="line-height: 2;">
                <li>Contribute R300/month to collective pot</li>
                <li>Vote on investment decisions</li>
                <li>Share in collective returns (proportional)</li>
                <li>Track collective pot growth</li>
                <li>Community support system</li>
                <li>Full transparency on investments</li>
            </ul>
            
            <h3 style="margin-top: 30px;">💰 Collective Milestones</h3>
            <ul style="line-height: 2;">
                <li><strong>R50k:</strong> RSA Bonds (8.25%)</li>
                <li><strong>R80k:</strong> ETF Access (9-10%)</li>
                <li><strong>R100k:</strong> Full Diversification (10-11%)</li>
            </ul>
            
            <p style="margin-top: 20px; padding: 15px; background: #e7f3ff; border-radius: 8px;">
                <strong>💡 Remember:</strong> Your R300 alone = 5% savings account. 
                Our R6,000 together = 9% collective returns. That's the power of pooling!
            </p>
        </div>
        """, unsafe_allow_html=True)

# Main app logic
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: white;">🌱 Khula</h1>
            <p style="color: white; opacity: 0.9;">Collective Investment Club</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.session_state.logged_in:
            st.success(f"Logged in as: {st.session_state.username}")
            if st.button("Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.user_role = None
                st.session_state.page = 'landing'
                st.rerun()
        else:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; color: white;">
                <h3>Quick Links</h3>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = 'landing'
                st.rerun()
            
            if st.button("👀 Demo", use_container_width=True):
                st.session_state.page = 'demo'
                st.rerun()
            
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
            
            if st.button("🚀 Join Now", use_container_width=True):
                st.session_state.page = 'register'
                st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        <div style="color: white; opacity: 0.8; font-size: 0.9em; text-align: center;">
            <p>💡 <strong>Tip:</strong> Start with R300/month and watch your wealth grow!</p>
            <p style="margin-top: 20px;">📞 Support: support@khula.co.za</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content routing
    if st.session_state.page == 'landing':
        landing_page()
    elif st.session_state.page == 'demo':
        demo_mode()
    elif st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'register':
        register_page()
    elif st.session_state.page == 'dashboard' and st.session_state.logged_in:
        st.info("Dashboard page would load here with the original khula_final.py functionality")
        st.write("For now, this is a placeholder. The full dashboard from khula_final.py would be integrated here.")
    else:
        landing_page()

if __name__ == "__main__":
    main()