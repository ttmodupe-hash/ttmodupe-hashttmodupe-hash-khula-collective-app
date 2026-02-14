# 🚀 Khula Collective Deployment Checklist

## Pre-Deployment Verification

### ✅ Code Quality
- [ ] All files committed to GitHub
- [ ] No syntax errors in Python files
- [ ] All imports working correctly
- [ ] Tests passing (`pytest tests/test_app.py`)
- [ ] No hardcoded credentials in code
- [ ] `.gitignore` includes sensitive files

### ✅ Database Setup
- [ ] Supabase project created
- [ ] Database schema executed (`supabase_schema.sql`)
- [ ] All tables created successfully
- [ ] Data migrated from SQLite
- [ ] Migration verified (user count, contribution count)
- [ ] Global balance correct (R71,700)

### ✅ Environment Configuration
- [ ] GitHub secrets configured
  - [ ] `SUPABASE_URL`
  - [ ] `SUPABASE_KEY`
  - [ ] `STITCH_CLIENT_ID`
  - [ ] `STITCH_CLIENT_SECRET`
  - [ ] `STITCH_WEBHOOK_SECRET`
- [ ] Streamlit secrets configured
  - [ ] `[supabase]` section
  - [ ] `[stitch]` section (optional)
  - [ ] `[twilio]` section (optional)

### ✅ GitHub Actions
- [ ] Workflow file exists (`.github/workflows/main.yml`)
- [ ] Workflow enabled in repository
- [ ] All jobs configured:
  - [ ] `streamlit-ci` (testing)
  - [ ] `fnb-sync` (daily at 8 AM SAST)
  - [ ] `monthly-reset` (1st of month)
  - [ ] `market-update` (weekly)
- [ ] Test workflow runs successfully

### ✅ Webhook Setup
- [ ] Webhook listener deployed (Render/Railway)
- [ ] Webhook URL publicly accessible
- [ ] Health endpoint responding (`/health`)
- [ ] Registered with Stitch API
- [ ] Test transaction processed successfully

### ✅ Automation Scripts
- [ ] `scripts/sync_fnb.py` - FNB sync working
- [ ] `scripts/monthly_reset.py` - Monthly reset working
- [ ] `scripts/update_market_data.py` - Market updates working
- [ ] `scripts/stitch_webhook.py` - Webhook listener working
- [ ] `scripts/migrate_to_supabase.py` - Migration completed

---

## Deployment Steps

### Step 1: Final Code Review
```bash
# Run tests
pytest tests/test_app.py -v

# Check for syntax errors
python -m py_compile app.py
python -m py_compile database_helper.py
python -m py_compile version.py

# Verify all scripts
python -m py_compile scripts/*.py
```

### Step 2: Commit and Push
```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: Add complete automation system with Supabase, webhooks, and scheduled tasks"

# Push to GitHub
git push origin main
```

### Step 3: Verify GitHub Actions
1. Go to GitHub repository
2. Click **Actions** tab
3. Verify workflow runs successfully
4. Check all jobs pass ✅

### Step 4: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select repository: `ttmodupe-hash/ttmodupe-hashttmodupe-hash-khula-collective-app`
4. Set main file: `app.py`
5. Click "Deploy"
6. Wait for deployment (~2-3 minutes)

### Step 5: Configure Streamlit Secrets
1. In Streamlit Cloud dashboard
2. Click app settings (⚙️)
3. Go to **Secrets**
4. Paste configuration:
```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "your-anon-key"

[stitch]
client_id = "your-client-id"
client_secret = "your-client-secret"
fnb_account_id = "your-account-id"
```
5. Click "Save"
6. App will restart automatically

### Step 6: Verify Deployment
1. Open deployed app URL
2. Test login (admin: `admin_khula` / `admin123`)
3. Verify all features:
   - [ ] Member dashboard loads
   - [ ] Group overview shows correct balance
   - [ ] Leaderboard displays
   - [ ] Voting system works
   - [ ] AI advisor shows recommendations
   - [ ] Payment tracker displays correctly

---

## Post-Deployment Testing

### Functional Testing
- [ ] **Login System**
  - [ ] Admin login works
  - [ ] Member login works
  - [ ] Invalid credentials rejected
  - [ ] Session persists across pages

- [ ] **Member Dashboard**
  - [ ] Personal stats display correctly
  - [ ] Monthly grid shows payment history
  - [ ] Contribution history accurate
  - [ ] AI suggestions relevant

- [ ] **Group Overview**
  - [ ] Total balance correct (R71,700)
  - [ ] Leaderboard shows top 5
  - [ ] Investment opportunities display
  - [ ] Voting system functional

- [ ] **Admin Panel**
  - [ ] Member list displays all 20 members
  - [ ] FICA compliance metrics correct
  - [ ] Signature log accessible
  - [ ] Export to CSV works

