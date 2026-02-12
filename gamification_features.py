"""
Gamification Features for Khula Collective
Adds badges, achievements, challenges, and rewards to increase engagement
"""

from datetime import datetime, timedelta
from typing import List, Dict

class GamificationSystem:
    """Manages badges, achievements, and rewards"""
    
    def __init__(self):
        self.badges = self._initialize_badges()
        self.challenges = self._initialize_challenges()
        self.levels = self._initialize_levels()
    
    def _initialize_badges(self) -> Dict:
        """Define all available badges"""
        return {
            # Contribution Badges
            'first_contribution': {
                'name': '🌱 First Step',
                'description': 'Made your first R300 contribution',
                'points': 10,
                'rarity': 'common'
            },
            'consistent_3': {
                'name': '🔥 3-Month Streak',
                'description': 'Contributed for 3 consecutive months',
                'points': 25,
                'rarity': 'common'
            },
            'consistent_6': {
                'name': '💪 Half-Year Hero',
                'description': 'Contributed for 6 consecutive months',
                'points': 50,
                'rarity': 'uncommon'
            },
            'consistent_12': {
                'name': '👑 Year-Long Champion',
                'description': 'Contributed for 12 consecutive months',
                'points': 100,
                'rarity': 'rare'
            },
            'perfect_year': {
                'name': '💎 Perfect Year',
                'description': 'Never missed a payment for 12 months',
                'points': 200,
                'rarity': 'epic'
            },
            
            # Savings Milestones
            'saver_1k': {
                'name': '💰 First Thousand',
                'description': 'Saved your first R1,000',
                'points': 15,
                'rarity': 'common'
            },
            'saver_5k': {
                'name': '🎯 Five Grand',
                'description': 'Reached R5,000 in savings',
                'points': 40,
                'rarity': 'uncommon'
            },
            'saver_10k': {
                'name': '🚀 Ten Thousand Club',
                'description': 'Achieved R10,000 in savings',
                'points': 75,
                'rarity': 'rare'
            },
            'goal_achiever': {
                'name': '🏆 Goal Crusher',
                'description': 'Reached your yearly savings goal',
                'points': 150,
                'rarity': 'epic'
            },
            'over_achiever': {
                'name': '⭐ Over-Achiever',
                'description': 'Exceeded your yearly goal by 20%',
                'points': 250,
                'rarity': 'legendary'
            },
            
            # Community Badges
            'early_adopter': {
                'name': '🌟 Early Adopter',
                'description': 'Joined in the first month',
                'points': 50,
                'rarity': 'rare'
            },
            'referral_1': {
                'name': '🤝 Friend Bringer',
                'description': 'Referred your first member',
                'points': 30,
                'rarity': 'uncommon'
            },
            'referral_5': {
                'name': '🌍 Community Builder',
                'description': 'Referred 5 members',
                'points': 100,
                'rarity': 'epic'
            },
            'referral_10': {
                'name': '👑 Khula Ambassador',
                'description': 'Referred 10+ members',
                'points': 300,
                'rarity': 'legendary'
            },
            'top_3': {
                'name': '🥉 Top 3 Saver',
                'description': 'Ranked in top 3 for the month',
                'points': 40,
                'rarity': 'uncommon'
            },
            'number_1': {
                'name': '🥇 #1 Saver',
                'description': 'Ranked #1 for the month',
                'points': 75,
                'rarity': 'rare'
            },
            
            # Engagement Badges
            'dashboard_explorer': {
                'name': '🔍 Dashboard Explorer',
                'description': 'Logged in 10 times',
                'points': 10,
                'rarity': 'common'
            },
            'active_member': {
                'name': '⚡ Active Member',
                'description': 'Logged in 50 times',
                'points': 30,
                'rarity': 'uncommon'
            },
            'super_active': {
                'name': '🔥 Super Active',
                'description': 'Logged in 100 times',
                'points': 60,
                'rarity': 'rare'
            },
            'feedback_giver': {
                'name': '💬 Voice of Khula',
                'description': 'Provided valuable feedback',
                'points': 25,
                'rarity': 'uncommon'
            },
            
            # Special Badges
            'founding_member': {
                'name': '🏛️ Founding Member',
                'description': 'One of the first 20 members',
                'points': 100,
                'rarity': 'legendary'
            },
            'milestone_witness': {
                'name': '🎉 Milestone Witness',
                'description': 'Present when collective hit major milestone',
                'points': 50,
                'rarity': 'rare'
            },
            'constitution_signer': {
                'name': '📜 Constitution Signer',
                'description': 'Signed the Khula constitution',
                'points': 20,
                'rarity': 'common'
            },
            'fica_verified': {
                'name': '✅ FICA Verified',
                'description': 'Completed FICA verification',
                'points': 15,
                'rarity': 'common'
            }
        }
    
    def _initialize_challenges(self) -> Dict:
        """Define monthly and special challenges"""
        return {
            'monthly': [
                {
                    'id': 'perfect_month',
                    'name': 'Perfect Month Challenge',
                    'description': 'Contribute on time this month',
                    'reward': 50,
                    'badge': 'monthly_perfect'
                },
                {
                    'id': 'early_bird',
                    'name': 'Early Bird',
                    'description': 'Contribute before the 20th',
                    'reward': 25,
                    'badge': 'early_bird'
                },
                {
                    'id': 'double_up',
                    'name': 'Double Up',
                    'description': 'Contribute R600 this month',
                    'reward': 75,
                    'badge': 'double_contributor'
                }
            ],
            'quarterly': [
                {
                    'id': 'quarter_perfect',
                    'name': 'Perfect Quarter',
                    'description': 'No missed payments for 3 months',
                    'reward': 150,
                    'badge': 'quarterly_champion'
                },
                {
                    'id': 'growth_spurt',
                    'name': 'Growth Spurt',
                    'description': 'Increase savings by 20% this quarter',
                    'reward': 100,
                    'badge': 'growth_champion'
                }
            ],
            'special': [
                {
                    'id': 'birthday_bonus',
                    'name': 'Birthday Bonus',
                    'description': 'Contribute on your birthday month',
                    'reward': 50,
                    'badge': 'birthday_saver'
                },
                {
                    'id': 'new_year_boost',
                    'name': 'New Year Boost',
                    'description': 'Contribute in January',
                    'reward': 100,
                    'badge': 'new_year_champion'
                },
                {
                    'id': 'anniversary',
                    'name': 'Anniversary Celebration',
                    'description': 'Active for 1 year',
                    'reward': 200,
                    'badge': 'anniversary_member'
                }
            ]
        }
    
    def _initialize_levels(self) -> List[Dict]:
        """Define member levels based on points"""
        return [
            {'level': 1, 'name': '🌱 Seedling', 'points_required': 0, 'perks': ['Basic dashboard access']},
            {'level': 2, 'name': '🌿 Sprout', 'points_required': 100, 'perks': ['Custom profile picture', 'Monthly newsletter']},
            {'level': 3, 'name': '🪴 Growing Plant', 'points_required': 250, 'perks': ['Priority support', 'Early feature access']},
            {'level': 4, 'name': '🌳 Strong Tree', 'points_required': 500, 'perks': ['VIP badge', 'Exclusive webinars', 'Investment insights']},
            {'level': 5, 'name': '🏆 Forest Guardian', 'points_required': 1000, 'perks': ['Lifetime VIP', 'Advisory board seat', 'Profit sharing bonus']},
            {'level': 6, 'name': '👑 Khula Legend', 'points_required': 2000, 'perks': ['All perks', 'Founding member status', 'Special recognition']}
        ]
    
    def calculate_member_level(self, total_points: int) -> Dict:
        """Calculate member's current level"""
        current_level = self.levels[0]
        for level in self.levels:
            if total_points >= level['points_required']:
                current_level = level
            else:
                break
        
        # Calculate progress to next level
        next_level_index = self.levels.index(current_level) + 1
        if next_level_index < len(self.levels):
            next_level = self.levels[next_level_index]
            points_to_next = next_level['points_required'] - total_points
            progress_percentage = ((total_points - current_level['points_required']) / 
                                  (next_level['points_required'] - current_level['points_required'])) * 100
        else:
            next_level = None
            points_to_next = 0
            progress_percentage = 100
        
        return {
            'current_level': current_level,
            'next_level': next_level,
            'points_to_next': points_to_next,
            'progress_percentage': progress_percentage
        }
    
    def check_earned_badges(self, member_data: Dict) -> List[str]:
        """Check which badges a member has earned"""
        earned = []
        
        # Check contribution badges
        if member_data.get('total_contributions', 0) >= 1:
            earned.append('first_contribution')
        
        consecutive_months = member_data.get('consecutive_months', 0)
        if consecutive_months >= 3:
            earned.append('consistent_3')
        if consecutive_months >= 6:
            earned.append('consistent_6')
        if consecutive_months >= 12:
            earned.append('consistent_12')
        
        # Check savings milestones
        total_saved = member_data.get('total_saved', 0)
        if total_saved >= 1000:
            earned.append('saver_1k')
        if total_saved >= 5000:
            earned.append('saver_5k')
        if total_saved >= 10000:
            earned.append('saver_10k')
        
        # Check goal achievement
        yearly_goal = member_data.get('yearly_goal', 3600)
        if total_saved >= yearly_goal:
            earned.append('goal_achiever')
        if total_saved >= yearly_goal * 1.2:
            earned.append('over_achiever')
        
        # Check community badges
        referrals = member_data.get('referrals', 0)
        if referrals >= 1:
            earned.append('referral_1')
        if referrals >= 5:
            earned.append('referral_5')
        if referrals >= 10:
            earned.append('referral_10')
        
        # Check ranking
        rank = member_data.get('rank', 999)
        if rank <= 3:
            earned.append('top_3')
        if rank == 1:
            earned.append('number_1')
        
        # Check engagement
        login_count = member_data.get('login_count', 0)
        if login_count >= 10:
            earned.append('dashboard_explorer')
        if login_count >= 50:
            earned.append('active_member')
        if login_count >= 100:
            earned.append('super_active')
        
        # Check special badges
        if member_data.get('is_founding_member', False):
            earned.append('founding_member')
        if member_data.get('constitution_signed', False):
            earned.append('constitution_signer')
        if member_data.get('fica_verified', False):
            earned.append('fica_verified')
        
        return earned
    
    def get_leaderboard_with_levels(self, members: List[Dict]) -> List[Dict]:
        """Generate leaderboard with levels and badges"""
        leaderboard = []
        
        for member in members:
            total_points = member.get('total_points', 0)
            level_info = self.calculate_member_level(total_points)
            earned_badges = self.check_earned_badges(member)
            
            leaderboard.append({
                'username': member['username'],
                'full_name': member['full_name'],
                'total_saved': member['total_saved'],
                'rank': member['rank'],
                'level': level_info['current_level']['name'],
                'total_points': total_points,
                'badges_count': len(earned_badges),
                'top_badges': earned_badges[:3]  # Show top 3 badges
            })
        
        return sorted(leaderboard, key=lambda x: x['total_saved'], reverse=True)

