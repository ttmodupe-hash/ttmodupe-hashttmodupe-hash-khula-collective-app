"""
Khula Collective WhatsApp Notification Module
Handles WhatsApp messaging via Twilio API
"""

from typing import List, Dict, Optional
from datetime import datetime
import os


class KhulaWhatsApp:
    """Manages WhatsApp notifications for Khula Collective"""
    
    def __init__(self, account_sid: str = None, auth_token: str = None, 
                 whatsapp_number: str = None):
        """
        Initialize WhatsApp client
        
        Args:
            account_sid: Twilio Account SID
            auth_token: Twilio Auth Token
            whatsapp_number: Twilio WhatsApp number (format: whatsapp:+27...)
        """
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = whatsapp_number or os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        # Initialize Twilio client if credentials available
        self.client = None
        if self.account_sid and self.auth_token:
            try:
                from twilio.rest import Client
                self.client = Client(self.account_sid, self.auth_token)
            except ImportError:
                print("⚠️  Twilio library not installed. Run: pip install twilio")
            except Exception as e:
                print(f"⚠️  Error initializing Twilio: {e}")
    
    def send_message(self, to_number: str, message: str) -> Dict:
        """
        Send WhatsApp message to a number
        
        Args:
            to_number: Recipient's WhatsApp number (format: +27...)
            message: Message content
            
        Returns:
            Dictionary with status and message SID
        """
        if not self.client:
            return {
                'success': False,
                'error': 'Twilio client not initialized',
                'sid': None
            }
        
        try:
            # Format numbers for WhatsApp
            from_number = f"whatsapp:{self.whatsapp_number}"
            to_whatsapp = f"whatsapp:{to_number}"
            
            # Send message
            message_obj = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to_whatsapp
            )
            
            return {
                'success': True,
                'sid': message_obj.sid,
                'status': message_obj.status,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'sid': None
            }
    
    def send_payment_reminder(self, member_name: str, to_number: str, 
                             month: str, year: int) -> Dict:
        """Send payment reminder to member"""
        message = f"""
Hi *{member_name}*! 👋

This is the *Khula Bot* 🤖

⏰ *Reminder:* Please deposit your *R300* into the FNB account before month-end!

📅 *Month:* {month} {year}
💰 *Amount:* R300.00

Your contribution helps our collective grow! 🇿🇦

_Reply STOP to unsubscribe_
        """
        
        return self.send_message(to_number, message)
    
    def send_milestone_alert(self, to_numbers: List[str], balance: float, 
                           milestone: str, suggestion: str) -> List[Dict]:
        """Send milestone achievement alert to multiple members"""
        message = f"""
🎉 *KHULA COLLECTIVE MILESTONE!*

We've hit *R{balance:,.2f}*! 🚀

💡 *AI Suggestion:*
{suggestion}

👉 Check the app for detailed investment recommendations!

Keep up the great work, team! 💪🇿🇦

_Khula AI Advisor_
        """
        
        results = []
        for number in to_numbers:
            result = self.send_message(number, message)
            results.append({
                'number': number,
                'result': result
            })
        
        return results
    
    def send_monthly_summary(self, member_name: str, to_number: str,
                           total_saved: float, month: str, year: int,
                           rank: int = None) -> Dict:
        """Send monthly summary to member"""
        rank_text = f"\n🏆 *Your Rank:* #{rank} in the collective!" if rank else ""
        
        message = f"""
📊 *KHULA COLLECTIVE - MONTHLY SUMMARY*

Hi *{member_name}*! 

📅 *Period:* {month} {year}
💰 *Your Total Saved:* R{total_saved:,.2f}
{rank_text}

Keep up the excellent work! Every R300 brings us closer to our investment goals! 🎯

_Khula Collective Bot_
        """
        
        return self.send_message(to_number, message)
    
    def send_welcome_message(self, member_name: str, to_number: str) -> Dict:
        """Send welcome message to new member"""
        message = f"""
🎉 *WELCOME TO KHULA COLLECTIVE!*

Hi *{member_name}*! 👋

Welcome to our investment club! 🇿🇦

📋 *Your Commitment:*
• R300 per month
• Payment by month-end
• Annual target: R3,600

💡 *What We Do:*
• Pool resources for investments
• AI-powered investment advice
• Collective wealth building

👉 Login to the app to view your dashboard!

Questions? Reply to this message!

_Khula Collective Team_
        """
        
        return self.send_message(to_number, message)
    
    def send_constitution_reminder(self, member_name: str, to_number: str) -> Dict:
        """Remind member to sign constitution"""
        message = f"""
📋 *ACTION REQUIRED*

Hi *{member_name}*,

Please sign the Khula Collective Constitution to activate your account.

👉 Login to the app and complete the sign-up process.

⏰ *Deadline:* 7 days from registration

_Khula Collective Admin_
        """
        
        return self.send_message(to_number, message)
    
    def send_arrears_notice(self, member_name: str, to_number: str,
                          months_owed: int, amount_owed: float) -> Dict:
        """Send notice to member in arrears"""
        message = f"""
⚠️ *PAYMENT NOTICE*

Hi *{member_name}*,

Our records show outstanding contributions:

📅 *Months Owed:* {months_owed}
💰 *Amount Due:* R{amount_owed:,.2f}

Please catch up on your contributions to remain in good standing.

Need help? Contact the admin team.

_Khula Collective Admin_
        """
        
        return self.send_message(to_number, message)
    
    def generate_whatsapp_link(self, member_name: str, total_saved: float,
                              rica_number: str) -> str:
        """
        Generate WhatsApp click-to-chat link with pre-filled message
        
        Args:
            member_name: Member's name
            total_saved: Member's total savings
            rica_number: Member's RICA number (without +27)
            
        Returns:
            WhatsApp click-to-chat URL
        """
        # Format number for WhatsApp (remove leading 0, add 27)
        if rica_number.startswith('0'):
            rica_number = '27' + rica_number[1:]
        elif not rica_number.startswith('27'):
            rica_number = '27' + rica_number
        
        # Pre-filled message
        message = f"Hi, I'm {member_name}. My current Khula Collective balance is R{total_saved:,.2f}. "
        
        # URL encode the message
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        
        # Generate WhatsApp link
        whatsapp_url = f"https://wa.me/{rica_number}?text={encoded_message}"
        
        return whatsapp_url
    
    def send_bulk_reminder(self, members_in_arrears: List[Dict], 
                          month: str, year: int) -> Dict:
        """
        Send bulk payment reminders to members in arrears
        
        Args:
            members_in_arrears: List of member dictionaries with name and rica_number
            month: Current month name
            year: Current year
            
        Returns:
            Summary of sent messages
        """
        results = {
            'total': len(members_in_arrears),
            'sent': 0,
            'failed': 0,
            'details': []
        }
        
        for member in members_in_arrears:
            result = self.send_payment_reminder(
                member_name=f"{member['first_name']} {member['surname']}",
                to_number=member['rica_number'],
                month=month,
                year=year
            )
            
            if result['success']:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            results['details'].append({
                'member': f"{member['first_name']} {member['surname']}",
                'number': member['rica_number'],
                'success': result['success'],
                'error': result.get('error')
            })
        
        return results
    
    def check_credentials(self) -> Dict:
        """Check if Twilio credentials are configured"""
        return {
            'configured': bool(self.client),
            'account_sid': bool(self.account_sid),
            'auth_token': bool(self.auth_token),
            'whatsapp_number': bool(self.whatsapp_number)
        }


# Demo mode for testing without Twilio
class DemoWhatsApp(KhulaWhatsApp):
    """Demo WhatsApp client for testing without Twilio credentials"""
    
    def __init__(self):
        """Initialize demo client"""
        super().__init__()
        self.sent_messages = []
    
    def send_message(self, to_number: str, message: str) -> Dict:
        """Simulate sending message"""
        self.sent_messages.append({
            'to': to_number,
            'message': message,
            'timestamp': datetime.now()
        })
        
        return {
            'success': True,
            'sid': f'DEMO{len(self.sent_messages):06d}',
            'status': 'sent',
            'error': None
        }
    
    def get_sent_messages(self) -> List[Dict]:
        """Get all sent messages in demo mode"""
        return self.sent_messages