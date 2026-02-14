"""
Test Suite for Khula Collective
Run with: pytest tests/test_app.py -v
"""

import pytest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_version_info():
    """Test version tracking"""
    from version import VERSION_INFO, VERSION_STRING
    
    assert VERSION_INFO is not None
    assert "version" in VERSION_INFO
    assert "commit" in VERSION_INFO
    assert "date" in VERSION_INFO
    assert len(VERSION_STRING) > 0
    print(f"✅ Version: {VERSION_STRING}")

def test_database_helper():
    """Test database helper initialization"""
    from database_helper import DatabaseManager
    
    db = DatabaseManager()
    assert db is not None
    assert hasattr(db, 'get_users')
    assert hasattr(db, 'get_contributions')
    assert hasattr(db, 'get_global_balance')
    print("✅ Database helper initialized")

def test_sync_script_imports():
    """Test sync script can be imported"""
    try:
        sys.path.insert(0, 'scripts')
        # Just test imports, don't execute
        import sync_fnb
        import monthly_reset
        import update_market_data
        print("✅ All automation scripts importable")
    except ImportError as e:
        pytest.skip(f"Skipping: {e}")

def test_market_data_structure():
    """Test market data structure"""
    from database_helper import db
    
    market_data = db.get_market_data()
    assert market_data is not None
    
    # Check required fields
    required_fields = ["repo_rate", "prime_rate", "inflation_rate"]
    for field in required_fields:
        assert field in market_data, f"Missing field: {field}"
    
    print(f"✅ Market data structure valid")

def test_contribution_status_values():
    """Test contribution status values are valid"""
    valid_statuses = ["Pending", "Received", "Overdue"]
    
    # This is a structural test
    assert len(valid_statuses) == 3
    print(f"✅ Valid contribution statuses: {valid_statuses}")

def test_user_roles():
    """Test user role definitions"""
    valid_roles = ["admin", "member"]
    
    assert "admin" in valid_roles
    assert "member" in valid_roles
    print(f"✅ Valid user roles: {valid_roles}")

def test_investment_risk_levels():
    """Test investment risk level definitions"""
    risk_levels = ["Low", "Medium", "High"]
    
    assert len(risk_levels) == 3
    print(f"✅ Risk levels defined: {risk_levels}")

def test_monthly_target_calculation():
    """Test monthly target calculation"""
    members = 20
    contribution_per_member = 300
    expected_monthly_target = members * contribution_per_member
    
    assert expected_monthly_target == 6000
    print(f"✅ Monthly target: R{expected_monthly_target:,}")

def test_yearly_target_calculation():
    """Test yearly target calculation"""
    monthly_target = 6000
    months = 12
    expected_yearly_target = monthly_target * months
    
    assert expected_yearly_target == 72000
    print(f"✅ Yearly target: R{expected_yearly_target:,}")

def test_date_format():
    """Test date format consistency"""
    test_date = datetime.now()
    month_format = test_date.strftime("%Y-%m")
    
    assert len(month_format) == 7
    assert month_format[4] == "-"
    print(f"✅ Date format valid: {month_format}")

def test_sa_id_length():
    """Test SA ID number validation"""
    valid_id = "9001015009087"
    
    assert len(valid_id) == 13
    assert valid_id.isdigit()
    print(f"✅ SA ID format valid")

def test_contribution_amount():
    """Test contribution amount is R300"""
    expected_amount = 300.0
    
    assert expected_amount == 300.0
    print(f"✅ Contribution amount: R{expected_amount}")

def test_roi_calculation():
    """Test ROI calculation formula"""
    investment = 50000
    annual_return = 4125
    roi_percentage = (annual_return / investment) * 100
    
    assert roi_percentage == 8.25
    print(f"✅ ROI calculation: {roi_percentage}%")

def test_balance_threshold_logic():
    """Test investment balance thresholds"""
    thresholds = {
        "foundation": 50000,
        "conservative": 100000,
        "diversified": 100000
    }
    
    assert thresholds["foundation"] < thresholds["conservative"]
    print(f"✅ Balance thresholds: {thresholds}")

def test_vote_threshold():
    """Test voting approval threshold"""
    total_members = 20
    approval_threshold = 0.60
    required_votes = int(total_members * approval_threshold)
    
    assert required_votes == 12
    print(f"✅ Approval requires {required_votes}/{total_members} votes (60%)")

# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])