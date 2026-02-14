# 🔍 Review Mode Guide - Khula Collective

## Overview

**Review Mode** is a special testing feature that allows your 20 members to safely explore and test the Khula Collective platform **without accessing real bank data or credentials**.

---

## 🎯 Purpose

Review Mode enables:
- ✅ **Safe Testing** - Members can test all features without affecting real data
- ✅ **Hidden Credentials** - Real Stitch API credentials remain completely hidden
- ✅ **Full Feature Access** - Login, FICA registration, voting, and all dashboards work normally
- ✅ **Realistic Data** - Uses 14 months of mock data (Jan 2025 - Feb 2026) with R71,700 balance
- ✅ **Member Onboarding** - Perfect for training sessions and demos

---

## 🚀 How to Enable Review Mode

### For Admin Only

1. **Login as Admin**
   - Username: `admin_khula`
   - Password: `admin123`

2. **Toggle Review Mode**
   - Look for the **"🔍 Review Mode"** section in the sidebar
   - Toggle **"Enable Review Mode"** to ON
   - You'll see: "📊 Using mock data for testing"

3. **Visual Confirmation**
   - A bright orange banner appears at the top:
     ```
     🔍 REVIEW MODE ACTIVE
     Using mock data for testing. Real bank credentials are hidden.
     ```

4. **Share with Members**
   - Members can now login and test all features
   - All data they see is mock data
   - No real bank API calls are made

---

## 📊 What Members See in Review Mode

### Mock Data Includes:

1. **20 Member Profiles**
   - Realistic South African names
   - Full FICA-compliant profiles
   - Login credentials work normally

2. **14 Months of Contributions**
   - January 2025 - February 2026
   - R300/month per member
   - ~90% payment compliance
   - Total balance: R71,700

3. **Investment Opportunities**
   - 5 realistic SA investment options
   - Load shedding solutions
   - Borehole drilling
   - Cannabis cultivation
   - RSA Retail Bonds
   - Satrix Top 40 ETF

4. **Voting Data**
   - Pre-populated votes on proposals
   - Members can cast test votes
   - Vote counts update in real-time

5. **Market Data**
   - SARB Repo Rate: 8.25%
   - Prime Rate: 11.75%
   - Inflation: 5.2%
   - JSE All Share: 78,500

---

## ✅ Features Available in Review Mode

### Fully Functional:
- ✅ **Login System** - All 20 members can login
- ✅ **FICA Registration** - Test SA ID validation, document upload
- ✅ **Constitution Signing** - Digital signature capture
- ✅ **Member Dashboard** - Personal stats, contribution history
- ✅ **Group Overview** - Total balance, monthly charts
- ✅ **Voting System** - Cast votes on investment proposals
- ✅ **AI Advisor** - Market-aware recommendations
- ✅ **Payment Tracker** - Monthly contribution grid
- ✅ **Leaderboard** - Top 5 contributors

### What's Different:
- ⚠️ **No Real Bank API Calls** - Stitch API is not contacted
- ⚠️ **Votes Don't Save** - Test votes don't persist (by design)
- ⚠️ **Mock Data Only** - All charts/tables use seed data

---

## 🔄 Switching Between Modes

### Admin Can Toggle Anytime:

**Review Mode → Live Mode:**
1. Toggle OFF "Enable Review Mode"
2. Banner disappears
3. Real bank data loads
4. Stitch API credentials used

**Live Mode → Review Mode:**
1. Toggle ON "Enable Review Mode"
2. Orange banner appears
3. Mock data loads
4. Real credentials hidden

---

## 👥 Member Login Credentials (Review Mode)

All members use the same password: `password123`

### Sample Usernames:
- `thabo_mthembu`
- `nomsa_dlamini`
- `sipho_khumalo`
- `zanele_ndlovu`
- `mandla_zulu`
- `lindiwe_nkosi`
- `bongani_mokoena`
- `precious_mahlangu`
- `tshepo_molefe`
- `nandi_buthelezi`
- *(+ 10 more members)*

---

## 📋 Testing Checklist for Members

Use this checklist during review sessions:

### Login & Authentication
- [ ] Login with username/password
- [ ] View personal dashboard
- [ ] Check contribution history
- [ ] Logout and re-login

### FICA Compliance
- [ ] Enter SA ID number
- [ ] Verify auto-extracted DOB/gender
- [ ] Upload ID document (test file)
- [ ] Upload proof of residence
- [ ] Complete RICA verification

### Constitution
- [ ] Read full constitution
- [ ] Check "I agree" checkbox
- [ ] Enter full name
- [ ] Sign digitally
- [ ] Verify signature timestamp

### Voting System
- [ ] View investment proposals
- [ ] Read AI recommendations
- [ ] Cast vote on proposal
- [ ] See "You voted" badge
- [ ] Check vote counts update

### Dashboard Features
- [ ] View total collective pot
- [ ] Check monthly growth chart
- [ ] See personal contribution stats
- [ ] View leaderboard rankings
- [ ] Check AI advisor suggestions

