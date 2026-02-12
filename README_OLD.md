# FNB Savings Tracker 💰

A high-performance Streamlit application for monitoring savings in South African FNB bank accounts using the Stitch API.

## Features

### Core Functionality
- **Live Banking Integration**: Connects to FNB accounts via Stitch Money API
- **Goal Tracking**: Set and monitor yearly savings targets in ZAR
- **Real-time Monitoring**: Automatically filters and tracks credit transactions (deposits)
- **Visual Dashboard**: 
  - Progress bar showing savings vs. target
  - Metric cards displaying remaining amount
  - Monthly savings breakdown chart
  - Recent deposits table view
- **Demo Mode**: Test the application without API credentials

### Technical Highlights
- GraphQL API integration with Stitch Money
- Pandas-based data processing and filtering
- Dark mode friendly UI
- Session state management for data persistence
- Secure credential management via environment variables or Streamlit Secrets

## Installation

### Prerequisites
- Python 3.8 or higher
- Stitch API credentials (or use demo mode)

### Setup Steps

1. **Clone or download the project files**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure API credentials** (Optional - skip if using demo mode):

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Stitch API credentials:
   ```
   STITCH_CLIENT_ID=your_client_id_here
   STITCH_CLIENT_SECRET=your_client_secret_here
   STITCH_API_URL=https://api.stitch.money/graphql
   ```

   **Alternative**: Use Streamlit Secrets (for deployment)
   
   Create `.streamlit/secrets.toml`:
   ```toml
   STITCH_CLIENT_ID = "your_client_id_here"
   STITCH_CLIENT_SECRET = "your_client_secret_here"
   STITCH_API_URL = "https://api.stitch.money/graphql"
   ```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using Demo Mode

If you don't have Stitch API credentials yet:

1. Launch the application
2. Check the "Use Demo Mode" checkbox in the sidebar
3. Click "Load/Refresh Data"
4. Explore the features with sample data

### Connecting Your FNB Account

1. Obtain Stitch API credentials from [stitch.money](https://stitch.money)
2. Configure credentials in `.env` or Streamlit Secrets
3. Uncheck "Use Demo Mode" in the sidebar
4. Click "Load/Refresh Data"
5. The app will fetch your real transaction data

### Setting Your Savings Goal

1. In the sidebar, enter your "Yearly Savings Target" in ZAR
2. Select the year you want to track
3. The dashboard will automatically update to show your progress

## Project Structure

```
fnb-savings-tracker/
├── app.py                 # Main Streamlit application
├── stitch_api.py         # Stitch API integration module
├── data_processor.py     # Transaction data processing
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment configuration
└── README.md            # This file
```

## API Integration Details

### Stitch API
The application uses the Stitch Money API to:
- Authenticate using OAuth 2.0 client credentials flow
- Fetch transaction history via GraphQL queries
- Retrieve account balance information
- Filter transactions by date range

### GraphQL Query Structure
```graphql
query GetTransactions($accountId: ID, $from: Date, $to: Date) {
  user {
    bankAccounts {
      id
      name
      accountNumber
      transactions(from: $from, to: $to) {
        edges {
          node {
            id
            amount
            date
            description
          }
        }
      }
    }
  }
}
```

## Data Processing

### Transaction Filtering
- **Credit Transactions**: Automatically filters for positive amounts (deposits)
- **Date Range**: Configurable lookback period (default: 365 days)
- **Year-based**: Groups and analyzes by selected year

### Calculations
- **Total Savings**: Sum of all credit transactions for the year
- **Progress Percentage**: (Current Savings / Target) × 100
- **Remaining Amount**: Target - Current Savings
- **Monthly Breakdown**: Aggregated savings per month
- **Statistics**: Average, largest, and smallest deposits

## Security Best Practices

1. **Never commit credentials**: The `.env` file is gitignored
2. **Use environment variables**: Keep sensitive data out of code
3. **Secure API tokens**: Stitch API uses OAuth 2.0 for authentication
4. **HTTPS only**: Always use secure connections in production

## Troubleshooting

### Common Issues

**"Authentication failed"**
- Verify your Stitch API credentials are correct
- Check that credentials are properly set in `.env` or Streamlit Secrets
- Ensure you have the correct API scopes

**"No transactions loaded"**
- Enable demo mode to test the application
- Verify your FNB account is linked to Stitch
- Check that the date range includes transactions

**"Failed to fetch transactions"**
- Check your internet connection
- Verify the Stitch API is accessible
- Review API rate limits

## Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP library for API calls
- **pandas**: Data manipulation and analysis
- **python-dotenv**: Environment variable management
- **plotly**: Interactive visualizations

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is provided as-is for educational and personal use.

## Support

For Stitch API support, visit: https://stitch.money/docs
For application issues, please open an issue in the repository.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Banking data via [Stitch Money](https://stitch.money)
- Designed for South African FNB bank accounts