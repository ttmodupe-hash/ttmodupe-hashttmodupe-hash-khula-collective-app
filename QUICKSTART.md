# Quick Start Guide 🚀

## Instant Access

Your FNB Savings Tracker is now running! Access it here:
**https://00303.app.super.myninja.ai**

## Getting Started in 3 Steps

### Step 1: Open the Application
Click the link above to open the FNB Savings Tracker in your browser.

### Step 2: Enable Demo Mode (Recommended for First Time)
1. Look at the left sidebar
2. Check the box "Use Demo Mode"
3. Click the "🔄 Load/Refresh Data" button

This will load sample transaction data so you can explore all features without needing API credentials.

### Step 3: Set Your Savings Goal
1. In the sidebar, find "🎯 Yearly Savings Target"
2. Enter your desired savings amount (e.g., 100000 for R100,000)
3. Watch the dashboard update automatically!

## What You'll See

### Main Dashboard
- **Progress Bar**: Visual representation of your savings progress
- **Current Savings**: Total deposits for the selected year
- **Amount Remaining**: How much more you need to reach your goal
- **Statistics**: Number of deposits, averages, and extremes

### Monthly Breakdown
- Interactive chart showing savings by month
- Hover over bars to see exact amounts

### Recent Deposits
- Table of your most recent deposit transactions
- Includes dates, amounts, and descriptions

## Using Your Real FNB Account

### Prerequisites
1. Sign up for Stitch API at https://stitch.money
2. Link your FNB account to Stitch
3. Get your API credentials (Client ID and Client Secret)

### Configuration
1. Create a `.env` file in the project directory
2. Add your credentials:
   ```
   STITCH_CLIENT_ID=your_client_id_here
   STITCH_CLIENT_SECRET=your_client_secret_here
   STITCH_API_URL=https://api.stitch.money/graphql
   ```
3. Restart the application
4. Uncheck "Use Demo Mode"
5. Click "Load/Refresh Data"

## Features to Explore

### 📊 Progress Tracking
- Set different yearly targets
- Switch between years to see historical data
- Monitor your progress in real-time

### 📈 Statistics
- View total number of deposits
- See average deposit amounts
- Identify your largest and smallest deposits

### 📅 Monthly Analysis
- Understand your savings patterns
- Identify high and low saving months
- Plan better for future months

### 💳 Transaction History
- Review recent deposits
- Check transaction descriptions
- Verify amounts and dates

## Tips for Best Results

1. **Set Realistic Goals**: Start with achievable targets and adjust as needed
2. **Regular Monitoring**: Check your progress weekly or monthly
3. **Celebrate Milestones**: Acknowledge when you reach 25%, 50%, 75% of your goal
4. **Adjust as Needed**: Life changes - update your targets accordingly
5. **Use Historical Data**: Review past years to set better future goals

## Troubleshooting

### Demo Mode Not Loading
- Refresh the page
- Click "Load/Refresh Data" again
- Check browser console for errors

### Real API Connection Issues
- Verify credentials in `.env` file
- Ensure FNB account is linked to Stitch
- Check internet connection
- Review Stitch API status

### Data Not Updating
- Click "Load/Refresh Data" button
- Check selected year in sidebar
- Verify transactions exist for selected period

## Need Help?

- **Documentation**: See README.md for detailed information
- **Stitch API**: Visit https://stitch.money/docs
- **Demo Mode**: Always available for testing

## Next Steps

1. ✅ Explore the demo mode
2. ✅ Set your first savings goal
3. ✅ Review the monthly breakdown
4. ✅ Check recent transactions
5. 🔜 Connect your real FNB account
6. 🔜 Start tracking your actual savings!

---

**Enjoy tracking your savings journey! 💰📈**