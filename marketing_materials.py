"""
Marketing Materials Generator for Khula Collective
Creates shareable social media graphics, flyers, and promotional content
"""

import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io

def create_social_media_graphics():
    """Generate social media graphics for promotion"""
    
    graphics = {
        'instagram_post': {
            'size': (1080, 1080),
            'content': [
                {
                    'type': 'hero',
                    'title': 'Start Building Wealth',
                    'subtitle': 'With Just R300/Month',
                    'cta': 'Join Khula Collective Today'
                }
            ]
        },
        'facebook_cover': {
            'size': (820, 312),
            'content': [
                {
                    'type': 'banner',
                    'title': 'Khula Collective',
                    'tagline': 'Grow Together, Prosper Together'
                }
            ]
        },
        'whatsapp_status': {
            'size': (1080, 1920),
            'content': [
                {
                    'type': 'story',
                    'stat': 'R71,700',
                    'label': 'Total Pot',
                    'message': 'Join 20+ members building wealth together'
                }
            ]
        }
    }
    
    return graphics

def create_comparison_chart():
    """Create solo vs collective investment comparison"""
    
    years = list(range(1, 11))
    
    # Solo savings (just contributions, no returns)
    solo_savings = [300 * 12 * year for year in years]
    
    # Collective with 9% returns
    collective_savings = []
    for year in years:
        months = year * 12
        monthly_rate = 0.09 / 12
        fv = 300 * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        collective_savings.append(fv)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=solo_savings,
        name='Solo Savings (0% return)',
        line=dict(color='#ff6b6b', width=3, dash='dash'),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=collective_savings,
        name='Khula Collective (9% return)',
        line=dict(color='#51cf66', width=4),
        fill='tozeroy',
        fillcolor='rgba(81, 207, 102, 0.3)'
    ))
    
    # Add annotations for key milestones
    fig.add_annotation(
        x=5,
        y=collective_savings[4],
        text=f"R{collective_savings[4]:,.0f}<br>vs R{solo_savings[4]:,.0f}",
        showarrow=True,
        arrowhead=2,
        bgcolor='#51cf66',
        font=dict(color='white', size=12)
    )
    
    fig.add_annotation(
        x=10,
        y=collective_savings[9],
        text=f"R{collective_savings[9]:,.0f}<br>vs R{solo_savings[9]:,.0f}",
        showarrow=True,
        arrowhead=2,
        bgcolor='#51cf66',
        font=dict(color='white', size=12)
    )
    
    fig.update_layout(
        title={
            'text': 'Solo Savings vs Khula Collective<br><sub>The Power of Collective Investing</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24}
        },
        xaxis_title='Years',
        yaxis_title='Total Value (R)',
        hovermode='x unified',
        height=500,
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_milestone_timeline():
    """Create visual milestone timeline"""
    
    milestones = [
        {'amount': 10000, 'title': 'Foundation', 'benefit': 'Money Market Access', 'return': '7.5%'},
        {'amount': 30000, 'title': 'Growth', 'benefit': 'ETF Investments', 'return': '8-9%'},
        {'amount': 50000, 'title': 'Expansion', 'benefit': 'RSA Retail Bonds', 'return': '8.25%'},
        {'amount': 80000, 'title': 'Diversification', 'benefit': 'Full Portfolio', 'return': '9-11%'},
        {'amount': 100000, 'title': 'Prosperity', 'benefit': 'International ETFs', 'return': '10-12%'}
    ]
    
    fig = go.Figure()
    
    # Create timeline
    amounts = [m['amount'] for m in milestones]
    titles = [m['title'] for m in milestones]
    benefits = [m['benefit'] for m in milestones]
    returns = [m['return'] for m in milestones]
    
    fig.add_trace(go.Scatter(
        x=amounts,
        y=[1]*len(amounts),
        mode='markers+text',
        marker=dict(
            size=40,
            color=['#667eea', '#51cf66', '#ffd43b', '#ff6b6b', '#845ef7'],
            line=dict(color='white', width=3)
        ),
        text=[f"R{a/1000:.0f}k" for a in amounts],
        textposition='middle center',
        textfont=dict(color='white', size=12, family='Arial Black'),
        hovertemplate='<b>%{text}</b><br>%{customdata[0]}<br>%{customdata[1]}<br>Expected Return: %{customdata[2]}<extra></extra>',
        customdata=[[titles[i], benefits[i], returns[i]] for i in range(len(milestones))],
        showlegend=False
    ))
    
    # Add connecting line
    fig.add_trace(go.Scatter(
        x=amounts,
        y=[1]*len(amounts),
        mode='lines',
        line=dict(color='#dee2e6', width=4),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add labels below
    for i, milestone in enumerate(milestones):
        fig.add_annotation(
            x=milestone['amount'],
            y=0.85,
            text=f"<b>{milestone['title']}</b><br>{milestone['benefit']}<br><i>{milestone['return']} return</i>",
            showarrow=False,
            font=dict(size=10),
            align='center'
        )
    
    fig.update_layout(
        title={
            'text': 'Your Investment Journey with Khula Collective',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis=dict(
            title='Total Collective Pot (R)',
            showgrid=False,
            zeroline=False,
            range=[0, 110000]
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0.7, 1.3]
        ),
        height=400,
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig

def create_referral_program_details():
    """Create referral program structure"""
    
    program = {
        'title': '🎁 Refer & Earn Program',
        'tagline': 'Grow the collective, grow your rewards',
        'tiers': [
            {
                'referrals': 1,
                'reward': 'R50 bonus contribution',
                'badge': '🌱 Seed Planter'
            },
            {
                'referrals': 3,
                'reward': 'R200 bonus + Priority support',
                'badge': '🌿 Growth Champion'
            },
            {
                'referrals': 5,
                'reward': 'R500 bonus + VIP status',
                'badge': '🌳 Community Builder'
            },
            {
                'referrals': 10,
                'reward': 'R1,500 bonus + Lifetime VIP',
                'badge': '👑 Khula Ambassador'
            }
        ],
        'how_it_works': [
            'Share your unique referral link',
            'Friend joins and makes first contribution',
            'You both receive rewards',
            'Track referrals in your dashboard'
        ],
        'terms': [
            'Referred member must complete FICA verification',
            'Rewards credited after first successful contribution',
            'No limit on number of referrals',
            'Rewards can be withdrawn or reinvested'
        ]
    }
    
    return program

def create_email_templates():
    """Create email marketing templates"""
    
    templates = {
        'welcome': {
            'subject': '🌱 Welcome to Khula Collective - Your Wealth Journey Begins!',
            'body': '''
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; color: white;">
                    <h1>Welcome to Khula Collective! 🎉</h1>
                    <p style="font-size: 18px;">Your wealth-building journey starts today</p>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa;">
                    <h2>What Happens Next?</h2>
                    
                    <div style="background: white; padding: 20px; margin: 20px 0; border-radius: 10px;">
                        <h3>✅ Step 1: Complete Your Profile</h3>
                        <p>Finish your FICA verification to unlock all features</p>
                    </div>
                    
                    <div style="background: white; padding: 20px; margin: 20px 0; border-radius: 10px;">
                        <h3>💰 Step 2: Make Your First Contribution</h3>
                        <p>Start with R300 and watch your savings grow</p>
                    </div>
                    
                    <div style="background: white; padding: 20px; margin: 20px 0; border-radius: 10px;">
                        <h3>📊 Step 3: Track Your Progress</h3>
                        <p>Access your personal dashboard and community stats</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="#" style="background: #667eea; color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: bold;">
                            Access Your Dashboard
                        </a>
                    </div>
                    
                    <h2>Quick Stats</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div style="background: white; padding: 20px; text-align: center; border-radius: 10px;">
                            <h3 style="color: #667eea; margin: 0;">20+</h3>
                            <p style="margin: 5px 0;">Active Members</p>
                        </div>
                        <div style="background: white; padding: 20px; text-align: center; border-radius: 10px;">
                            <h3 style="color: #667eea; margin: 0;">R71,700</h3>
                            <p style="margin: 5px 0;">Total Pot</p>
                        </div>
                    </div>
                    
                    <h2 style="margin-top: 30px;">Need Help?</h2>
                    <p>Our support team is here for you:</p>
                    <ul>
                        <li>📧 Email: support@khula.co.za</li>
                        <li>📱 WhatsApp: +27 XX XXX XXXX</li>
                        <li>💬 Live Chat: Available in your dashboard</li>
                    </ul>
                </div>
                
                <div style="background: #343a40; color: white; padding: 20px; text-align: center;">
                    <p>Grow Together, Prosper Together</p>
                    <p style="font-size: 12px; opacity: 0.8;">© 2024 Khula Collective. All rights reserved.</p>
                </div>
            </body>
            </html>
            '''
        },
        'monthly_reminder': {
            'subject': '💰 Your Monthly Contribution is Due - Keep Growing!',
            'body': '''
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white;">
                    <h1>Monthly Contribution Reminder</h1>
                    <p style="font-size: 18px;">Keep your wealth-building momentum going!</p>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa;">
                    <h2>Hi [Member Name],</h2>
                    <p>Your R300 monthly contribution is due on the 25th. Don't break your streak!</p>
                    
                    <div style="background: white; padding: 25px; margin: 20px 0; border-radius: 10px; border-left: 5px solid #667eea;">
                        <h3>Your Progress This Year</h3>
                        <p><strong>Contributed:</strong> R[Amount]</p>
                        <p><strong>Goal:</strong> R3,600</p>
                        <p><strong>Progress:</strong> [X]%</p>
                        <div style="background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden;">
                            <div style="background: #667eea; height: 100%; width: [X]%;"></div>
                        </div>
                    </div>
                    
                    <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #155724;">🎯 Community Update</h3>
                        <p style="color: #155724;">The collective pot has grown to <strong>R[Total]</strong>!</p>
                        <p style="color: #155724;">We're R[Amount] away from our next milestone.</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="#" style="background: #667eea; color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: bold;">
                            Make Payment Now
                        </a>
                    </div>
                </div>
            </body>
            </html>
            '''
        },
        'milestone_achieved': {
            'subject': '🎉 Milestone Achieved! The Collective Just Hit R[Amount]!',
            'body': '''
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #51cf66 0%, #38d9a9 100%); padding: 40px; text-align: center; color: white;">
                    <h1>🎉 MILESTONE ACHIEVED! 🎉</h1>
                    <h2 style="font-size: 48px; margin: 20px 0;">R[Amount]</h2>
                    <p style="font-size: 20px;">The collective pot has reached a major milestone!</p>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa;">
                    <h2>Congratulations, Khula Family!</h2>
                    <p>Together, we've achieved something amazing. This milestone unlocks new investment opportunities!</p>
                    
                    <div style="background: white; padding: 25px; margin: 20px 0; border-radius: 10px;">
                        <h3>🚀 What This Means</h3>
                        <ul style="line-height: 2;">
                            <li>Access to [Investment Type]</li>
                            <li>Expected returns: [X]% annually</li>
                            <li>Diversified portfolio expansion</li>
                            <li>Lower risk, higher rewards</li>
                        </ul>
                    </div>
                    
                    <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3 style="color: #856404;">💡 AI Advisor Recommendation</h3>
                        <p style="color: #856404;">[Specific investment recommendation based on milestone]</p>
                    </div>
                    
                    <h3>Next Milestone: R[Next Amount]</h3>
                    <p>We're R[Difference] away from unlocking even more opportunities!</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="#" style="background: #51cf66; color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: bold;">
                            View Investment Strategy
                        </a>
                    </div>
                </div>
            </body>
            </html>
            '''
        }
    }
    
    return templates

def create_whatsapp_message_templates():
    """Create WhatsApp message templates"""
    
    templates = {
        'welcome': '''
🌱 *Welcome to Khula Collective!*

Hi [Name], your wealth journey starts today! 🎉

*Quick Start:*
✅ Complete FICA verification
💰 Make your first R300 contribution
📊 Access your dashboard

*Current Stats:*
👥 20+ active members
💵 R71,700 total pot
📈 8-11% expected returns

Need help? Reply to this message!

_Grow Together, Prosper Together_ 🌍
        ''',
        
        'payment_reminder': '''
💰 *Monthly Contribution Reminder*

Hi [Name]! Your R300 contribution is due on the 25th.

*Your Progress:*
✅ Contributed: R[Amount]
🎯 Goal: R3,600
📊 Progress: [X]%

Keep your streak going! 🔥

Pay now: [Payment Link]
        ''',
        
        'milestone': '''
🎉 *MILESTONE ACHIEVED!*

Khula Family, we did it! 🙌

💵 Total Pot: *R[Amount]*

This unlocks:
🚀 [Investment opportunity]
📈 [Expected returns]
💡 [AI recommendation]

View details: [Link]

_Together we prosper!_ 🌱
        ''',
        
        'leaderboard_update': '''
🏆 *Monthly Leaderboard Update*

Hi [Name]! Here's where you stand:

*Your Rank:* #[Rank] [Medal]
*Your Savings:* R[Amount]
*Progress:* [X]%

*Top 3:*
🥇 [Name] - R[Amount]
🥈 [Name] - R[Amount]
🥉 [Name] - R[Amount]

Keep climbing! 📈
        ''',
        
        'referral_reward': '''
🎁 *Referral Reward Unlocked!*

Congratulations [Name]! 🎉

Your friend [Friend Name] just joined Khula Collective!

*Your Reward:* R[Amount] bonus
*New Badge:* [Badge] [Emoji]

Keep referring, keep earning! 💰

Share your link: [Referral Link]
        '''
    }
    
    return templates

def create_printable_flyer_content():
    """Create content for printable marketing flyers"""
    
    flyer = {
        'headline': 'Start Building Wealth with Just R300/Month',
        'subheadline': 'Join Khula Collective - South Africa\'s Premier Investment Club',
        
        'key_benefits': [
            '💰 Low Entry: Start with R300/month',
            '📈 High Returns: 8-11% annually',
            '🤝 Collective Power: Pool resources for better opportunities',
            '🔒 FICA Compliant: Safe and secure',
            '🤖 AI Advisor: Personalized investment recommendations',
            '👥 Community: Learn and grow together'
        ],
        
        'how_it_works': [
            '1. Sign up online in 5 minutes',
            '2. Contribute R300 monthly',
            '3. Watch your wealth grow',
            '4. Access exclusive investment opportunities'
        ],
        
        'stats': {
            'members': '20+',
            'total_pot': 'R71,700',
            'avg_savings': 'R3,585',
            'returns': '8-11%'
        },
        
        'testimonial': {
            'text': '"I started 14 months ago with R300/month. Today I have R3,900 saved and learned so much about investing!"',
            'author': '- Thabo M., Top Saver'
        },
        
        'cta': {
            'primary': 'Join Now',
            'secondary': 'Learn More',
            'url': 'www.khulacollective.co.za',
            'qr_code': True
        },
        
        'contact': {
            'email': 'join@khula.co.za',
            'phone': '+27 XX XXX XXXX',
            'whatsapp': '+27 XX XXX XXXX'
        }
    }
    
    return flyer

# Export all marketing materials
MARKETING_MATERIALS = {
    'social_graphics': create_social_media_graphics(),
    'comparison_chart': create_comparison_chart(),
    'milestone_timeline': create_milestone_timeline(),
    'referral_program': create_referral_program_details(),
    'email_templates': create_email_templates(),
    'whatsapp_templates': create_whatsapp_message_templates(),
    'printable_flyer': create_printable_flyer_content()
}