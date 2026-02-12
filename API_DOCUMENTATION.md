# API Documentation 📡

## Stitch Money API Integration

This document provides detailed information about the Stitch Money API integration in the FNB Savings Tracker.

## Overview

The application uses the Stitch Money API to:
- Authenticate users via OAuth 2.0
- Fetch bank account information
- Retrieve transaction history
- Access account balances

## Authentication

### OAuth 2.0 Client Credentials Flow

```python
# Authentication endpoint
POST https://secure.stitch.money/connect/token

# Request body
{
    "grant_type": "client_credentials",
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "scope": "client_paymentrequest client_paymentauthorizationrequest"
}

# Response
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
}
```

### Implementation

```python
from stitch_api import StitchAPIClient

# Initialize client
client = StitchAPIClient()

# Authenticate
if client.authenticate():
    print("Authentication successful!")
else:
    print("Authentication failed!")
```

## GraphQL Queries

### 1. Fetch Transactions

#### Query Structure

```graphql
query GetTransactions($accountId: ID, $from: Date, $to: Date) {
  user {
    bankAccounts {
      id
      name
      accountNumber
      bankId
      currentBalance
      availableBalance
      transactions(from: $from, to: $to) {
        edges {
          node {
            id
            amount
            currency
            date
            description
            reference
            runningBalance
          }
        }
      }
    }
  }
}
```

#### Variables

```json
{
  "from": "2024-01-01",
  "to": "2024-12-31",
  "accountId": "optional_account_id"
}
```

#### Response Structure

```json
{
  "data": {
    "user": {
      "bankAccounts": [
        {
          "id": "acc_123456",
          "name": "FNB Cheque Account",
          "accountNumber": "62***789",
          "bankId": "fnb",
          "currentBalance": 25000.00,
          "availableBalance": 25000.00,
          "transactions": {
            "edges": [
              {
                "node": {
                  "id": "txn_789012",
                  "amount": 5000.00,
                  "currency": "ZAR",
                  "date": "2024-02-11",
                  "description": "Salary Deposit",
                  "reference": "SAL202402",
                  "runningBalance": 25000.00
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

#### Implementation

```python
# Fetch transactions for the last 365 days
transactions = client.fetch_transactions(days_back=365)

# Fetch transactions for specific account
transactions = client.fetch_transactions(
    account_id="acc_123456",
    days_back=365
)
```

### 2. Get Account Balance

#### Query Structure

```graphql
query GetBalance($accountId: ID) {
  user {
    bankAccounts(filter: {accountId: $accountId}) {
      id
      name
      accountNumber
      currentBalance
      availableBalance
      currency
    }
  }
}
```

#### Variables

```json
{
  "accountId": "acc_123456"
}
```

#### Response Structure

```json
{
  "data": {
    "user": {
      "bankAccounts": [
        {
          "id": "acc_123456",
          "name": "FNB Cheque Account",
          "accountNumber": "62***789",
          "currentBalance": 25000.00,
          "availableBalance": 25000.00,
          "currency": "ZAR"
        }
      ]
    }
  }
}
```

#### Implementation

```python
# Get balance for all accounts
balance = client.get_account_balance()

# Get balance for specific account
balance = client.get_account_balance(account_id="acc_123456")
```

## API Client Methods

### StitchAPIClient Class

#### Constructor

```python
def __init__(self):
    """
    Initialize the Stitch API client with credentials
    
    Credentials are loaded from:
    1. Environment variables (.env file)
    2. Streamlit secrets (for cloud deployment)
    """
```

#### authenticate()

```python
def authenticate(self) -> bool:
    """
    Authenticate with Stitch API and obtain access token
    
    Returns:
        bool: True if authentication successful, False otherwise
    """
```

#### fetch_transactions()

```python
def fetch_transactions(
    self, 
    account_id: Optional[str] = None, 
    days_back: int = 365
) -> List[Dict]:
    """
    Fetch transaction history from Stitch API
    
    Args:
        account_id: Optional specific account ID to query
        days_back: Number of days to look back for transactions
        
    Returns:
        List[Dict]: List of transaction dictionaries
    """
```

#### get_account_balance()

```python
def get_account_balance(
    self, 
    account_id: Optional[str] = None
) -> Dict:
    """
    Get current account balance
    
    Args:
        account_id: Optional specific account ID to query
        
    Returns:
        Dict: Dictionary with balance information
    """
```

## Data Processing

### TransactionProcessor Class

#### Constructor

```python
def __init__(self, transactions: List[Dict]):
    """
    Initialize processor with transaction data
    
    Args:
        transactions: List of transaction dictionaries
    """
```

#### filter_credit_transactions()

```python
def filter_credit_transactions(self) -> pd.DataFrame:
    """
    Filter transactions to only include credits (deposits)
    
    Returns:
        pd.DataFrame: DataFrame with only credit transactions
    """
```

#### calculate_total_savings()

```python
def calculate_total_savings(self, year: int = None) -> float:
    """
    Calculate total savings (sum of credit transactions)
    
    Args:
        year: Optional year to filter by (defaults to current year)
        
    Returns:
        float: Total savings amount
    """
