# 🎉 Multi-User FNB Savings Tracker Guide

## Overview

The FNB Savings Tracker has been upgraded to support **20 individual users** with:
- ✅ Secure authentication system
- ✅ Individual user dashboards
- ✅ Database-backed data storage
- ✅ Encrypted Stitch API tokens
- ✅ Group overview page
- ✅ Leaderboard rankings
- ✅ Complete data privacy

---

## 🌐 Access the Application

**Live URL**: https://00303.app.super.myninja.ai

---

## 🔐 Authentication System

### Login Credentials

#### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

#### Sample User Accounts (20 users created)
- **Usernames**: `john_doe`, `jane_smith`, `mike_wilson`, `sarah_jones`, `david_brown`, `emma_davis`, `james_miller`, `olivia_garcia`, `william_martinez`, `sophia_rodriguez`, `liam_hernandez`, `ava_lopez`, `noah_gonzalez`, `isabella_wilson`, `ethan_anderson`, `mia_thomas`, `mason_taylor`, `charlotte_moore`, `lucas_jackson`
- **Password**: `password123` (for all sample users)

### Security Features
- ✅ **Password Hashing**: Bcrypt encryption for all passwords
- ✅ **Token Encryption**: Fernet encryption for Stitch API tokens
- ✅ **Session Management**: Secure session state handling
- ✅ **Data Privacy**: Users can only see their own transactions

---

## 📊 Database Schema

### Tables

#### 1. Users Table
```sql
- user_id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash (Bcrypt encrypted)
- stitch_token (Fernet encrypted)
- created_at (Timestamp)
```

#### 2. SavingsGoals Table
```sql
- goal_id (Primary Key)
- user_id (Foreign Key → Users)
- yearly_target (Decimal)
- target_year (Integer)
- currency (Default: ZAR)
```

#### 3. Transactions Table
```sql
- transaction_id (Primary Key)
- user_id (Foreign Key → Users)
- amount (Decimal)
- description (Text)
- bank_reference (String)
- transaction_date (Date)
- is_verified (Boolean)
```

#### 4. GlobalAccountSync Table
```sql
- sync_id (Primary Key)
- total_balance (Decimal)
- last_updated (Timestamp)
```

---

## 🎯 Features

### 1. My Dashboard (Personal View)
Each user has their own private dashboard showing:

- **Progress Bar**: Visual representation of savings vs. goal
- **Metrics**:
  - Current Savings
  - Yearly Target
  - Amount Remaining
- **Statistics**:
  - Total Deposits
  - Average Deposit
  - Largest Deposit
  - Smallest Deposit
- **Monthly Breakdown**: Interactive chart showing savings by month
- **Recent Transactions**: Table of recent deposits
- **Actions**:
  - Sync from Stitch API
  - Update savings goal

**Privacy**: Users can ONLY see their own transactions and data.

### 2. Group Overview (Collective View)
Shows aggregated data for all users:

- **Collective Savings**: Total savings across all 20 users
- **FNB Account Balance**: Current balance in the shared account
- **Active Users**: Number of registered users
- **Group Progress**: Combined progress towards collective goals
- **User Contributions**: Breakdown of each user's savings
- **Distribution Chart**: Pie chart showing contribution percentages

**Privacy**: Individual amounts are shown, but this is a shared view for transparency.

### 3. Leaderboard (Gamification)
Fun competitive element showing:

- **Top 3 Champions**: Special recognition with medals 🥇🥈🥉
- **Full Rankings**: Complete list sorted by progress percentage
- **Progress Distribution**: Bar chart comparing all users
- **Status Indicators**: Shows who achieved their goals

**Privacy**: Rankings are by **percentage progress**, not absolute amounts, maintaining relative privacy while celebrating achievements.

---

## 🚀 Getting Started

### Step 1: Login
1. Visit: https://00303.app.super.myninja.ai
2. Enter username and password
3. Click "Login"

### Step 2: Set Your Goal (First Time)
1. Navigate to "My Dashboard"
2. Enter your yearly savings target
3. Click "Save Goal"