- [ ] **AI Investment Advisor**
  - [ ] Recommendations based on balance
  - [ ] Market data up-to-date
  - [ ] ROI calculations accurate
  - [ ] Risk levels appropriate

### Integration Testing
- [ ] **Supabase Connection**
  - [ ] Data loads from cloud database
  - [ ] Queries execute successfully
  - [ ] No connection errors
  - [ ] Response times acceptable (<2s)

- [ ] **GitHub Actions**
  - [ ] Daily sync scheduled correctly
  - [ ] Monthly reset scheduled correctly
  - [ ] Weekly market update scheduled
  - [ ] Manual triggers work

- [ ] **Webhook Integration**
  - [ ] Webhook receives Stitch events
  - [ ] Contributions update automatically
  - [ ] Global balance updates
  - [ ] No duplicate processing

### Performance Testing
- [ ] **Load Times**
  - [ ] Initial page load <3 seconds
  - [ ] Dashboard loads <2 seconds
  - [ ] Charts render smoothly
  - [ ] No lag on interactions

- [ ] **Database Performance**
  - [ ] Queries execute quickly
  - [ ] No timeout errors
  - [ ] Concurrent users supported
  - [ ] Data consistency maintained

### Security Testing
- [ ] **Authentication**
  - [ ] Passwords hashed (SHA-256)
  - [ ] No plain text passwords
  - [ ] Session management secure
  - [ ] Logout works correctly

- [ ] **Data Privacy**
  - [ ] Members see only own data
  - [ ] Admin sees all data
  - [ ] No unauthorized access
  - [ ] FICA data protected

- [ ] **API Security**
  - [ ] Secrets not exposed in logs
  - [ ] Webhook signature verified
  - [ ] API keys encrypted
  - [ ] HTTPS enforced

---

## Monitoring Setup

### Daily Monitoring
```bash
# Check GitHub Actions runs
# Go to: https://github.com/your-repo/actions

# Check Supabase logs
# Go to: Supabase Dashboard > Logs

# Check webhook health
curl https://your-webhook-url.com/health
```

### Weekly Monitoring
- [ ] Review market data updates
- [ ] Check AI recommendation accuracy
- [ ] Verify member contribution compliance
- [ ] Review error logs

### Monthly Monitoring
- [ ] Verify Hall of Fame archived
- [ ] Check monthly reset executed
- [ ] Review global balance accuracy
- [ ] Audit member signatures

---

## Rollback Plan

### If Deployment Fails

**Option 1: Revert to Previous Version**
```bash
# Find last working commit
git log --oneline

# Revert to that commit
git revert <commit-hash>
git push origin main
```

**Option 2: Switch Back to SQLite**
```bash
# Remove Supabase secrets from Streamlit
# App will automatically fall back to SQLite
# Restore khula_collective.db from backup
```

**Option 3: Disable Automation**
```bash
# Disable GitHub Actions workflow
# Go to: Settings > Actions > Disable workflow
```

---

## Success Criteria

Deployment is successful when:

1. ✅ **App Accessible**: Members can access app 24/7
2. ✅ **Real-time Sync**: FNB deposits update automatically
3. ✅ **Automated Tasks**: Daily/monthly/weekly jobs run without intervention
4. ✅ **Data Integrity**: All 21 users, 239 contributions, R71,700 balance intact
5. ✅ **Performance**: Page loads <3s, queries <2s
6. ✅ **Security**: Authentication working, data protected
7. ✅ **Monitoring**: Logs accessible, errors tracked

---

## Emergency Contacts

### Technical Issues
- **GitHub Actions**: Check workflow logs
- **Supabase**: Check dashboard logs
- **Webhook**: Check Render/Railway logs
- **Streamlit**: Check app logs in dashboard

### Escalation Path
1. Check troubleshooting section in `AUTOMATION_SETUP_GUIDE.md`
2. Review error logs in respective platforms
3. Test with manual script execution
4. Rollback if critical issue

---

## Post-Launch Tasks

### Week 1
- [ ] Monitor daily sync execution
- [ ] Verify webhook processing
- [ ] Check member feedback
- [ ] Fix any reported bugs

### Week 2
- [ ] Review performance metrics
- [ ] Optimize slow queries
- [ ] Update documentation
- [ ] Plan feature enhancements

### Month 1
- [ ] Verify monthly reset executed
- [ ] Review Hall of Fame archive
- [ ] Analyze usage patterns
- [ ] Plan scaling strategy

---

## Documentation Updates

After successful deployment:

- [ ] Update README.md with live URL
- [ ] Document any configuration changes
- [ ] Update troubleshooting guide
- [ ] Create user guide for members
- [ ] Record lessons learned

---

**Deployment Date**: _________________

**Deployed By**: _________________

**Live URL**: _________________

**Status**: ⬜ Pending | ⬜ In Progress | ⬜ Complete | ⬜ Failed

---

**Notes**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________