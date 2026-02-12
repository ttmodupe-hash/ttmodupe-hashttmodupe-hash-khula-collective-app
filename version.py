"""
Version Tracking System
Automatically updates version based on git commits
"""

import subprocess
from datetime import datetime

def get_git_version():
    """Get version from git"""
    try:
        # Get latest commit hash
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
        
        # Get commit count
        commit_count = subprocess.check_output(
            ['git', 'rev-list', '--count', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
        
        # Get last commit date
        commit_date = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd', '--date=short'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
        
        # Get branch name
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('ascii').strip()
        
        return {
            "version": f"v2.{commit_count}",
            "commit": commit_hash,
            "date": commit_date,
            "branch": branch
        }
    
    except Exception:
        # Fallback if git is not available
        return {
            "version": "v2.0",
            "commit": "unknown",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "branch": "main"
        }

def get_version_string():
    """Get formatted version string"""
    info = get_git_version()
    return f"{info['version']} ({info['commit']}) - {info['date']}"

def get_changelog():
    """Get recent changelog from git commits"""
    try:
        # Get last 10 commits
        log = subprocess.check_output(
            ['git', 'log', '-10', '--pretty=format:%h - %s (%ar)'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8')
        
        return log.split('\n')
    
    except Exception:
        return ["No changelog available"]

# Version information
VERSION_INFO = get_git_version()
VERSION_STRING = get_version_string()
CHANGELOG = get_changelog()

# Feature flags
FEATURES = {
    "supabase_cloud": True,
    "stitch_webhook": True,
    "automated_sync": True,
    "market_intelligence": True,
    "fica_compliance": True,
    "whatsapp_notifications": False,  # Optional
    "email_notifications": False,  # Optional
}

if __name__ == "__main__":
    print(f"Khula Collective {VERSION_STRING}")
    print(f"\nFeatures:")
    for feature, enabled in FEATURES.items():
        status = "✅" if enabled else "⚠️"
        print(f"  {status} {feature.replace('_', ' ').title()}")
    
    print(f"\nRecent Changes:")
    for change in CHANGELOG[:5]:
        print(f"  • {change}")