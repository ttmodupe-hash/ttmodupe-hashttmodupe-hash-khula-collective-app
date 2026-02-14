"""
Khula Collective - Advanced AI-Powered Investment Platform
For serious investors who want real opportunities, real analysis, real returns
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
from ai_investment_engine import InvestmentOpportunityEngine, MarketTrendAnalyzer, RiskCalculator

# Page configuration
st.set_page_config(
    page_title="Khula Collective - AI Investment Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark Professional Theme */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Hero Section */
    .hero-advanced {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 800;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Opportunity Cards */
    .opportunity-card {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        color: white;
        transition: all 0.3s;
    }
    
    .opportunity-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .opp-title {
        font-size: 1.8em;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 15px;
    }
    
    .opp-category {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: 600;
        margin-bottom: 15px;
    }
    
    /* Financial Metrics */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .metric-box {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        color: #51cf66;
        margin-bottom: 5px;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: rgba(255,255,255,0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Risk Assessment */
    .risk-indicator {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9em;
    }
    
    .risk-low {
        background: rgba(81, 207, 102, 0.2);
        color: #51cf66;
    }
    
    .risk-medium {
        background: rgba(255, 212, 59, 0.2);
        color: #ffd43b;
    }
    
    .risk-high {
        background: rgba(255, 107, 107, 0.2);
        color: #ff6b6b;
    }
    
    /* Success Probability */
    .success-bar {
        background: rgba(255,255,255,0.1);
        height: 30px;
        border-radius: 15px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .success-fill {
        height: 100%;
        background: linear-gradient(90deg, #51cf66 0%, #38d9a9 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        transition: width 1s ease-in-out;
    }
    
    /* Action Plan */
    .action-phase {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 3px solid #667eea;
    }
    
    .action-phase h4 {
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .action-item {
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.9);
    }
    
    /* Trend Cards */
    .trend-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin-bottom: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Stats Dashboard */
    .stats-dashboard {
        background: rgba(255,255,255,0.05);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Recommendation Strength */
    .recommendation-badge {
        display: inline-block;
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.1em;
        margin: 10px 0;
    }
    
    .rec-strong {
        background: linear-gradient(135deg, #51cf66 0%, #38d9a9 100%);
        color: white;
    }
    
    .rec-moderate {
        background: linear-gradient(135deg, #ffd43b 0%, #ffa94d 100%);
        color: white;
    }
    
    .rec-weak {
        background: linear-gradient(135deg, #ff6b6b 0%, #fa5252 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Database setup (same as before)
Base = declarative_base()
engine = create_engine('sqlite:///khula_collective.db')
Session = sessionmaker(bind=engine)

class GlobalAccountSync(Base):
    __tablename__ = 'global_account_sync'
    id = Column(Integer, primary_key=True)
    total_balance = Column(Float, default=0.0)
    last_sync = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(engine)

def initialize_database():
    session = Session()
    try:
        sync = session.query(GlobalAccountSync).first()
        if not sync:
            sync = GlobalAccountSync(total_balance=71700.0)
            session.add(sync)
            session.commit()
    except:
        session.rollback()
    finally:
        session.close()

initialize_database()

def get_collective_balance():
    session = Session()
    try:
        sync = session.query(GlobalAccountSync).first()
        return sync.total_balance if sync else 71700.0
    finally:
        session.close()

# Initialize AI Engine
@st.cache_resource
def get_ai_engine():
    balance = get_collective_balance()
    return InvestmentOpportunityEngine(balance)

@st.cache_resource
def get_trend_analyzer():
    return MarketTrendAnalyzer()

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px; color: white;">
            <h1 style="color: white;">🧠 Khula AI</h1>
            <p style="opacity: 0.9;">Investment Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🎯 Investment Opportunities", "📈 Market Trends", "🧮 ROI Calculator", "📚 Investment Academy"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        balance = get_collective_balance()
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; color: white;">
            <h3 style="color: #51cf66;">Collective Pot</h3>
            <h2 style="color: white;">R{balance:,.0f}</h2>
            <p style="opacity: 0.8; font-size: 0.9em;">20 members pooling together</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    if page == "🎯 Investment Opportunities":
        show_investment_opportunities()
    elif page == "📈 Market Trends":
        show_market_trends()
    elif page == "🧮 ROI Calculator":
        show_roi_calculator()
    elif page == "📚 Investment Academy":
        show_investment_academy()

def show_investment_opportunities():
    """Show AI-powered investment opportunities"""
    
    st.markdown("""
    <div class="hero-advanced">
        <div class="hero-title">🧠 AI Investment Intelligence</div>
        <p style="font-size: 1.3em; margin-bottom: 20px;">
            Real opportunities. Real analysis. Real returns.
        </p>
        <p style="font-size: 1.1em; opacity: 0.9;">
            Our AI analyzes your R71,700 collective pot and recommends the best investment opportunities
            with detailed risk analysis, ROI projections, and step-by-step action plans.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get AI recommendations
    engine = get_ai_engine()
    balance = get_collective_balance()
    opportunities = engine.get_opportunities_for_balance(balance)
    
    if not opportunities:
        st.warning(f"No suitable opportunities found for R{balance:,.0f}. Consider growing the collective pot to R80,000+ for more options.")
        return
    
    st.markdown(f"## 🎯 Top {len(opportunities)} Opportunities for R{balance:,.0f}")
    st.markdown("Ranked by success probability, ROI, and risk-adjusted returns")
    
    # Show top opportunities
    for i, opp in enumerate(opportunities, 1):
        with st.expander(f"#{i} - {opp['name']} - {opp['roi']['annual_return_percentage']:.0f}% ROI", expanded=(i==1)):
            show_opportunity_detail(opp, engine)

