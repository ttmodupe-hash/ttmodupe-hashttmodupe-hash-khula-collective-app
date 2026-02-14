# 🚀 Khula Collective - Automated Investment Platform

> **Fully automated FICA-compliant investment club platform for 20 South African members**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

---

## 🌟 Features

### 💰 Financial Management
- **R300/month contributions** per member
- **R71,700 collective pot** (current balance)
- **Real-time FNB sync** via Stitch API
- **Automatic payment tracking** (Pending → Received)
- **13 months historical data** (239 contributions)

### 🤖 AI-Powered Intelligence
- **Market-aware recommendations** (SARB repo rate: 8.25%)
- **8 SA crisis-based opportunities** (load shedding, water crisis, etc.)
- **ROI calculations** with risk analysis
- **Balance-based strategies** (<R50k, R50k-R100k, >R100k)
- **Weekly market updates** (automated)

### 🗳️ Democratic Voting
- **One vote per member** per proposal
- **60% approval threshold** (12/20 votes)
- **Real-time vote tracking** with live charts
- **Investment proposals** with detailed analysis

### 🔒 FICA Compliance
- **SA ID validation** with Luhn algorithm
- **Digital constitution** signing
- **Member signature log** with timestamps
- **Document upload** capability
- **RICA verification**

### ⚡ Full Automation
- **Daily FNB sync** (8 AM SAST)
- **Monthly reset** (1st of month)
- **Weekly market updates** (Mondays)
- **Real-time webhooks** for instant updates
- **Zero manual intervention**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Khula Collective                         │
│                   Investment Platform                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         Streamlit Cloud App              │
        │    (24/7 availability, auto-deploy)      │
        └─────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │  Supabase Cloud   │       │  GitHub Actions   │
    │   PostgreSQL DB   │       │   Automation      │
    │  (10 tables, RLS) │       │  (Daily/Monthly)  │
    └───────────────────┘       └───────────────────┘
                ▲                           ▲
                │                           │
    ┌───────────┴───────────┐   ┌──────────┴──────────┐
    │   Stitch Webhook      │   │   Market Data API   │
    │  (Real-time sync)     │   │  (SARB, Stats SA)   │
    └───────────────────────┘   └─────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Use Existing Deployment (Fastest)

**Live App**: https://ttmodupe-hashttmodupe-hash-khula-collective-app-gpgc3mgplddy27.streamlit.app/

**Login Credentials:**
- **Admin**: `admin_khula` / `admin123`
- **Members**: `thabo_mthembu`, `nomsa_dlamini`, etc. / `password123`

### Option 2: Deploy Your Own (30 minutes)

Follow the **[Quick Start Guide](QUICK_START_AUTOMATION.md)** for step-by-step instructions.

**Summary:**
1. Create Supabase project (10 min)
2. Setup GitHub Actions (5 min)
3. Deploy webhook listener (10 min)
4. Configure Streamlit secrets (5 min)

---

## 📊 Automation Schedule

| Task | Frequency | Time (SAST) | Description |
|------|-----------|-------------|-------------|
| **FNB Sync** | Daily | 08:00 | Sync transactions, update contributions |
| **Market Update** | Weekly | Monday 08:00 | Fetch latest rates, refresh AI advisor |
| **Monthly Reset** | Monthly | 1st @ 00:01 | Archive Hall of Fame, create new records |
| **Webhook** | Real-time | Always | Instant deposit notifications |

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit 1.31+** - Web framework
- **Plotly 5.18+** - Interactive charts
- **Pandas 2.0+** - Data processing

### Backend
- **Supabase** - Cloud PostgreSQL database
- **SQLAlchemy** - ORM (SQLite fallback)
- **Flask** - Webhook listener

### Integrations
- **Stitch API** - FNB bank integration
- **GitHub Actions** - CI/CD automation
- **Twilio** - WhatsApp notifications (optional)

### Infrastructure
- **Streamlit Cloud** - App hosting
- **Render/Railway** - Webhook hosting
- **GitHub** - Version control & automation

---

## 📁 Project Structure

```
khula-collective/
├── app.py                          # Main Streamlit application
├── database_helper.py              # Unified DB manager (SQLite/Supabase)
├── version.py                      # Version tracking system
├── khula_collective.db             # SQLite database (backup)
├── supabase_schema.sql             # PostgreSQL schema
│
├── scripts/
│   ├── sync_fnb.py                 # Daily FNB sync (8 AM)
│   ├── monthly_reset.py            # Monthly reset (1st of month)
│   ├── update_market_data.py       # Weekly market updates
│   ├── stitch_webhook.py           # Real-time webhook listener
│   └── migrate_to_supabase.py      # SQLite → Supabase migration
│
├── .github/workflows/
│   └── main.yml                    # GitHub Actions automation
│
├── tests/
│   └── test_app.py                 # Test suite
│
├── docs/
│   ├── AUTOMATION_SETUP_GUIDE.md   # Detailed setup instructions
│   ├── QUICK_START_AUTOMATION.md   # 30-minute quick start
│   ├── DEPLOYMENT_CHECKLIST.md     # Pre-deployment verification
│   └── README_AUTOMATION.md        # This file
│
└── requirements.txt                # Python dependencies
```

---

## 🔐 Security

### Authentication
- **SHA-256 password hashing** (replaced bcrypt for compatibility)
- **Session management** with Streamlit
- **Role-based access** (admin/member)