class AchievementNotifier:
    """Handles achievement notifications"""
    
    @staticmethod
    def create_badge_notification(badge_info: Dict) -> str:
        """Create notification message for new badge"""
        rarity_colors = {
            'common': '⚪',
            'uncommon': '🟢',
            'rare': '🔵',
            'epic': '🟣',
            'legendary': '🟡'
        }
        
        color = rarity_colors.get(badge_info['rarity'], '⚪')
        
        return f"""
🎉 **NEW BADGE UNLOCKED!** 🎉

{badge_info['name']} {color}

{badge_info['description']}

**Points Earned:** +{badge_info['points']}
**Rarity:** {badge_info['rarity'].title()}

Keep up the great work! 💪
        """
    
    @staticmethod
    def create_level_up_notification(old_level: Dict, new_level: Dict) -> str:
        """Create notification for level up"""
        return f"""
🎊 **LEVEL UP!** 🎊

You've advanced from {old_level['name']} to {new_level['name']}!

**New Perks Unlocked:**
{chr(10).join(f"✨ {perk}" for perk in new_level['perks'])}

**Points Required for Next Level:** {new_level.get('points_to_next', 'MAX LEVEL')}

You're crushing it! 🚀
        """
    
    @staticmethod
    def create_challenge_completion(challenge: Dict) -> str:
        """Create notification for challenge completion"""
        return f"""
🏆 **CHALLENGE COMPLETED!** 🏆

{challenge['name']}

{challenge['description']}

**Reward:** +{challenge['reward']} points
**Badge Earned:** {challenge.get('badge', 'N/A')}

Ready for the next challenge? 💪
        """

