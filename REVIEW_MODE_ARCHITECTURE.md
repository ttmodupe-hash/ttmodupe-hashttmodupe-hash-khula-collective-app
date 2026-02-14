# 🏗️ Review Mode Architecture

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    KHULA COLLECTIVE APP                      │
│                  (Streamlit Application)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Admin Login    │
                    │  admin_khula    │
                    └─────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      🔍 Review Mode Toggle              │
        │      (Sidebar - Admin Only)             │
        └─────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │   REVIEW MODE     │       │    LIVE MODE      │
    │   (Mock Data)     │       │  (Real Bank Data) │
    └───────────────────┘       └───────────────────┘
                │                           │
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │  seed_data.py     │       │  Stitch API       │
    │  • 21 members     │       │  • FNB Account    │
    │  • 280 contribs   │       │  • Real Deposits  │
    │  • R75,600        │       │  • Live Balance   │
    │  • 5 proposals    │       │  • Transactions   │
    └───────────────────┘       └───────────────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌─────────────────┐
                    │  Member Login   │
                    │  20 Members     │
                    └─────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         Member Dashboard                 │
        │  • Personal Stats                        │
        │  • Contribution History                  │
        │  • Voting System                         │
        │  • FICA Registration                     │
        │  • Constitution Signing                  │
        └─────────────────────────────────────────┘
```

---

## Data Flow

### Review Mode (Mock Data):

```
User Action → app.py → is_review_mode() → seed_data.py → Mock Data → Display
                ↓
         No API Calls
         No Database Writes
         Safe Testing
```

### Live Mode (Real Data):

```
User Action → app.py → is_review_mode() → khula_collective.db → Real Data → Display
                ↓                              ↓
         Stitch API                    FNB Account
         Real Deposits                 Live Balance
```

---

## Function Call Flow

### Example: Get Total Balance

```python
# User views dashboard
show_dashboard()
    ↓
# Get balance
total_balance = get_total_balance()
    ↓
# Check mode
if is_review_mode() and MOCK_DATA_AVAILABLE:
    ↓
    # Review Mode: Use mock data
    return calculate_mock_balance()  # Returns R75,600
else:
    ↓
    # Live Mode: Query database
    conn = get_db()
    cursor.execute("SELECT SUM(amount)...")
    return real_balance  # Returns actual FNB balance
```

---

## Component Interaction

```
┌──────────────────────────────────────────────────────────┐
│                      app.py                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Session State                                      │  │
│  │  • logged_in: True/False                           │  │
│  │  • user: {user_id, username, role, ...}           │  │
│  │  • review_mode: True/False  ← Admin Toggle        │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Data Loading Functions                            │  │
│  │  • get_total_balance()                             │  │
│  │  • get_monthly_totals()                            │  │
│  │  • get_member_contributions()                      │  │
│  │  • get_votes()                                     │  │
│  │  • user_has_voted()                                │  │
│  │  • cast_vote()                                     │  │
│  │                                                     │  │
│  │  Each function checks: is_review_mode()            │  │
│  │  ↓                                                  │  │
│  │  If True → seed_data.py                            │  │
│  │  If False → khula_collective.db                    │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │  seed_data.py     │       │ khula_collective  │
    │                   │       │      .db          │
    │  Mock Functions:  │       │                   │
    │  • generate_mock  │       │  Real Tables:     │
    │    _contributions │       │  • Users          │
    │  • calculate_mock │       │  • Monthly_       │
    │    _balance       │       │    Contributions  │
    │  • get_mock_      │       │  • Votes          │
    │    leaderboard    │       │  • Suggestions    │
    │  • get_mock_      │       │  • GlobalAccount  │
    │    investment_    │       │    Sync           │
    │    opportunities  │       │                   │
    └───────────────────┘       └───────────────────┘
```

---

## UI Component Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Sidebar (Admin)                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  🇿🇦 KHULA                                         │  │
│  │  Admin User                                        │  │
│  ├───────────────────────────────────────────────────┤  │
│  │  🔍 Review Mode                                    │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │ ⚪ Enable Review Mode                       │  │  │
│  │  │                                             │  │  │
│  │  │ [Toggle Switch]                             │  │  │
│  │  │                                             │  │  │
│  │  │ ℹ️ Use mock data for testing.              │  │  │
│  │  │   Real bank credentials stay hidden.       │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │                                                    │  │
│  │  When ON:                                          │  │
│  │  📊 Using mock data for testing                   │  │
│  │                                                    │  │
│  │  When OFF:                                         │  │
│  │  🔴 Using live bank data                          │  │
│  ├───────────────────────────────────────────────────┤  │
│  │  🚪 Logout                                         │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  Main Content Area                       │
│                                                          │
│  When Review Mode ON:                                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 🔍 REVIEW MODE ACTIVE                              │ │
│  │                                                     │ │
│  │ Using mock data for testing. Real bank            │ │
│  │ credentials are hidden. Members can safely        │ │
│  │ test login, FICA registration, and voting.        │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 💰 COLLECTIVE POT                                  │ │
│  │                                                     │ │
│  │         R75,600.00                                 │ │
│  │                                                     │ │
│  │ 20 Members • Since Jan 2025                        │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [Dashboard] [Member Voice] [AI Advisor] [Profile]      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## State Management

```python
# Session State Structure
st.session_state = {
    'logged_in': True,
    'user': {
        'user_id': 1,
        'username': 'admin_khula',
        'first_name': 'Admin',
        'surname': 'User',
        'is_admin': 1,
        'constitution_signed': 1
    },
    'review_mode': True,  # ← Controlled by admin toggle
    'review_mode_toggle': True  # ← Toggle widget state
}