### Step 3: View Your Data
- Your dashboard will show any existing transactions
- Sample data has been pre-loaded for testing

### Step 4: Explore Other Pages
- **Group Overview**: See how the group is doing collectively
- **Leaderboard**: Check your ranking among peers

---

## 🔧 Technical Implementation

### Authentication Flow
```
User Login → Database Verification → Session Creation → Dashboard Access
```

### Data Privacy Implementation
```python
# Users can only access their own data
def load_user_transactions(user_id: int, year: int):
    # Filters transactions by user_id
    transactions = db.get_user_transactions(user_id, year)
    return transactions
```

### Token Encryption
```python
# Stitch tokens are encrypted before storage
encrypted_token = cipher.encrypt(token.encode())

# Decrypted only when needed for API calls
decrypted_token = cipher.decrypt(encrypted_token)
```

### Database Operations
- **SQLAlchemy ORM**: Type-safe database operations
- **Session Management**: Proper connection handling
- **Transaction Safety**: Rollback on errors
- **Relationship Mapping**: Automatic foreign key handling

---

## 📁 File Structure

```
fnb-savings-tracker/
├── app_multiuser.py          # Multi-user Streamlit application
├── database.py                # Database models and operations
├── init_database.py           # Database initialization script
├── stitch_api.py             # Stitch API integration (unchanged)
├── data_processor.py         # Transaction processing (unchanged)
├── auth_config.yaml          # Authentication configuration
├── fnb_savings.db            # SQLite database file
├── encryption.key            # Encryption key for tokens
└── requirements.txt          # Updated dependencies
```

---

## 🔐 Security Best Practices

### Password Security
- ✅ Passwords are hashed with bcrypt (never stored in plain text)
- ✅ Salt is automatically generated for each password
- ✅ Hashing algorithm is computationally expensive (prevents brute force)

### Token Security
- ✅ Stitch API tokens are encrypted with Fernet (symmetric encryption)
- ✅ Encryption key is stored separately from database
- ✅ Tokens are only decrypted when needed for API calls
- ✅ Never exposed in logs or UI

### Session Security
- ✅ Session state is managed by Streamlit
- ✅ User ID is stored in session (not sensitive data)
- ✅ Logout clears all session data

### Database Security
- ✅ SQLite database with proper permissions
- ✅ SQL injection prevention through ORM
- ✅ Foreign key constraints enforced
- ✅ Transaction rollback on errors

---

## 🎮 Usage Scenarios

### Scenario 1: Individual User
```
1. Login with your credentials
2. Set your yearly savings goal
3. Sync transactions from Stitch API
4. Monitor your progress on dashboard
5. Check leaderboard to see your ranking
```

### Scenario 2: Group Administrator
```
1. Login as admin
2. View Group Overview for collective statistics
3. Monitor total FNB account balance
4. Check individual contributions
5. Review leaderboard for engagement
```

### Scenario 3: Competitive User
```
1. Login and check your dashboard
2. Navigate to Leaderboard
3. See your ranking vs. others
4. Increase savings to improve ranking
5. Celebrate when you reach top 3!
```

---

## 📊 Sample Data

The database has been initialized with:
- **20 Users**: Admin + 19 sample users
- **Random Goals**: Between R50,000 and R200,000 per user
- **Sample Transactions**: 10-30 transactions per user
- **Realistic Data**: Varied amounts and descriptions
- **Current Year**: All data for 2025

### Sample Statistics
- **Total Group Savings**: ~R208,000
- **Average User Goal**: ~R120,000
- **Total Transactions**: ~400 transactions
- **Active Users**: 20

---

## 🔄 Syncing with Stitch API

### For Individual Users
1. Configure your Stitch API token (admin can do this)
2. Click "Sync from Stitch API" on your dashboard
3. New transactions will be imported automatically
4. Duplicates are prevented by checking bank references

### Token Configuration
```python
# Admin can update user tokens
db.update_user_token(user_id, stitch_token)

# Tokens are encrypted before storage
encrypted = cipher.encrypt(token.encode())
```

---

## 🏆 Leaderboard Mechanics

