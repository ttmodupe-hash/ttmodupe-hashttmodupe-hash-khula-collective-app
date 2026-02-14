# ⚡ Quick Start: Khula Collective Automation

Get your automated investment platform running in **30 minutes**!

---

## 🎯 What You'll Get

- ✅ **Real-time FNB Sync** - Deposits automatically update contributions
- ✅ **Daily Automation** - 8 AM sync runs without manual intervention
- ✅ **Monthly Reset** - 1st of month tasks complete automatically
- ✅ **Market Intelligence** - AI advisor uses latest SA market rates
- ✅ **Cloud Database** - Accessible from anywhere, always available
- ✅ **Zero Maintenance** - Everything runs on autopilot

---

## 📋 Prerequisites (5 minutes)

### 1. Create Accounts (Free Tier)
- [ ] [Supabase](https://supabase.com) - Cloud database
- [ ] [GitHub](https://github.com) - Code repository (already have)
- [ ] [Render](https://render.com) - Webhook hosting
- [ ] [Streamlit Cloud](https://streamlit.io/cloud) - App hosting (already have)

### 2. Get API Credentials
- [ ] Stitch API credentials (if using FNB sync)
- [ ] Twilio credentials (optional, for WhatsApp)

---

## 🚀 Setup Steps

### Step 1: Supabase Setup (10 minutes)

**1.1 Create Project**
```
1. Go to supabase.com
2. Click "New Project"
3. Name: "khula-collective"
4. Password: (save securely)
5. Region: eu-west-1 (closest to SA)
6. Wait 2 minutes for setup
```

**1.2 Create Tables**
```
1. Go to SQL Editor
2. Copy contents of supabase_schema.sql
3. Click "Run"
4. Verify 10 tables created
```

**1.3 Get Credentials**
```
1. Go to Settings > API
2. Copy:
   - Project URL: https://xxxxx.supabase.co
   - anon key: eyJhbGc...
3. Save for later
```

**1.4 Migrate Data**
```bash
export SUPABASE_URL="https://xxxxx.supabase.co"
export SUPABASE_KEY="your-anon-key"
python scripts/migrate_to_supabase.py
```

✅ **Checkpoint**: You should see "✅ Migration completed successfully!"

---

### Step 2: GitHub Actions (5 minutes)

**2.1 Add Secrets**
```
1. Go to GitHub repo > Settings > Secrets
2. Click "New repository secret"
3. Add these secrets:
```

| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://xxxxx.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGc...` |
| `STITCH_CLIENT_ID` | `your-client-id` |
| `STITCH_CLIENT_SECRET` | `your-secret` |

**2.2 Enable Workflow**
```bash
git add .
git commit -m "Enable automation"
git push origin main
```

**2.3 Verify**
```
1. Go to Actions tab
2. Watch workflow run
3. All jobs should pass ✅
```

✅ **Checkpoint**: GitHub Actions workflow runs successfully

---

### Step 3: Webhook Setup (10 minutes)

**3.1 Deploy to Render**
```
1. Go to render.com
2. Click "New +" > "Web Service"
3. Connect GitHub repo
4. Configure:
   - Name: khula-webhook
   - Build: pip install -r requirements.txt
   - Start: python scripts/stitch_webhook.py
5. Add environment variables (same as GitHub secrets)
6. Click "Create"
7. Copy URL: https://khula-webhook.onrender.com
```

**3.2 Register with Stitch**
```
1. Go to Stitch Developer Portal
2. Webhooks > Add Webhook
3. URL: https://khula-webhook.onrender.com/webhook/stitch
4. Events: transaction.created, transaction.updated
5. Save webhook secret
```

**3.3 Test**
```bash
# Test health endpoint
curl https://khula-webhook.onrender.com/health

# Should return: {"status": "healthy"}
```

✅ **Checkpoint**: Webhook responds to health check

---

### Step 4: Streamlit Deployment (5 minutes)

**4.1 Update Secrets**
```
1. Go to Streamlit Cloud dashboard
2. Select your app
3. Settings > Secrets
4. Add:
```

```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "your-anon-key"

[stitch]
client_id = "your-client-id"
client_secret = "your-client-secret"
fnb_account_id = "your-account-id"
```

**4.2 Redeploy**
```
1. Click "Reboot app"
2. Wait 2 minutes
3. App will restart with cloud database
```

**4.3 Verify**
```
1. Open app URL
2. Login as admin
3. Check balance: R71,700
4. Verify all 20 members
5. Test voting system
```

✅ **Checkpoint**: App loads with Supabase data

---

## ✅ Verification (5 minutes)

### Test Automation

**1. Daily Sync (8 AM SAST)**
```bash
# Manual trigger
Go to: GitHub > Actions > FNB Sync > Run workflow
```

**2. Monthly Reset (1st of month)**
```bash
# Manual trigger
python scripts/monthly_reset.py
```

**3. Market Update (Weekly)**
```bash
# Manual trigger
python scripts/update_market_data.py
```

**4. Webhook**
```bash
# Make test R300 deposit
# Check webhook logs in Render
# Verify contribution updated in app
```

---

## 🎉 Success!

Your Khula Collective platform is now fully automated!

### What Happens Now?

**Every Day at 8 AM SAST:**
- ✅ FNB transactions synced
- ✅ Pending contributions updated
- ✅ Global balance refreshed

**Every Monday:**
- ✅ Market rates updated
- ✅ AI recommendations refreshed

**Every 1st of Month:**
- ✅ Hall of Fame archived
- ✅ New contribution records created
- ✅ Monthly targets reset

**Real-time:**
- ✅ FNB deposits trigger instant updates
- ✅ Members see changes immediately

---

## 📊 Monitoring

### Daily Checks
```bash
# GitHub Actions
https://github.com/your-repo/actions

# Supabase Logs
https://app.supabase.com/project/xxxxx/logs

# Webhook Health
curl https://khula-webhook.onrender.com/health
```

### Weekly Review
- Check market data accuracy
- Verify AI recommendations
- Review member compliance

### Monthly Review
- Verify Hall of Fame archived
- Check monthly reset executed
- Audit global balance

---

## 🐛 Troubleshooting

### Issue: Workflow fails
```bash
# Check GitHub Actions logs
# Verify all secrets are set
# Re-run workflow manually
```

### Issue: Webhook not receiving events
```bash
# Check webhook URL is accessible
curl https://your-webhook-url.com/health

# Verify registered with Stitch
# Check webhook secret matches
```

### Issue: App not connecting to Supabase
```bash
# Verify secrets in Streamlit Cloud
# Check SUPABASE_URL and SUPABASE_KEY
# Reboot app
```

### Issue: Data not syncing
```bash
# Check Supabase logs for errors
# Verify migration completed
# Test database connection
```

---

## 📞 Need Help?

1. Check `AUTOMATION_SETUP_GUIDE.md` for detailed instructions
2. Review `DEPLOYMENT_CHECKLIST.md` for verification steps
3. Check error logs in respective platforms
4. Test with manual script execution

---

## 🚀 Next Steps

### Week 1
- [ ] Monitor daily sync execution
- [ ] Share app URL with members
- [ ] Collect feedback
- [ ] Fix any issues

### Week 2
- [ ] Optimize performance
- [ ] Update documentation
- [ ] Plan enhancements

### Month 1
- [ ] Review automation effectiveness
- [ ] Analyze usage patterns
- [ ] Plan scaling strategy

---

## 📝 Configuration Summary

After setup, you'll have:

```
✅ Supabase Cloud Database
   - 10 tables with all data
   - Real-time queries
   - Automatic backups

✅ GitHub Actions
   - Daily FNB sync (8 AM SAST)
   - Monthly reset (1st of month)
   - Weekly market update (Mondays)

✅ Webhook Listener
   - Real-time deposit notifications
   - Automatic contribution updates
   - Global balance sync

✅ Streamlit App
   - Connected to cloud database
   - 24/7 availability
   - Auto-deploy on push
```

---

**Setup Time**: ~30 minutes
**Maintenance**: ~5 minutes/week
**Uptime**: 99.9%
**Cost**: R0 (free tier)

**Congratulations! Your investment platform is now running on autopilot! 🎉**