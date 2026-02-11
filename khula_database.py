"""
Khula Collective Database Module
Handles all database operations for the investment club
"""

import sqlite3
from datetime import datetime, date
from typing import Optional, List, Dict, Tuple
import bcrypt
import os


class KhulaDatabase:
    """Manages all database operations for Khula Collective"""
    
    def __init__(self, db_path: str = "khula_collective.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('khula_schema.sql', 'r') as f:
            schema = f.read()
            cursor.executescript(schema)
        
        # Insert default constitution if not exists
        cursor.execute("SELECT COUNT(*) FROM Constitution")
        if cursor.fetchone()[0] == 0:
            self.insert_default_constitution(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_default_constitution(self, cursor):
        """Insert default Khula Collective constitution"""
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
- Investment options include:
  * RSA Retail Savings Bonds
  * Money Market Unit Trusts
  * EasyEquities ETFs
  * Other approved investment vehicles

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

## 9. DISPUTE RESOLUTION
- Disputes handled by admin team first
- Escalation to full member vote if needed
- External mediation as last resort

## 10. AMENDMENTS
- Constitution may be amended with 75% member approval
- All amendments must be documented and signed

By signing this constitution, I agree to abide by all terms and conditions.
        """
        
        cursor.execute("""
            INSERT INTO Constitution (version, content, effective_date)
            VALUES (?, ?, ?)
        """, ('1.0', constitution_text, date(2025, 1, 1)))
    
    # User Management
    
    def validate_sa_id(self, id_number: str) -> Tuple[bool, str]:
        """
        Validate South African ID number using Luhn algorithm
        
        Args:
            id_number: 13-digit SA ID number
            
        Returns:
            Tuple of (is_valid, message)
        """
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
    
    def extract_info_from_id(self, id_number: str) -> Dict:
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
        
        # Citizenship
        citizenship = "Citizen" if id_number[10] == '0' else "Permanent Resident"
        
        return {
            'date_of_birth': dob,
            'gender': gender,
            'citizenship': citizenship
        }
    
    def create_user(self, username: str, first_name: str, surname: str,
                   id_number: str, rica_number: str, email: str,
                   password: str, is_admin: bool = False) -> Optional[int]:
        """
        Create a new user with FICA compliance
        
        Returns:
            user_id if successful, None otherwise
        """
        # Validate ID
        is_valid, message = self.validate_sa_id(id_number)
        if not is_valid:
            raise ValueError(message)
        
        # Extract info from ID
        id_info = self.extract_info_from_id(id_number)
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Users (
                    username, first_name, surname, id_number, rica_number,
                    email, password_hash, gender, date_of_birth, is_admin
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                username, first_name, surname, id_number, rica_number,
                email, password_hash, id_info['gender'], 
                id_info['date_of_birth'], is_admin
            ))
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user info"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, username, first_name, surname, password_hash,
                   is_admin, constitution_signed
            FROM Users WHERE username = ?
        """, (username,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
            return dict(user)
        return None
    
    def sign_constitution(self, user_id: int) -> bool:
        """Mark user as having signed the constitution"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE Users 
                SET constitution_signed = 1,
                    constitution_signed_date = ?
                WHERE user_id = ?
            """, (datetime.now(), user_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error signing constitution: {e}")
            return False
        finally:
            conn.close()
    
    def update_document_paths(self, user_id: int, id_doc_path: str = None,
                             por_path: str = None) -> bool:
        """Update document paths for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if id_doc_path:
                cursor.execute("""
                    UPDATE Users SET id_document_path = ? WHERE user_id = ?
                """, (id_doc_path, user_id))
            
            if por_path:
                cursor.execute("""
                    UPDATE Users SET proof_of_residence_path = ? WHERE user_id = ?
                """, (por_path, user_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating documents: {e}")
            return False
        finally:
            conn.close()
    
    # Contribution Management
    
    def record_contribution(self, user_id: int, month: int, year: int,
                          amount: float, payment_date: date,
                          payment_reference: str = None) -> bool:
        """Record a monthly contribution"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO Monthly_Contributions
                (user_id, month, year, amount, payment_date, payment_reference, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, month, year, amount, payment_date, payment_reference, 'Paid'))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error recording contribution: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_contributions(self, user_id: int, year: int = None) -> List[Dict]:
        """Get all contributions for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if year:
            cursor.execute("""
                SELECT * FROM Monthly_Contributions
                WHERE user_id = ? AND year = ?
                ORDER BY year DESC, month DESC
            """, (user_id, year))
        else:
            cursor.execute("""
                SELECT * FROM Monthly_Contributions
                WHERE user_id = ?
                ORDER BY year DESC, month DESC
            """, (user_id,))
        
        contributions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return contributions
    
    def get_user_total_contributions(self, user_id: int, year: int = None) -> float:
        """Calculate total contributions for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if year:
            cursor.execute("""
                SELECT SUM(amount) FROM Monthly_Contributions
                WHERE user_id = ? AND year = ?
            """, (user_id, year))
        else:
            cursor.execute("""
                SELECT SUM(amount) FROM Monthly_Contributions
                WHERE user_id = ?
            """, (user_id,))
        
        result = cursor.fetchone()[0]
        conn.close()
        return float(result) if result else 0.0
    
    def check_monthly_payment(self, user_id: int, month: int, year: int) -> bool:
        """Check if user has paid for specific month"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM Monthly_Contributions
            WHERE user_id = ? AND month = ? AND year = ? AND status = 'Paid'
        """, (user_id, month, year))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def get_members_in_arrears(self, month: int, year: int) -> List[Dict]:
        """Get list of members who haven't paid for specific month"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.surname, u.rica_number, u.email
            FROM Users u
            WHERE u.is_admin = 0
            AND u.user_id NOT IN (
                SELECT user_id FROM Monthly_Contributions
                WHERE month = ? AND year = ? AND status = 'Paid'
            )
        """, (month, year))
        
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return members
    
    # Group Statistics
    
    def get_total_pot(self) -> float:
        """Get total collective savings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(amount) FROM Monthly_Contributions
            WHERE status = 'Paid'
        """)
        
        result = cursor.fetchone()[0]
        conn.close()
        return float(result) if result else 0.0
    
    def get_group_compliance(self, month: int, year: int) -> Tuple[int, int, float]:
        """
        Calculate group compliance for specific month
        
        Returns:
            Tuple of (paid_count, total_members, percentage)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total non-admin members
        cursor.execute("SELECT COUNT(*) FROM Users WHERE is_admin = 0")
        total_members = cursor.fetchone()[0]
        
        # Members who paid
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) FROM Monthly_Contributions
            WHERE month = ? AND year = ? AND status = 'Paid'
        """, (month, year))
        paid_count = cursor.fetchone()[0]
        
        conn.close()
        
        percentage = (paid_count / total_members * 100) if total_members > 0 else 0
        return paid_count, total_members, percentage
    
    def get_leaderboard(self, year: int = None) -> List[Dict]:
        """Get leaderboard of top savers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if year:
            cursor.execute("""
                SELECT u.user_id, u.first_name, u.surname,
                       SUM(mc.amount) as total_saved,
                       COUNT(mc.contribution_id) as months_paid
                FROM Users u
                LEFT JOIN Monthly_Contributions mc ON u.user_id = mc.user_id
                WHERE u.is_admin = 0 AND (mc.year = ? OR mc.year IS NULL)
                GROUP BY u.user_id
                ORDER BY total_saved DESC
            """, (year,))
        else:
            cursor.execute("""
                SELECT u.user_id, u.first_name, u.surname,
                       SUM(mc.amount) as total_saved,
                       COUNT(mc.contribution_id) as months_paid
                FROM Users u
                LEFT JOIN Monthly_Contributions mc ON u.user_id = mc.user_id
                WHERE u.is_admin = 0
                GROUP BY u.user_id
                ORDER BY total_saved DESC
            """)
        
        leaderboard = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return leaderboard
    
    # Admin Functions
    
    def get_all_members_fica(self) -> List[Dict]:
        """Get FICA information for all members"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_id, first_name, surname, id_number, rica_number,
                   email, gender, date_of_birth, constitution_signed,
                   constitution_signed_date, id_document_path,
                   proof_of_residence_path, created_at
            FROM Users
            WHERE is_admin = 0
            ORDER BY surname, first_name
        """)
        
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return members
    
    def log_admin_action(self, admin_user_id: int, action_type: str,
                        action_details: str) -> bool:
        """Log admin action"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Admin_Actions (admin_user_id, action_type, action_details)
                VALUES (?, ?, ?)
            """, (admin_user_id, action_type, action_details))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging admin action: {e}")
            return False
        finally:
            conn.close()
    
    # WhatsApp Notifications
    
    def log_whatsapp_notification(self, user_id: int, message_type: str,
                                  message_content: str, status: str,
                                  twilio_sid: str = None) -> bool:
        """Log WhatsApp notification"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO WhatsApp_Notifications
                (user_id, message_type, message_content, status, twilio_sid)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, message_type, message_content, status, twilio_sid))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging notification: {e}")
            return False
        finally:
            conn.close()
    
    # Investment Suggestions
    
    def log_investment_suggestion(self, total_balance: float, suggestion_type: str,
                                 suggested_amount: float, expected_return: float,
                                 risk_level: str) -> bool:
        """Log investment suggestion"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Investment_Suggestions
                (total_balance, suggestion_type, suggested_amount, expected_return, risk_level)
                VALUES (?, ?, ?, ?, ?)
            """, (total_balance, suggestion_type, suggested_amount, expected_return, risk_level))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging suggestion: {e}")
            return False
        finally:
            conn.close()
    
    def get_constitution(self) -> str:
        """Get current constitution text"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT content FROM Constitution
            ORDER BY effective_date DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        return result['content'] if result else ""