---

## 🎓 Training Session Agenda

### Recommended Flow (30 minutes):

**1. Introduction (5 min)**
- Explain Review Mode purpose
- Show orange banner
- Emphasize safety of testing

**2. Login Demo (5 min)**
- Admin demonstrates login
- Members login individually
- Verify everyone can access

**3. FICA Registration (10 min)**
- Walk through SA ID validation
- Show document upload
- Complete constitution signing

**4. Dashboard Tour (5 min)**
- Show collective pot balance
- Explain monthly charts
- Review personal stats

**5. Voting Practice (5 min)**
- View investment proposals
- Cast test votes
- See real-time updates

**6. Q&A (5 min)**
- Answer member questions
- Address concerns
- Collect feedback

---

## 🔒 Security & Privacy

### What's Protected:
- ✅ **Real Bank Credentials** - Never exposed in Review Mode
- ✅ **Stitch API Keys** - Completely hidden from members
- ✅ **Live Data** - Real contributions remain private
- ✅ **Member Privacy** - Each member sees only their own data

### What Members Can't Access:
- ❌ Real bank account details
- ❌ Actual FNB transaction data
- ❌ Other members' personal information
- ❌ Admin-only features

---

## 📊 Mock Data Statistics

### Generated Data:
- **Members**: 20 active + 1 admin
- **Time Period**: 14 months (Jan 2025 - Feb 2026)
- **Total Contributions**: 239 payments
- **Total Balance**: R71,700
- **Payment Compliance**: ~90%
- **Investment Proposals**: 5 opportunities
- **Vote Participation**: ~85%

### Top 5 Mock Contributors:
1. 🥇 Thabo Mthembu - R3,900
2. 🥈 Nomsa Dlamini - R3,600
3. 🥉 Sipho Khumalo - R3,600
4. Zanele Ndlovu - R3,300
5. Mandla Zulu - R3,300

---

## 🐛 Troubleshooting

### Issue: Review Mode toggle not visible
**Solution**: Only admin users can see the toggle. Login as `admin_khula`.

### Issue: Orange banner doesn't appear
**Solution**: Refresh the page after enabling Review Mode.

### Issue: Mock data not loading
**Solution**: Ensure `seed_data.py` file exists in the same directory as `app.py`.

### Issue: Members see real data
**Solution**: Admin must toggle Review Mode ON in sidebar.

### Issue: Votes not saving
**Solution**: This is expected behavior in Review Mode. Votes are simulated only.

---

## 🎯 Best Practices

### For Admin:
1. **Enable Review Mode** before sharing app URL with members
2. **Announce clearly** that it's a testing environment
3. **Collect feedback** during review sessions
4. **Switch to Live Mode** only when ready for production
5. **Keep credentials secure** - never share real bank API keys

### For Members:
1. **Test thoroughly** - try all features
2. **Report issues** - note any bugs or confusion
3. **Ask questions** - clarify anything unclear
4. **Provide feedback** - suggest improvements
5. **Don't worry** - nothing you do affects real data

---

## 📞 Support

### Common Questions:

**Q: Can I break anything in Review Mode?**
A: No! All data is mock data. Test freely.

**Q: Will my test votes count?**
A: No, votes in Review Mode are for testing only.

**Q: Can I see other members' data?**
A: No, privacy rules still apply. You only see your own data.

**Q: How do I know I'm in Review Mode?**
A: Look for the bright orange banner at the top of the page.

**Q: When will we use real data?**
A: Admin will switch to Live Mode after all members complete testing.

---

## 🚀 Going Live

### When Ready for Production:

1. **Complete Testing**
   - All members tested features
   - Feedback collected and addressed
   - No critical bugs reported

2. **Admin Actions**
   - Toggle Review Mode OFF
   - Verify real bank credentials configured
   - Test Stitch API connection

3. **Member Communication**
   - Announce switch to Live Mode
   - Explain real data is now active
   - Remind about R300/month commitment

4. **Monitor**
   - Watch for real FNB deposits
   - Verify contributions update correctly
   - Check member feedback

---

## 📈 Success Metrics

Track these during review period:

- [ ] All 20 members successfully logged in
- [ ] 100% FICA registration completion
- [ ] 100% constitution signatures
- [ ] 80%+ members cast test votes
- [ ] Zero critical bugs reported
- [ ] Positive member feedback
- [ ] Members understand platform features

---

## 🎉 Benefits of Review Mode

### For Admin:
- ✅ Safe member onboarding
- ✅ Hidden real credentials
- ✅ Controlled testing environment
- ✅ Collect feedback before launch
- ✅ Train members effectively

### For Members:
- ✅ Risk-free exploration
- ✅ Learn platform features
- ✅ Practice voting
- ✅ Understand FICA process
- ✅ Build confidence

---

**Review Mode makes member onboarding safe, easy, and effective! 🎉**

**Questions? Contact admin or refer to this guide.**