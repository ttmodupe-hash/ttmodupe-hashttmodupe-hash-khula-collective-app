# Khula Collective Automation Setup Guide

## 🎯 Overview

This guide will help you set up complete automation for the Khula Collective platform, including:

1. **GitHub CI/CD** - Automated testing and deployment
2. **Supabase Cloud Database** - Migrate from SQLite to PostgreSQL
3. **FNB Stitch Sync** - Real-time deposit notifications
4. **Intelligent Automation** - Monthly resets and market updates
5. **Version Control** - Automatic version tracking

---

## 📋 Prerequisites

- GitHub account with repository access
- Supabase account (free tier available)
- Stitch API credentials (for FNB integration)
- Streamlit Cloud account (free tier available)

---

## 🚀 Part 1: Supabase Cloud Database Setup

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Create a new organization (if needed)
4. Create a new project:
   - **Name**: `khula-collective`
   - **Database Password**: (save this securely)
   - **Region**: Choose closest to South Africa (e.g., `eu-west-1`)
5. Wait for project to initialize (~2 minutes)

### Step 2: Create Database Tables

1. In Supabase Dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy and paste the contents of `supabase_schema.sql`
4. Click "Run" to create all tables
5. Verify tables created in **Table Editor**

### Step 3: Get API Credentials

1. Go to **Settings** > **API**
2. Copy these values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: `eyJhbGc...` (long string)
3. Save these for later use

### Step 4: Migrate Data from SQLite

Run the migration script:

```bash
# Set environment variables
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_KEY="your-anon-key"

# Run migration
python scripts/migrate_to_supabase.py
```

**Expected Output:**
```
🚀 Starting SQLite to Supabase Migration...
✅ Connected to SQLite: khula_collective.db
✅ Connected to Supabase: https://xxxxx.supabase.co
👥 Migrating users...
✅ Migrated 21/21 users
💰 Migrating contributions...
✅ Migrated 239/239 contributions
🌍 Migrating global account sync...
✅ Migrated global balance: R71,700.00
✅ Migration completed successfully!
```

---

## 🔧 Part 2: GitHub Actions Setup

### Step 1: Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** > **Secrets and variables** > **Actions**
3. Click "New repository secret"
4. Add the following secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `SUPABASE_URL` | `https://xxxxx.supabase.co` | Your Supabase project URL |
| `SUPABASE_KEY` | `eyJhbGc...` | Your Supabase anon key |
| `STITCH_CLIENT_ID` | `your-client-id` | Stitch API client ID |
| `STITCH_CLIENT_SECRET` | `your-secret` | Stitch API client secret |
| `STITCH_WEBHOOK_SECRET` | `your-webhook-secret` | Webhook verification secret |

### Step 2: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. The workflow will run automatically on every push to `main`

### Step 3: Verify Workflow

1. Make a test commit:
   ```bash
   git add .
   git commit -m "Enable automation"
   git push origin main
   ```
2. Go to **Actions** tab
3. Watch the workflow run
4. Verify all jobs pass ✅

---

## 📡 Part 3: Stitch Webhook Setup

### Step 1: Deploy Webhook Listener

**Option A: Deploy to Render (Recommended)**

