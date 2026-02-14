"""
Stitch Webhook Listener
Receives real-time deposit notifications from Stitch API
Automatically updates contributions from Pending to Received
"""

from flask import Flask, request, jsonify
import os
import hmac
import hashlib
from datetime import datetime
from supabase import create_client, Client

app = Flask(__name__)

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
STITCH_WEBHOOK_SECRET = os.getenv("STITCH_WEBHOOK_SECRET")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_webhook_signature(payload, signature):
    """Verify webhook signature from Stitch"""
    expected_signature = hmac.new(
        STITCH_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

@app.route('/webhook/stitch', methods=['POST'])
def stitch_webhook():
    """Handle incoming Stitch webhook notifications"""
    
    # Verify signature
    signature = request.headers.get('X-Stitch-Signature')
    if not signature or not verify_webhook_signature(request.data, signature):
        return jsonify({"error": "Invalid signature"}), 401
    
    # Parse webhook data
    data = request.json
    event_type = data.get('type')
    
    print(f"📨 Received webhook: {event_type}")
    
    if event_type == 'transaction.created':
        handle_transaction_created(data)
    elif event_type == 'transaction.updated':
        handle_transaction_updated(data)
    else:
        print(f"⚠️ Unhandled event type: {event_type}")
    
    return jsonify({"status": "success"}), 200

def handle_transaction_created(data):
    """Handle new transaction notification"""
    
    transaction = data.get('data', {})
    amount = float(transaction.get('amount', 0))
    description = transaction.get('description', '').lower()
    txn_date = transaction.get('date')
    txn_id = transaction.get('id')
    
    print(f"💰 New transaction: R{amount} on {txn_date}")
    
    # Filter for R300 deposits (Khula contributions)
    if amount != 300.0:
        print(f"⚠️ Amount is not R300, skipping...")
        return
    
    # Find matching pending contribution
    try:
        txn_datetime = datetime.strptime(txn_date, "%Y-%m-%d")
        month_str = txn_datetime.strftime("%Y-%m")
        
        # Query pending contributions for this month
        result = supabase.table("monthly_contributions").select("*").eq("status", "Pending").eq("month", month_str).eq("amount", 300).execute()
        
        if not result.data:
            print(f"⚠️ No pending contributions found for {month_str}")
            return
        
        # Update first matching contribution
        contribution = result.data[0]
        
        supabase.table("monthly_contributions").update({
            "status": "Received",
            "payment_date": txn_date,
            "transaction_reference": txn_id
        }).eq("id", contribution["id"]).execute()
        
        print(f"✅ Updated contribution for user {contribution['user_id']} - {month_str}")
        
        # Update global balance
        update_global_balance(amount)
        
        # Send confirmation notification (WhatsApp/Email)
        send_payment_confirmation(contribution['user_id'], amount, txn_date)
    
    except Exception as e:
        print(f"❌ Error processing transaction: {e}")

def handle_transaction_updated(data):
    """Handle transaction update notification"""
    
    transaction = data.get('data', {})
    txn_id = transaction.get('id')
    status = transaction.get('status')
    
    print(f"🔄 Transaction {txn_id} updated: {status}")
    
    # Handle transaction status changes (e.g., reversed, failed)
    if status == 'reversed':
        handle_transaction_reversal(txn_id)

def handle_transaction_reversal(txn_id):
    """Handle reversed transaction"""
    
    try:
        # Find contribution with this transaction reference
        result = supabase.table("monthly_contributions").select("*").eq("transaction_reference", txn_id).execute()
        
        if result.data:
            contribution = result.data[0]
            
            # Revert to Pending
            supabase.table("monthly_contributions").update({
                "status": "Pending",
                "payment_date": None,
                "transaction_reference": None
            }).eq("id", contribution["id"]).execute()
            
            print(f"⚠️ Reverted contribution {contribution['id']} to Pending")
            
            # Update global balance (subtract)
            update_global_balance(-contribution['amount'])
    
    except Exception as e:
        print(f"❌ Error handling reversal: {e}")

def update_global_balance(amount):
    """Update global account balance"""
    
    try:
        result = supabase.table("global_account_sync").select("total_balance").execute()
        
        if result.data:
            current_balance = result.data[0]["total_balance"]
            new_balance = current_balance + amount
            
            supabase.table("global_account_sync").update({
                "total_balance": new_balance,
                "last_sync": datetime.now().isoformat()
            }).eq("id", 1).execute()
            
            print(f"💼 Updated global balance: R{current_balance:,.2f} → R{new_balance:,.2f}")
    
    except Exception as e:
        print(f"❌ Failed to update global balance: {e}")

def send_payment_confirmation(user_id, amount, date):
    """Send payment confirmation to member"""
    
    try:
        # Get user details
        result = supabase.table("users").select("username, phone, email").eq("id", user_id).execute()
        
        if result.data:
            user = result.data[0]
            
            message = f"""
✅ Payment Confirmed!

Hi {user['username']},

Your R{amount:.2f} contribution for {date} has been received.

Thank you for supporting Khula Collective! 🚀

Current collective balance will be updated shortly.
            """
            
            print(f"📧 Sending confirmation to {user['username']}")
            # TODO: Integrate with Twilio/Email service
    
    except Exception as e:
        print(f"❌ Failed to send confirmation: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Stitch Webhook Listener",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    # Run webhook listener
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)