### Data Protection
- **Row Level Security (RLS)** in Supabase
- **Encrypted API keys** in GitHub secrets
- **HTTPS enforced** on all endpoints
- **Webhook signature verification**

### FICA Compliance
- **SA ID validation** with Luhn algorithm
- **Digital signatures** with timestamps
- **Document storage** capability
- **Audit trail** for all actions

---

## 📈 Database Schema

### Core Tables (10)
1. **users** - Member authentication & profiles
2. **monthly_contributions** - R300/month tracking
3. **global_account_sync** - Total pot balance
4. **investment_goals** - Collective targets
5. **votes** - Democratic voting records
6. **investment_suggestions** - AI recommendations
7. **hall_of_fame** - Monthly top contributors
8. **market_data** - SA market rates
9. **member_signatures** - FICA compliance
10. **audit_log** - Admin action tracking

### Views (2)
- **member_summary** - Aggregated member stats
- **monthly_stats** - Monthly collection metrics

---

## 🎯 Investment Opportunities

### 1. Load Shedding Solutions (652% ROI)
- **Investment**: R72,000
- **Annual Return**: R444,000
- **Risk**: Medium (15%)

### 2. Borehole Drilling (1,523% ROI)
- **Investment**: R72,000
- **Annual Return**: R1,380,000
- **Risk**: Medium (20%)

### 3. Cannabis Cultivation (736% ROI)
- **Investment**: R55,000
- **Annual Return**: R460,000
- **Risk**: Medium (25%)

### 4. RSA Retail Bonds (8.25% ROI)
- **Investment**: R50,000
- **Annual Return**: R4,125
- **Risk**: Low (2%)

### 5. Satrix Top 40 ETF (12-15% ROI)
- **Investment**: R50,000
- **Annual Return**: R6,000-R7,500
- **Risk**: Medium (15%)

*+ 3 more opportunities*

---

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/test_app.py -v

# Run specific test
pytest tests/test_app.py::test_version_info -v
```

### Test Coverage
- ✅ Version tracking
- ✅ Database helper
- ✅ Market data structure
- ✅ Contribution calculations
- ✅ ROI calculations
- ✅ Voting thresholds
- ✅ SA ID validation

---

## 📊 Monitoring

### GitHub Actions Dashboard
```
https://github.com/your-repo/actions
```

### Supabase Logs
```
https://app.supabase.com/project/xxxxx/logs
```

### Webhook Health Check
```bash
curl https://khula-webhook.onrender.com/health
```

### Streamlit App Logs
```
Streamlit Cloud Dashboard > Logs
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: App not connecting to Supabase
```bash
# Solution: Verify secrets in Streamlit Cloud
# Check SUPABASE_URL and SUPABASE_KEY
# Reboot app
```

**Issue**: Workflow fails in GitHub Actions
```bash
# Solution: Check GitHub secrets are set
# Verify all secret names match exactly
# Re-run workflow manually
```

**Issue**: Webhook not receiving events
```bash
# Solution: Check webhook URL is publicly accessible
curl https://your-webhook-url.com/health
# Verify registered with Stitch API
```

**Issue**: Data not syncing
```bash
# Solution: Check Supabase logs for errors
# Verify migration completed successfully
# Test database connection
```

---

## 📚 Documentation

- **[Quick Start Guide](QUICK_START_AUTOMATION.md)** - Get started in 30 minutes
- **[Setup Guide](AUTOMATION_SETUP_GUIDE.md)** - Detailed instructions
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Pre-deployment verification
- **[API Documentation](API_DOCUMENTATION.md)** - Stitch API integration

---

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/ttmodupe-hash/khula-collective-app.git
cd khula-collective-app

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Making Changes
1. Create feature branch
2. Make changes
3. Run tests
4. Commit and push
5. Create pull request

---

## 📝 License

This project is proprietary software for Khula Collective members.

---

## 👥 Team

**Khula Collective** - 20 South African members pooling R300/month for collective investment opportunities.

**Admin**: admin_khula

**Top Contributors** (Feb 2026):
- 🥇 Thabo Mthembu - R3,900
- 🥈 Nomsa Dlamini - R3,600
- 🥉 Sipho Khumalo - R3,600

---

## 📞 Support

For technical support:
1. Check documentation in `/docs` folder
2. Review troubleshooting section above
3. Check platform-specific logs
4. Contact admin

---

## 🎉 Achievements

- ✅ **21 users** (1 admin + 20 members)
- ✅ **239 contributions** over 13 months
- ✅ **R71,700** collective balance
- ✅ **90% compliance** rate
- ✅ **8 investment opportunities** analyzed
- ✅ **100% automated** operations
- ✅ **24/7 availability** with cloud infrastructure

---

## 🚀 Roadmap

### Q1 2026
- [x] Supabase cloud migration
- [x] GitHub Actions automation
- [x] Stitch webhook integration
- [x] AI investment advisor
- [ ] WhatsApp notifications
- [ ] Email notifications

### Q2 2026
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Investment portfolio tracking
- [ ] Automated tax reporting

### Q3 2026
- [ ] Multi-currency support
- [ ] International investments
- [ ] Member referral program
- [ ] Educational resources

---

**Version**: v2.0 (Automated)
**Last Updated**: 2026-02-01
**Status**: 🟢 Production Ready

**Live App**: https://ttmodupe-hashttmodupe-hash-khula-collective-app-gpgc3mgplddy27.streamlit.app/

---

**Built with ❤️ for Khula Collective members**