1. Go to [render.com](https://render.com)
2. Click "New +" > "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `khula-webhook`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python scripts/stitch_webhook.py`
5. Add environment variables (same as GitHub secrets)
6. Click "Create Web Service"
7. Copy the service URL (e.g., `https://khula-webhook.onrender.com`)

**Option B: Deploy to Railway**

1. Go to [railway.app](https://railway.app)
2. Click "New Project" > "Deploy from GitHub repo"
3. Select your repository
4. Add environment variables
5. Deploy and copy the URL

### Step 2: Register Webhook with Stitch

1. Go to Stitch Developer Portal
2. Navigate to **Webhooks**
3. Click "Add Webhook"
4. Configure:
   - **URL**: `https://your-webhook-url.com/webhook/stitch`
   - **Events**: Select `transaction.created`, `transaction.updated`
   - **Secret**: (generate and save in GitHub secrets)
5. Click "Save"

### Step 3: Test Webhook

1. Make a test R300 deposit to FNB account
2. Check webhook logs in Render/Railway
3. Verify contribution updated in Supabase
4. Check Streamlit app for updated status

---

## ⏰ Part 4: Scheduled Automation

### Daily FNB Sync (8 AM SAST)

**Already configured in `.github/workflows/main.yml`**

- Runs every day at 06:00 UTC (08:00 SAST)
- Syncs last 7 days of transactions
- Updates pending contributions to received
- Updates global balance

**Manual Trigger:**
```bash
# Go to GitHub Actions > FNB Sync > Run workflow
```

### Monthly Reset (1st of Month)

**Automatically runs on 1st of every month**

- Archives previous month's Hall of Fame
- Creates new contribution records for all members
- Resets monthly targets
- Sends monthly summary

**Manual Trigger:**
```bash
python scripts/monthly_reset.py
```

### Weekly Market Update (Mondays)

**Runs every Monday at 06:00 UTC**

- Fetches latest SARB repo rate
- Updates prime lending rate
- Fetches inflation data
- Updates JSE All Share Index
- Refreshes AI investment recommendations

**Manual Trigger:**
```bash
python scripts/update_market_data.py
```

---

## 🎨 Part 5: Streamlit Cloud Deployment

### Step 1: Update Streamlit Secrets

1. Go to Streamlit Cloud dashboard
2. Select your app
3. Click **Settings** > **Secrets**
4. Add the following:

```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "your-anon-key"

[stitch]
client_id = "your-client-id"
client_secret = "your-client-secret"
fnb_account_id = "your-account-id"
```

### Step 2: Update App to Use Supabase

The app will automatically detect Supabase configuration and switch from SQLite.

**No code changes needed!** The `database_helper.py` handles this automatically.

### Step 3: Deploy

1. Push changes to GitHub
2. Streamlit Cloud will auto-deploy
3. Verify app loads correctly
4. Test all features with cloud database

---

## ✅ Verification Checklist

### Database Migration
- [ ] All 21 users migrated
- [ ] All 239 contributions migrated
- [ ] Global balance correct (R71,700)
- [ ] Votes and suggestions migrated

### GitHub Actions
- [ ] Workflow runs on push
- [ ] All tests pass
- [ ] Daily sync scheduled
- [ ] Monthly reset scheduled
- [ ] Weekly market update scheduled

### Webhook Integration
- [ ] Webhook deployed and accessible
- [ ] Registered with Stitch API
- [ ] Test transaction processed
- [ ] Contribution status updated

### Streamlit App
- [ ] App connects to Supabase
- [ ] All features working
- [ ] Real-time data updates
- [ ] No errors in logs

---

## 🐛 Troubleshooting

### Migration Issues

**Problem**: "Table already exists" error
```bash
# Solution: Drop tables in Supabase SQL Editor
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS monthly_contributions CASCADE;
# ... (drop all tables)
# Then re-run migration
```

**Problem**: "Connection refused" to Supabase
```bash
# Solution: Check firewall/network settings
# Verify SUPABASE_URL and SUPABASE_KEY are correct
```

### Webhook Issues

**Problem**: Webhook not receiving events
```bash
# Solution: Check webhook URL is publicly accessible
curl https://your-webhook-url.com/health
# Should return: {"status": "healthy"}
```

**Problem**: "Invalid signature" error
```bash
# Solution: Verify STITCH_WEBHOOK_SECRET matches Stitch portal
# Regenerate secret if needed
```

### GitHub Actions Issues

**Problem**: Workflow fails with "Missing secrets"
```bash
# Solution: Add all required secrets in GitHub Settings
# Verify secret names match exactly (case-sensitive)
```

---

## 📊 Monitoring & Maintenance

### Daily Checks
- [ ] Check GitHub Actions runs (should be green ✅)
- [ ] Verify webhook health endpoint
- [ ] Monitor Supabase dashboard for errors

### Weekly Checks
- [ ] Review market data updates
- [ ] Check AI recommendations accuracy
- [ ] Verify member contribution compliance

### Monthly Checks
- [ ] Verify Hall of Fame archived correctly
- [ ] Check monthly reset executed
- [ ] Review global balance accuracy
- [ ] Audit member signatures (FICA compliance)

---

## 🎉 Success Criteria

Your automation is fully operational when:

1. ✅ **Real-time Sync**: FNB deposits automatically update contributions
2. ✅ **Daily Automation**: 8 AM sync runs without manual intervention
3. ✅ **Monthly Reset**: 1st of month tasks complete automatically
4. ✅ **Market Intelligence**: AI advisor uses latest rates
5. ✅ **Cloud Database**: All data accessible from anywhere
6. ✅ **Zero Downtime**: Members can access app 24/7

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Check Supabase logs in dashboard
4. Verify webhook logs in Render/Railway
5. Test with manual script execution

---

## 🚀 Next Steps

After automation is complete:

1. **Member Onboarding**: Share app URL with all 20 members
2. **Training Session**: Walk through new features
3. **Monitoring Setup**: Set up alerts for failed workflows
4. **Backup Strategy**: Configure Supabase automatic backups
5. **Scale Planning**: Monitor usage and upgrade if needed

---

**Congratulations! Your Khula Collective platform is now fully automated! 🎉**