```

#### get_monthly_savings()

```python
def get_monthly_savings(self, year: int = None) -> pd.DataFrame:
    """
    Get savings grouped by month
    
    Args:
        year: Optional year to filter by (defaults to current year)
        
    Returns:
        pd.DataFrame: DataFrame with monthly savings totals
    """
```

#### calculate_progress()

```python
def calculate_progress(
    self, 
    target: float, 
    year: int = None
) -> Tuple[float, float, float]:
    """
    Calculate savings progress towards target
    
    Args:
        target: Target savings amount
        year: Optional year to filter by (defaults to current year)
        
    Returns:
        Tuple[float, float, float]: (current_savings, remaining, progress_percentage)
    """
```

## Error Handling

### Common Errors

#### Authentication Errors

```python
try:
    client.authenticate()
except requests.exceptions.RequestException as e:
    print(f"Authentication failed: {str(e)}")
```

#### API Request Errors

```python
try:
    transactions = client.fetch_transactions()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch transactions: {str(e)}")
except (KeyError, ValueError) as e:
    print(f"Error parsing transaction data: {str(e)}")
```

### Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 401 | Unauthorized | Check API credentials |
| 403 | Forbidden | Verify API scopes |
| 429 | Rate Limited | Implement retry logic |
| 500 | Server Error | Retry after delay |

## Rate Limiting

### Best Practices

1. **Cache Results**: Store transaction data in session state
2. **Batch Requests**: Fetch data for longer periods
3. **Implement Backoff**: Use exponential backoff for retries
4. **Monitor Usage**: Track API call frequency

### Implementation Example

```python
import time
from functools import wraps

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.RequestException as e:
                    if x == retries:
                        raise
                    sleep = backoff_in_seconds * 2 ** x
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

@retry_with_backoff(retries=3)
def fetch_with_retry():
    return client.fetch_transactions()
```

## Data Models

### Transaction Model

```python
{
    'transaction_id': str,      # Unique transaction identifier
    'amount': float,            # Transaction amount (positive for credits)
    'currency': str,            # Currency code (e.g., 'ZAR')
    'date': str,               # Transaction date (YYYY-MM-DD)
    'description': str,         # Transaction description
    'reference': str,           # Transaction reference
    'running_balance': float,   # Account balance after transaction
    'account_id': str,         # Account identifier
    'account_name': str,       # Account name
    'account_number': str,     # Masked account number
    'bank_id': str,            # Bank identifier
    'current_balance': float,  # Current account balance
    'available_balance': float # Available account balance
}
```

### Balance Model

```python
{
    'id': str,                 # Account identifier
    'name': str,               # Account name
    'accountNumber': str,      # Masked account number
    'currentBalance': float,   # Current balance
    'availableBalance': float, # Available balance
    'currency': str           # Currency code
}
```

## Testing

### Unit Tests

```python
import unittest
from stitch_api import StitchAPIClient

class TestStitchAPI(unittest.TestCase):
    def setUp(self):
        self.client = StitchAPIClient()
    
    def test_authentication(self):
        result = self.client.authenticate()
        self.assertTrue(result)
    
    def test_fetch_transactions(self):
        transactions = self.client.fetch_transactions(days_back=30)
        self.assertIsInstance(transactions, list)
```

### Integration Tests

```python
def test_full_workflow():
    # Initialize client
    client = StitchAPIClient()
    
    # Authenticate
    assert client.authenticate()
    
    # Fetch transactions
    transactions = client.fetch_transactions()
    assert len(transactions) > 0
    
    # Process data
    processor = TransactionProcessor(transactions)
    savings = processor.calculate_total_savings()
    assert savings >= 0
```

## Performance Optimization

### Caching Strategy

```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_cached_transactions():
    client = StitchAPIClient()
    return client.fetch_transactions()
```

### Pagination

```python
def fetch_transactions_paginated(page_size=100):
    all_transactions = []
    offset = 0
    
    while True:
        transactions = client.fetch_transactions(
            limit=page_size,
            offset=offset
        )
        
        if not transactions:
            break
            
        all_transactions.extend(transactions)
        offset += page_size
    
    return all_transactions
```

## Security Considerations

### Credential Management

```python
# ✅ Good: Use environment variables
import os
client_id = os.getenv('STITCH_CLIENT_ID')

# ❌ Bad: Hardcode credentials
client_id = "abc123"  # Never do this!
```

### Token Storage

```python
# Store tokens securely in session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None

# Use token
headers = {
    'Authorization': f'Bearer {st.session_state.access_token}'
}
```

## API Limits

| Limit Type | Value | Notes |
|------------|-------|-------|
| Requests per minute | 60 | Per client |
| Requests per hour | 1000 | Per client |
| Transaction history | 24 months | Maximum lookback |
| Response size | 10 MB | Maximum |

## Support Resources

- **Stitch API Documentation**: https://stitch.money/docs
- **GraphQL Playground**: https://api.stitch.money/graphql
- **Support Email**: support@stitch.money
- **Status Page**: https://status.stitch.money

## Changelog

### Version 1.0.0 (2024-02-11)
- Initial implementation
- OAuth 2.0 authentication
- Transaction fetching
- Balance retrieval
- Error handling
- Demo mode support

---

**For more information, visit the [Stitch Money Documentation](https://stitch.money/docs)**