def show_opportunity_detail(opp, engine):
    """Show detailed opportunity analysis"""
    
    # Header
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="opp-title">{opp['name']}</div>
        <div class="opp-category">{opp['category']}</div>
        <p style="font-size: 1.1em; color: rgba(255,255,255,0.9); margin-top: 15px;">
            {opp['description']}
        </p>
        """, unsafe_allow_html=True)
    
    with col2:
        rec = engine.generate_detailed_recommendation(opp)
        strength = rec['recommendation_strength']
        
        if strength >= 75:
            badge_class = "rec-strong"
            badge_text = "HIGHLY RECOMMENDED"
        elif strength >= 50:
            badge_class = "rec-moderate"
            badge_text = "RECOMMENDED"
        else:
            badge_class = "rec-weak"
            badge_text = "CONSIDER CAREFULLY"
        
        st.markdown(f"""
        <div class="recommendation-badge {badge_class}">
            {badge_text}
        </div>
        <p style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.9em;">
            Strength: {strength:.0f}/100
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Financial Metrics
    st.markdown("### 💰 Financial Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">R{opp['investment_required']:,}</div>
            <div class="metric-label">Investment Required</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">R{opp['revenue_model']['annual_profit']:,}</div>
            <div class="metric-label">Annual Profit</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{opp['roi']['annual_return_percentage']:.1f}%</div>
            <div class="metric-label">Annual ROI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{opp['roi']['payback_period_months']:.1f}</div>
            <div class="metric-label">Payback (Months)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Revenue Breakdown
    st.markdown("### 📊 Revenue Model")
    
    revenue_data = opp['revenue_model']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Monthly/Cycle Breakdown:**")
        if 'monthly_revenue' in revenue_data:
            st.write(f"• Revenue: R{revenue_data['monthly_revenue']:,}/month")
            st.write(f"• Costs: R{revenue_data['monthly_costs']['total']:,}/month")
            st.write(f"• **Profit: R{revenue_data['monthly_profit']:,}/month**")
        else:
            st.write(f"• Revenue: R{revenue_data['revenue_per_cycle']:,}/cycle")
            st.write(f"• Costs: R{revenue_data['costs_per_cycle']['total']:,}/cycle")
            st.write(f"• **Profit: R{revenue_data['profit_per_cycle']:,}/cycle**")
    
    with col2:
        st.markdown("**Annual Projections:**")
        st.write(f"• Total Revenue: R{revenue_data['annual_revenue']:,}")
        st.write(f"• Total Profit: R{revenue_data['annual_profit']:,}")
        st.write(f"• ROI: {opp['roi']['annual_return_percentage']:.1f}%")
    
    # Collective Impact
    st.markdown("### 👥 Impact on Collective (20 Members)")
    
    impact = rec['collective_impact']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Your Investment", f"R{impact['investment_per_member']:,.0f}", "5% of pot")
    
    with col2:
        st.metric("Your Annual Return", f"R{impact['profit_per_member']:,.0f}", f"{impact['roi_per_member']:.0f}%")
    
    with col3:
        st.metric("Monthly Passive Income", f"R{impact['monthly_return_per_member']:,.0f}", "per member")
    
    with col4:
        st.metric("Collective Annual Profit", f"R{impact['total_annual_profit']:,}", "total")
    
    # Risk Assessment
    st.markdown("### ⚠️ Risk Analysis")
    
    st.markdown(f"""
    <div style="margin: 20px 0;">
        <strong>Success Probability: {opp['success_probability']}%</strong>
        <div class="success-bar">
            <div class="success-fill" style="width: {opp['success_probability']}%;">
                {opp['success_probability']}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for risk_name, risk_data in opp['risks'].items():
        risk_level = risk_data['level']
        risk_class = f"risk-{risk_level.lower()}"
        
        st.markdown(f"""
        <div style="margin: 15px 0; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong style="color: white;">{risk_name.replace('_', ' ').title()}</strong>
                <span class="risk-indicator {risk_class}">{risk_level} Risk - {risk_data['percentage']}%</span>
            </div>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">
                <strong>Mitigation:</strong> {risk_data['mitigation']}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Market Analysis
    st.markdown("### 📈 Market Analysis")
    
    market_analysis = opp.get('market_analysis', {})
    if market_analysis:
        for key, value in market_analysis.items():
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    else:
        st.info("Market analysis data not available for this opportunity.")
    
    # Requirements
    st.markdown("### 📋 Requirements")
    
    requirements = opp.get('requirements', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Space:** {requirements.get('space', 'N/A')}")
        st.write(f"**Permits:** {requirements.get('permits', 'N/A')}")
    
    with col2:
        st.write(f"**Skills:** {requirements.get('skills', 'N/A')}")
        st.write(f"**Team:** {requirements.get('team', 'N/A')}")
    
    # Action Plan
    st.markdown("### 🎯 Step-by-Step Action Plan")
    
    action_plan = rec['action_plan']
    
    phases = [
        ('Phase 1: Research & Due Diligence', action_plan['phase_1_research']),
        ('Phase 2: Preparation & Setup', action_plan['phase_2_preparation']),
        ('Phase 3: Launch & Execution', action_plan['phase_3_execution'])
    ]
    
    for phase_name, actions in phases:
        st.markdown(f"""
        <div class="action-phase">
            <h4>{phase_name}</h4>
        """, unsafe_allow_html=True)
        
        for action in actions:
            st.markdown(f'<div class="action-item">✓ {action}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.info(f"⏱️ **Timeline:** {action_plan['timeline']}")
    
    # Vote Button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button(f"🗳️ Vote to Invest in {opp['name']}", use_container_width=True, type="primary"):
            st.success("Your vote has been recorded! The collective will review this opportunity.")
            st.balloons()

def show_market_trends():
    """Show market trend analysis"""
    
    st.markdown("""
    <div class="hero-advanced">
        <div class="hero-title">📈 Market Intelligence</div>
        <p style="font-size: 1.2em;">
            Real-time trends and emerging opportunities in South Africa
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    analyzer = get_trend_analyzer()
    trends = analyzer.get_trend_analysis()
    
    # High Growth Sectors
    st.markdown("## 🚀 High Growth Sectors")
    
    for sector in trends['high_growth_sectors']:
        st.markdown(f"""
        <div class="trend-card">
            <h3>{sector['sector']}</h3>
            <p><strong>Growth Rate:</strong> {sector['growth_rate']}</p>
            <p><strong>Opportunity:</strong> {sector['opportunity']}</p>
            <p><strong>Why Now:</strong> {sector['why']}</p>
            <p><strong>Entry Capital:</strong> {sector['entry_capital']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Emerging Opportunities
    st.markdown("## 💡 Emerging Opportunities")
    
    for opp in trends['emerging_opportunities']:
        st.markdown(f"""
        <div class="opportunity-card">
            <h3>{opp['opportunity']}</h3>
            <p><strong>Why:</strong> {opp['why']}</p>
            <p><strong>Potential Return:</strong> {opp['potential_return']}</p>
            <p><strong>Risk Level:</strong> {opp['risk_level']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sectors to Avoid
    st.markdown("## ⚠️ Sectors to Avoid")
    
    for sector in trends['avoid_sectors']:
        st.warning(f"**{sector['sector']}**: {sector['reason']}")

def show_roi_calculator():
    """Interactive ROI calculator"""
    
    st.markdown("""
    <div class="hero-advanced">
        <div class="hero-title">🧮 ROI Calculator</div>
        <p style="font-size: 1.2em;">
            Calculate returns for any investment opportunity
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        investment = st.number_input("Initial Investment (R)", min_value=1000, max_value=200000, value=50000, step=1000)
        monthly_profit = st.number_input("Monthly Profit (R)", min_value=0, max_value=100000, value=5000, step=500)
        risk_percentage = st.slider("Risk Level (%)", 0, 100, 30)
    
    with col2:
        annual_profit = monthly_profit * 12
        roi = (annual_profit / investment) * 100
        payback_months = investment / monthly_profit if monthly_profit > 0 else 0
        risk_adjusted_return = RiskCalculator.calculate_risk_adjusted_return(roi, risk_percentage)
        
        st.metric("Annual Profit", f"R{annual_profit:,.0f}")
        st.metric("ROI", f"{roi:.1f}%")
        st.metric("Payback Period", f"{payback_months:.1f} months")
        st.metric("Risk-Adjusted Return", f"{risk_adjusted_return:.1f}")
    
    # Projection Chart
    months = list(range(1, 37))
    cumulative_profit = [monthly_profit * m for m in months]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_profit,
        name='Cumulative Profit',
        fill='tozeroy',
        line=dict(color='#51cf66', width=3)
    ))
    fig.add_hline(y=investment, line_dash="dash", line_color="#ff6b6b", 
                  annotation_text="Break Even Point")
    
    fig.update_layout(
        title="3-Year Profit Projection",
        xaxis_title="Months",
        yaxis_title="Cumulative Profit (R)",
        template='plotly_dark',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_investment_academy():
    """Investment education content"""
    
    st.markdown("""
    <div class="hero-advanced">
        <div class="hero-title">📚 Investment Academy</div>
        <p style="font-size: 1.2em;">
            Learn how to evaluate and manage investments
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🎓 Key Investment Principles")
    
    principles = [
        {
            'title': 'Risk vs Reward',
            'content': 'Higher returns always come with higher risk. A 300% ROI opportunity has significant risk. Diversification is key.'
        },
        {
            'title': 'Due Diligence',
            'content': 'Never invest without thorough research. Visit locations, talk to experts, verify all claims, check references.'
        },
        {
            'title': 'Cash Flow is King',
            'content': 'Focus on investments that generate regular cash flow. Monthly profits are better than one-time gains.'
        },
        {
            'title': 'Start Small, Scale Smart',
            'content': 'Test with minimum viable investment. Prove the model works, then scale up with confidence.'
        },
        {
            'title': 'Know Your Exit Strategy',
            'content': 'Before investing, know how and when you can exit. What if it doesn\'t work? How do you recover capital?'
        }
    ]
    
    for principle in principles:
        with st.expander(f"📖 {principle['title']}"):
            st.write(principle['content'])
    
    st.markdown("## 📊 Case Studies")
    
    st.info("Coming soon: Real case studies from successful Khula Collective investments with actual numbers and lessons learned.")

if __name__ == "__main__":
    main()