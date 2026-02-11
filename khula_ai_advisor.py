"""
Khula Collective AI Investment Advisor
Provides investment suggestions based on total pool balance
"""

from typing import Dict, List
from datetime import datetime


class KhulaAIAdvisor:
    """AI-powered investment advisor for Khula Collective"""
    
    def __init__(self):
        """Initialize AI advisor with investment options"""
        self.investment_options = {
            'rsa_retail_bonds': {
                'name': 'RSA Retail Savings Bonds',
                'min_amount': 1000,
                'expected_return': 7.75,
                'risk_level': 'Low',
                'term': '2-5 years',
                'description': 'Government-backed bonds with guaranteed returns. Ideal for capital preservation.'
            },
            'money_market': {
                'name': 'Money Market Unit Trust',
                'min_amount': 1000,
                'expected_return': 8.5,
                'risk_level': 'Low',
                'term': 'Flexible',
                'description': 'Liquid investment with daily access. Good for emergency funds.'
            },
            'etf_satrix40': {
                'name': 'Satrix 40 ETF (Top 40 JSE)',
                'min_amount': 500,
                'expected_return': 12.0,
                'risk_level': 'Medium',
                'term': '3+ years',
                'description': 'Tracks top 40 JSE companies. Good for long-term growth.'
            },
            'etf_property': {
                'name': 'Property ETF (REIT)',
                'min_amount': 500,
                'expected_return': 10.5,
                'risk_level': 'Medium',
                'term': '3+ years',
                'description': 'Real estate exposure through listed property funds.'
            },
            'tfsa': {
                'name': 'Tax-Free Savings Account',
                'min_amount': 500,
                'expected_return': 9.0,
                'risk_level': 'Low-Medium',
                'term': 'Long-term',
                'description': 'Tax-free growth up to R36,000/year. Excellent for long-term savings.'
            }
        }
    
    def suggest_investments(self, current_balance: float, risk_level: str = 'Medium') -> Dict:
        """
        Generate investment suggestions based on current balance and risk level
        
        Args:
            current_balance: Total collective savings
            risk_level: 'Low', 'Medium', or 'High'
            
        Returns:
            Dictionary with investment suggestions
        """
        suggestions = {
            'current_balance': current_balance,
            'risk_level': risk_level,
            'recommendations': [],
            'allocation': {},
            'expected_annual_return': 0,
            'summary': ''
        }
        
        # Balance thresholds and strategies
        if current_balance < 10000:
            suggestions['recommendations'].append({
                'action': 'Continue Saving',
                'reason': 'Build emergency fund first',
                'target': 'R10,000',
                'timeline': 'Next 3-6 months'
            })
            suggestions['summary'] = f"""
**Current Balance: R{current_balance:,.2f}**

**Strategy: Build Foundation**

Your collective is in the early stages. Focus on:
1. Consistent R300/month contributions from all members
2. Building emergency fund to R10,000
3. Maintaining 100% payment compliance

**Next Milestone: R10,000** - Then we can start investing!
            """
        
        elif current_balance < 50000:
            # Small balance: Focus on liquid, low-risk options
            if risk_level == 'Low':
                suggestions['allocation'] = {
                    'Money Market': 70,
                    'RSA Retail Bonds': 30
                }
                suggestions['recommendations'].append({
                    'investment': 'Money Market Unit Trust',
                    'amount': current_balance * 0.70,
                    'expected_return': 8.5,
                    'reason': 'Liquid and safe for growing capital'
                })
                suggestions['recommendations'].append({
                    'investment': 'RSA Retail Savings Bonds',
                    'amount': current_balance * 0.30,
                    'expected_return': 7.75,
                    'reason': 'Government-backed security'
                })
                suggestions['expected_annual_return'] = 8.28
            
            else:  # Medium or High
                suggestions['allocation'] = {
                    'Money Market': 50,
                    'ETF (Satrix 40)': 30,
                    'RSA Retail Bonds': 20
                }
                suggestions['recommendations'].append({
                    'investment': 'Money Market Unit Trust',
                    'amount': current_balance * 0.50,
                    'expected_return': 8.5,
                    'reason': 'Maintain liquidity'
                })
                suggestions['recommendations'].append({
                    'investment': 'Satrix 40 ETF',
                    'amount': current_balance * 0.30,
                    'expected_return': 12.0,
                    'reason': 'Growth potential'
                })
                suggestions['recommendations'].append({
                    'investment': 'RSA Retail Bonds',
                    'amount': current_balance * 0.20,
                    'expected_return': 7.75,
                    'reason': 'Stability'
                })
                suggestions['expected_annual_return'] = 9.48
            
            suggestions['summary'] = f"""
**Current Balance: R{current_balance:,.2f}**

**Strategy: Balanced Growth**

Recommended allocation:
{self._format_allocation(suggestions['allocation'])}

**Expected Annual Return: {suggestions['expected_annual_return']:.2f}%**

**Action Steps:**
1. Open accounts with recommended providers
2. Diversify to reduce risk
3. Continue monthly contributions
4. Review quarterly

**Next Milestone: R50,000** - Unlock more investment options!
            """
        
        elif current_balance < 80000:
            # Medium balance: R50k-80k milestone
            if risk_level == 'Low':
                suggestions['allocation'] = {
                    'RSA Retail Bonds': 50,
                    'Money Market': 30,
                    'TFSA': 20
                }
                suggestions['recommendations'].append({
                    'investment': 'RSA Retail Top-Up Bonds',
                    'amount': 50000,
                    'expected_return': 7.75,
                    'reason': '🎯 MILESTONE: Protect R50k against inflation'
                })
                suggestions['recommendations'].append({
                    'investment': 'Money Market',
                    'amount': current_balance * 0.30,
                    'expected_return': 8.5,
                    'reason': 'Emergency liquidity'
                })
                suggestions['recommendations'].append({
                    'investment': 'Tax-Free Savings',
                    'amount': current_balance * 0.20,
                    'expected_return': 9.0,
                    'reason': 'Tax-efficient growth'
                })
                suggestions['expected_annual_return'] = 8.23
            
            elif risk_level == 'Medium':
                suggestions['allocation'] = {
                    'RSA Retail Bonds': 40,
                    'ETF (Satrix 40)': 30,
                    'Money Market': 20,
                    'TFSA': 10
                }
                suggestions['recommendations'].append({
                    'investment': 'RSA Retail Bonds',
                    'amount': 50000,
                    'expected_return': 7.75,
                    'reason': '🎯 MILESTONE: Secure foundation'
                })
                suggestions['recommendations'].append({
                    'investment': 'Satrix 40 ETF',
                    'amount': current_balance * 0.30,
                    'expected_return': 12.0,
                    'reason': 'Growth exposure'
                })
                suggestions['recommendations'].append({
                    'investment': 'Money Market',
                    'amount': current_balance * 0.20,
                    'expected_return': 8.5,
                    'reason': 'Liquidity buffer'
                })
                suggestions['recommendations'].append({
                    'investment': 'TFSA',
                    'amount': current_balance * 0.10,
                    'expected_return': 9.0,
                    'reason': 'Tax benefits'
                })
                suggestions['expected_annual_return'] = 9.28
            
            else:  # High risk
                suggestions['allocation'] = {
                    'ETF (Satrix 40)': 40,
                    'RSA Retail Bonds': 30,
                    'Property ETF': 20,
                    'Money Market': 10
                }
                suggestions['recommendations'].append({
                    'investment': 'Satrix 40 ETF',
                    'amount': current_balance * 0.40,
                    'expected_return': 12.0,
                    'reason': 'Maximum growth'
                })
                suggestions['recommendations'].append({
                    'investment': 'RSA Retail Bonds',
                    'amount': current_balance * 0.30,
                    'expected_return': 7.75,
                    'reason': 'Stability anchor'
                })
                suggestions['recommendations'].append({
                    'investment': 'Property ETF',
                    'amount': current_balance * 0.20,
                    'expected_return': 10.5,
                    'reason': 'Diversification'
                })
                suggestions['recommendations'].append({
                    'investment': 'Money Market',
                    'amount': current_balance * 0.10,
                    'expected_return': 8.5,
                    'reason': 'Emergency fund'
                })
                suggestions['expected_annual_return'] = 10.33
            
            suggestions['summary'] = f"""
**Current Balance: R{current_balance:,.2f}**

**🎉 MILESTONE REACHED: R50,000+**

**Strategy: Diversified Portfolio**

The Khula AI suggests moving **R50,000** into RSA Retail Top-Up Bonds at 7.75% interest to protect capital against inflation. The remaining liquidity should be diversified.

Recommended allocation:
{self._format_allocation(suggestions['allocation'])}

**Expected Annual Return: {suggestions['expected_annual_return']:.2f}%**
**Projected Growth (1 year): R{current_balance * suggestions['expected_annual_return'] / 100:,.2f}**

**Action Steps:**
1. ✅ Invest R50k in RSA Retail Bonds (Priority)
2. Diversify remaining funds as recommended
3. Set up automatic monthly contributions
4. Schedule quarterly review meeting

**Next Milestone: R80,000** - Advanced diversification options!
            """
        
        else:  # R80,000+
            # Large balance: Full diversification
            if risk_level == 'Low':
                suggestions['allocation'] = {
                    'RSA Retail Bonds': 45,
                    'Money Market': 25,
                    'TFSA': 20,
                    'Property ETF': 10
                }
                suggestions['expected_annual_return'] = 8.54
            
            elif risk_level == 'Medium':
                suggestions['allocation'] = {
                    'RSA Retail Bonds': 30,
                    'ETF (Satrix 40)': 30,
                    'Money Market': 20,
                    'TFSA': 15,
                    'Property ETF': 5
                }
                suggestions['expected_annual_return'] = 9.68
            
            else:  # High risk
                suggestions['allocation'] = {
                    'ETF (Satrix 40)': 45,
                    'Property ETF': 20,
                    'RSA Retail Bonds': 20,
                    'TFSA': 10,
                    'Money Market': 5
                }
                suggestions['expected_annual_return'] = 10.74
            
            # Generate detailed recommendations
            for investment, percentage in suggestions['allocation'].items():
                amount = current_balance * (percentage / 100)
                inv_key = self._get_investment_key(investment)
                if inv_key:
                    inv_info = self.investment_options[inv_key]
                    suggestions['recommendations'].append({
                        'investment': investment,
                        'amount': amount,
                        'percentage': percentage,
                        'expected_return': inv_info['expected_return'],
                        'reason': inv_info['description']
                    })
            
            suggestions['summary'] = f"""
**Current Balance: R{current_balance:,.2f}**

**🎉🎉 MILESTONE: R80,000+ ACHIEVED!**

**Strategy: Advanced Diversification**

Your collective has reached a significant milestone! Time for sophisticated portfolio management.

Recommended allocation:
{self._format_allocation(suggestions['allocation'])}

**Expected Annual Return: {suggestions['expected_annual_return']:.2f}%**
**Projected Growth (1 year): R{current_balance * suggestions['expected_annual_return'] / 100:,.2f}**
**Projected Balance (1 year): R{current_balance + (current_balance * suggestions['expected_annual_return'] / 100):,.2f}**

**Action Steps:**
1. ✅ Maintain R50k in RSA Retail Bonds (Foundation)
2. Diversify into Money Market for liquidity
3. Add ETF exposure for growth
4. Consider property ETFs for diversification
5. Maximize TFSA contributions (R36k/year limit)
6. Schedule professional financial advisor consultation

**Next Milestone: R100,000** - Consider unit trusts and offshore exposure!
            """
        
        return suggestions
    
    def _format_allocation(self, allocation: Dict) -> str:
        """Format allocation dictionary as string"""
        lines = []
        for investment, percentage in allocation.items():
            lines.append(f"  • {investment}: {percentage}%")
        return "\n".join(lines)
    
    def _get_investment_key(self, investment_name: str) -> str:
        """Get investment key from name"""
        mapping = {
            'RSA Retail Bonds': 'rsa_retail_bonds',
            'Money Market': 'money_market',
            'ETF (Satrix 40)': 'etf_satrix40',
            'Property ETF': 'etf_property',
            'TFSA': 'tfsa'
        }
        return mapping.get(investment_name)
    
    def generate_monthly_report(self, current_balance: float, risk_level: str,
                               month: str, year: int) -> str:
        """Generate monthly investment report"""
        suggestions = self.suggest_investments(current_balance, risk_level)
        
        report = f"""
# KHULA COLLECTIVE - MONTHLY INVESTMENT REPORT
## {month} {year}

---

### 💰 Current Financial Position
- **Total Collective Balance:** R{current_balance:,.2f}
- **Risk Profile:** {risk_level}
- **Expected Annual Return:** {suggestions['expected_annual_return']:.2f}%

---

### 🎯 AI Investment Recommendations

{suggestions['summary']}

---

### 📊 Detailed Allocation

"""
        
        for rec in suggestions['recommendations']:
            report += f"""
**{rec['investment']}**
- Amount: R{rec['amount']:,.2f}
- Expected Return: {rec['expected_return']:.2f}%
- Reason: {rec['reason']}

"""
        
        report += f"""
---

### 📈 Projected Returns

**Conservative Estimate (1 Year):**
- Investment: R{current_balance:,.2f}
- Return: R{current_balance * suggestions['expected_annual_return'] / 100:,.2f}
- Total: R{current_balance + (current_balance * suggestions['expected_annual_return'] / 100):,.2f}

**With Continued Contributions (R300/member/month):**
- Additional Contributions: R{300 * 20 * 12:,.2f}
- Total After 1 Year: R{current_balance + (current_balance * suggestions['expected_annual_return'] / 100) + (300 * 20 * 12):,.2f}

---

### ⚠️ Important Notes

1. **Past performance does not guarantee future returns**
2. **All investments carry risk** - diversification reduces but doesn't eliminate risk
3. **Consult a certified financial advisor** before making major investment decisions
4. **Maintain emergency fund** - keep 3-6 months expenses liquid
5. **Review quarterly** - adjust strategy based on performance and goals

---

### 📞 Next Steps

1. Schedule group meeting to discuss recommendations
2. Vote on investment allocation (60% approval required)
3. Open necessary investment accounts
4. Execute investment strategy
5. Set up automatic monthly contributions
6. Schedule quarterly review

---

*This report is generated by Khula AI Advisor and is for informational purposes only. 
Always consult with a qualified financial advisor before making investment decisions.*

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return report
    
    def get_whatsapp_investment_alert(self, current_balance: float, 
                                     milestone: str) -> str:
        """Generate WhatsApp message for investment milestone"""
        if milestone == '50k':
            return f"""
🎉 *KHULA COLLECTIVE MILESTONE!*

We've hit *R{current_balance:,.2f}*! 🇿🇦

💡 *AI Recommendation:*
Move R50,000 into RSA Retail Bonds at 7.75% to protect our capital against inflation.

📊 *Expected Return:* R3,875/year

👉 Check the app for full investment report!

_Khula AI Advisor_
            """
        elif milestone == '80k':
            return f"""
🎉🎉 *MAJOR MILESTONE ACHIEVED!*

Khula Collective: *R{current_balance:,.2f}*! 🚀

💡 *AI Recommendation:*
Time to diversify! Consider:
• Money Market Unit Trusts
• EasyEquities ETFs
• Property ETFs

📊 *Projected Growth:* 9-11% annually

👉 Full report available in the app!

_Khula AI Advisor_
            """
        else:
            return f"""
📊 *Khula Collective Update*

Current Balance: *R{current_balance:,.2f}*

Keep up the great work! 💪

_Khula AI Advisor_
            """