# Seasonal Events
SEASONAL_EVENTS = {
    'january': {
        'name': 'New Year, New Wealth',
        'bonus_multiplier': 1.5,
        'special_challenges': ['new_year_boost'],
        'theme_color': '#FFD700'
    },
    'june': {
        'name': 'Mid-Year Momentum',
        'bonus_multiplier': 1.25,
        'special_challenges': ['half_year_hero'],
        'theme_color': '#4169E1'
    },
    'december': {
        'name': 'Year-End Push',
        'bonus_multiplier': 2.0,
        'special_challenges': ['year_end_champion'],
        'theme_color': '#DC143C'
    }
}

# Reward Tiers
REWARD_TIERS = {
    'bronze': {
        'points_range': (0, 249),
        'color': '#CD7F32',
        'benefits': ['Basic dashboard', 'Monthly newsletter']
    },
    'silver': {
        'points_range': (250, 499),
        'color': '#C0C0C0',
        'benefits': ['Priority support', 'Custom profile', 'Early features']
    },
    'gold': {
        'points_range': (500, 999),
        'color': '#FFD700',
        'benefits': ['VIP badge', 'Exclusive webinars', 'Investment insights']
    },
    'platinum': {
        'points_range': (1000, 1999),
        'color': '#E5E4E2',
        'benefits': ['Lifetime VIP', 'Advisory board', 'Profit sharing']
    },
    'diamond': {
        'points_range': (2000, float('inf')),
        'color': '#B9F2FF',
        'benefits': ['All perks', 'Founding status', 'Special recognition']
    }
}