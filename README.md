# Khula Collective Investment Club App

A comprehensive FICA-compliant investment club tracker for 20 members, built with Streamlit and Python.

## 🚀 Quick Deploy

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=ttmodupe-hash/ttmodupe-hashttmodupe-hash-khula-collective-app&branch=main&mainModule=khula_final.py)

**One-click deployment** - Click the button above to deploy instantly to Streamlit Cloud!

## 🌟 Features

### Core Functionality
- **Multi-User System**: 20 members + 1 admin account
- **FICA Compliance**: SA ID validation with Luhn algorithm, RICA verification
- **Monthly Contributions**: R300/month tracking per member
- **Investment Goals**: Collective savings targets with progress tracking
- **AI Investment Advisor**: Smart recommendations based on total pot size
- **WhatsApp Integration**: Automated reminders and notifications via Twilio
- **Stitch API Integration**: Live bank transaction syncing (optional)

### Member Features
- Personal dashboard with savings overview
- Monthly contribution grid (14 months history)
- Contribution history table
- AI-powered investment suggestions
- Progress tracking against yearly goals

### Admin Features
- Complete member management
- FICA compliance monitoring
- Bulk WhatsApp notifications
- CSV data export
- Audit trail logging
- Constitution management

### Group Analytics
- Total pot tracking
- Leaderboard with rankings
- Community health scoring
- Monthly trend analysis
- Top performers recognition
- Support identification for struggling members

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/khula-collective-app.git
cd khula-collective-app
```

2. Install dependencies:
```bash
pip install -r requirements_final.txt
```

3. Run the application:
```bash
streamlit run khula_final.py
```

4. Access the app at `http://localhost:8501`

### Default Login Credentials

**Admin Account:**
- Username: `admin_khula`
- Password: `admin123`

**Member Accounts:**
- Username: `thabo_mthembu`, `nomsa_dlamini`, etc.
- Password: `password123`

## 📊 Database Schema

The application uses SQLite with 9 tables:

1. **Users** - Member profiles with FICA data
2. **Monthly_Contributions** - R300/month tracking
3. **Transactions** - Stitch API synced transactions
4. **Investment_Goals** - Collective targets
5. **GlobalAccountSync** - Total pot management
6. **WhatsApp_Notifications** - Message logs
7. **Investment_Suggestions** - AI recommendations
8. **Admin_Actions** - Audit trail
9. **Constitution** - Legal document versioning

## 🔐 FICA Compliance

### SA ID Validation
- 13-digit format validation
- Luhn algorithm checksum verification
- Auto-extraction of DOB, Gender, Citizenship

### Required Documents
- SA ID photo upload
- Proof of residence
- RICA cellphone number
- Digital constitution signing

## 🤖 AI Investment Advisor

Smart recommendations based on total pot size:

- **< R10,000**: Build emergency fund (3-6 months expenses)
- **R10,000 - R50,000**: Money Market + Bonds (8-9% return)
- **R50,000+ MILESTONE**: RSA Retail Bonds (R50k @ 7.75% = R3,875/year)
- **R80,000+**: Full diversification (ETFs, Property, TFSA) - 9-11% return

## 📱 WhatsApp Integration

Automated notifications via Twilio:
- Payment reminders (25th of each month)
- Milestone alerts (R50k, R80k thresholds)
- Monthly summaries (1st of each month)
- Welcome messages for new members
- Bulk admin messaging

### Configuration
Add to `.streamlit/secrets.toml`:
```toml
[twilio]
account_sid = "your_account_sid"
auth_token = "your_auth_token"
whatsapp_from = "whatsapp:+14155238886"
```

## 🏦 Stitch API Integration

Optional live bank transaction syncing:

### Configuration
Add to `.streamlit/secrets.toml`:
```toml
[stitch]
client_id = "your_client_id"
client_secret = "your_client_secret"
redirect_uri = "your_redirect_uri"
```

## 📁 Project Structure

```
khula-collective-app/
├── khula_final.py              # Main Streamlit application
├── khula_database.py           # Database models and operations
├── khula_ai_advisor.py         # Investment recommendation engine
├── khula_whatsapp.py           # Twilio WhatsApp integration
├── khula_seed_data.py          # Database seeding script
├── khula_schema.sql            # Database schema definition
├── requirements_final.txt      # Python dependencies
├── khula_collective.db         # SQLite database (pre-seeded)
├── DEPLOYMENT_READY.md         # Deployment guide
├── KHULA_README.md             # Detailed documentation
└── README.md                   # This file
```

## 🎯 Key Metrics

- **Start Date**: January 2025
- **Monthly Contribution**: R300 per member
- **Yearly Target**: R3,600 per member
- **Total Members**: 20 + 1 admin
- **Historical Data**: 14 months (Jan 2025 - Feb 2026)
- **Current Total Pot**: R71,700 (seeded data)
- **Average Compliance**: ~90%

## 🏆 Top Savers (Sample Data)

1. 🥇 Thabo Mthembu - R3,900
2. 🥈 Nomsa Dlamini - R3,600
3. 🥉 Sipho Khumalo - R3,600
4. Zanele Ndlovu - R3,300
5. Mandla Zulu - R3,300

## 🔒 Security Features

- Bcrypt password hashing
- Luhn algorithm SA ID validation
- Fernet token encryption for Stitch API
- Role-based access control
- Comprehensive audit logging
- Session management

## 📚 Documentation

- `DEPLOYMENT_READY.md` - Complete deployment guide
- `KHULA_README.md` - Detailed feature documentation
- `API_DOCUMENTATION.md` - Stitch API integration guide
- `GROUP_ANALYTICS_GUIDE.md` - Analytics features

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Bcrypt
- **API Integration**: Stitch Money (GraphQL)
- **Notifications**: Twilio WhatsApp API
- **Data Visualization**: Plotly
- **Data Processing**: Pandas

## 📝 License

This project is proprietary software for Khula Collective members.

## 🤝 Contributing

This is a private repository for Khula Collective. For questions or support, contact the admin team.

## 📞 Support

For technical support or questions:
- Contact: admin@khulacollective.app
- Admin Dashboard: Access via admin account

## 🎉 Acknowledgments

Built with ❤️ for the Khula Collective community by NinjaTech AI.

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready ✅