# Mode Detection
def is_review_mode():
    return st.session_state.get('review_mode', False)

# Data Loading Decision
if is_review_mode() and MOCK_DATA_AVAILABLE:
    # Use mock data from seed_data.py
    data = get_mock_data()
else:
    # Use real data from database
    data = get_real_data()
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Security Layers                        │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
┌───────────────────┐                   ┌───────────────────┐
│   Review Mode     │                   │    Live Mode      │
│   (Safe Testing)  │                   │  (Production)     │
└───────────────────┘                   └───────────────────┘
        │                                           │
        ▼                                           ▼
┌───────────────────┐                   ┌───────────────────┐
│ ✅ No API Keys    │                   │ 🔒 Encrypted Keys │
│ ✅ No Real Data   │                   │ 🔒 Secure Storage │
│ ✅ No DB Writes   │                   │ 🔒 HTTPS Only     │
│ ✅ Safe Testing   │                   │ 🔒 Auth Required  │
└───────────────────┘                   └───────────────────┘
        │                                           │
        ▼                                           ▼
┌───────────────────┐                   ┌───────────────────┐
│ Members See:      │                   │ Members See:      │
│ • Mock balance    │                   │ • Real balance    │
│ • Test data       │                   │ • Live data       │
│ • Sample votes    │                   │ • Actual votes    │
│ • No risk         │                   │ • Real deposits   │
└───────────────────┘                   └───────────────────┘
```

---

## Toggle Mechanism

```python
# In sidebar (admin only)
if user['is_admin'] == 1:
    # Initialize state
    if 'review_mode' not in st.session_state:
        st.session_state.review_mode = False
    
    # Toggle widget
    review_mode = st.toggle(
        "Enable Review Mode",
        value=st.session_state.review_mode,
        help="Use mock data for testing",
        key="review_mode_toggle"
    )
    
    # Update state
    st.session_state.review_mode = review_mode
    
    # Visual feedback
    if review_mode:
        st.info("📊 Using mock data for testing")
    else:
        st.success("🔴 Using live bank data")
```

---

## Data Source Selection

```python
# Centralized mode check
def is_review_mode():
    return st.session_state.get('review_mode', False)

# Example: Get balance
def get_total_balance():
    if is_review_mode() and MOCK_DATA_AVAILABLE:
        # Review Mode path
        return float(calculate_mock_balance())
    else:
        # Live Mode path
        conn = get_db()
        # ... query database
        return float(total)

# Example: Get contributions
def get_member_contributions(user_id):
    if is_review_mode() and MOCK_DATA_AVAILABLE:
        # Review Mode path
        all_contribs = generate_mock_contributions()
        return [c for c in all_contribs if c['user_id'] == user_id]
    else:
        # Live Mode path
        conn = get_db()
        # ... query database
        return data
```

---

## Error Handling

```python
# Import with fallback
try:
    from seed_data import (
        generate_mock_contributions,
        calculate_mock_balance,
        # ... other functions
    )
    MOCK_DATA_AVAILABLE = True
except ImportError:
    MOCK_DATA_AVAILABLE = False

# Safe mode check
def is_review_mode():
    return st.session_state.get('review_mode', False)

# Safe data loading
if is_review_mode() and MOCK_DATA_AVAILABLE:
    # Use mock data
    data = get_mock_data()
elif is_review_mode() and not MOCK_DATA_AVAILABLE:
    # Fallback to live data if mock unavailable
    st.warning("Mock data unavailable, using live data")
    data = get_real_data()
else:
    # Use live data
    data = get_real_data()
```

---

## Performance Considerations

```
Review Mode (Mock Data):
├─ No database queries
├─ No API calls
├─ Fast data generation
├─ Instant response
└─ Low resource usage

Live Mode (Real Data):
├─ Database queries
├─ Stitch API calls
├─ Network latency
├─ Processing time
└─ Higher resource usage

Optimization:
├─ Mock data pre-generated
├─ Minimal computation
├─ No external dependencies
└─ Instant toggle switching
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Streamlit Cloud Deployment                  │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         app.py (Main Application)        │
        │         seed_data.py (Mock Data)         │
        │         khula_collective.db (Database)   │
        └─────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │  Review Mode      │       │   Live Mode       │
    │  (No Secrets)     │       │  (With Secrets)   │
    └───────────────────┘       └───────────────────┘
                                            │
                                            ▼
                              ┌───────────────────┐
                              │ Streamlit Secrets │
                              │ • STITCH_CLIENT   │
                              │ • STITCH_SECRET   │
                              │ • FNB_ACCOUNT     │
                              └───────────────────┘
                                            │
                                            ▼
                              ┌───────────────────┐
                              │   Stitch API      │
                              │   FNB Account     │
                              └───────────────────┘
```

---

**This architecture ensures safe testing while maintaining production security! 🔒**