### Ranking Calculation
```python
progress_percentage = (current_savings / target) * 100
```

### Privacy Protection
- Rankings show **percentage progress**, not absolute amounts
- Example: "85.5% of goal" instead of "R85,500 saved"
- Maintains competitive element while protecting financial privacy

### Medals and Recognition
- 🥇 **1st Place**: Gold medal
- 🥈 **2nd Place**: Silver medal
- 🥉 **3rd Place**: Bronze medal
- 🎉 **Goal Achieved**: Special status for 100%+ progress

---

## 🛠️ Administration

### Adding New Users
```python
from database import DatabaseManager

db = DatabaseManager()
user = db.create_user(
    username="new_user",
    email="new@example.com",
    password="secure_password"
)
```

### Updating User Goals
```python
db.create_or_update_goal(
    user_id=user.user_id,
    yearly_target=150000.00,
    target_year=2025
)
```

### Managing Transactions
```python
# Add manual transaction
db.add_transaction(
    user_id=user.user_id,
    amount=5000.00,
    description="Salary Deposit",
    bank_reference="REF123456",
    transaction_date=datetime.now(),
    is_verified=True
)
```

---

## 📈 Analytics and Insights

### Individual Analytics
- Monthly savings trends
- Average deposit size
- Deposit frequency
- Progress velocity

### Group Analytics
- Total collective savings
- Average group progress
- Top performers
- Contribution distribution

### Comparative Analytics
- Your rank vs. others
- Your progress vs. average
- Your deposits vs. group average

---

## 🔍 Troubleshooting

### Cannot Login
- **Check credentials**: Ensure username and password are correct
- **Database issue**: Verify `fnb_savings.db` exists
- **Run init script**: `python init_database.py`

### No Transactions Showing
- **Check year selection**: Ensure correct year is selected
- **Sync from API**: Click "Sync from Stitch API"
- **Database empty**: Run init script to populate sample data

### Leaderboard Empty
- **No goals set**: Users need to set yearly goals
- **Wrong year**: Select year with active goals
- **Database issue**: Check database integrity

### Group Overview Shows Zero
- **No transactions**: Import or create transactions
- **Database sync**: Run global balance update
- **Year filter**: Ensure correct year is selected

---

## 🎓 Best Practices

### For Users
1. **Set realistic goals**: Based on your income and expenses
2. **Regular monitoring**: Check dashboard weekly
3. **Sync frequently**: Keep data up-to-date with Stitch API
4. **Celebrate milestones**: Acknowledge progress at 25%, 50%, 75%
5. **Engage with leaderboard**: Use it as motivation

### For Administrators
1. **Secure credentials**: Change default passwords
2. **Regular backups**: Backup `fnb_savings.db` regularly
3. **Monitor activity**: Check group overview for anomalies
4. **Update tokens**: Keep Stitch API tokens current
5. **User support**: Help users with setup and issues

---

## 🚀 Next Steps

1. **Login**: Use provided credentials
2. **Explore**: Navigate through all three pages
3. **Customize**: Update your goal and profile
4. **Engage**: Check leaderboard and compete
5. **Monitor**: Track your progress regularly

---

## 📞 Support

### Documentation
- **Main README**: [README.md](README.md)
- **API Docs**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)

### Technical Support
- Database issues: Check `database.py`
- Authentication issues: Check `app_multiuser.py`
- API issues: Check `stitch_api.py`

---

## ✅ Feature Checklist

- [x] Authentication system with streamlit-authenticator
- [x] SQLAlchemy database integration
- [x] User table with encrypted tokens
- [x] Individual savings goals per user
- [x] Transaction filtering by user
- [x] Personal dashboard for each user
- [x] Group overview page
- [x] Leaderboard with percentage rankings
- [x] Data privacy controls
- [x] Encrypted Stitch API tokens
- [x] Sample data for 20 users
- [x] Comprehensive documentation

---

**Your Multi-User FNB Savings Tracker is ready!** 🎉

**Access now**: https://00303.app.super.myninja.ai

**Login**: `admin` / `admin123` or any sample user with `password123`