-- Khula Collective Supabase Database Schema
-- Run this in Supabase SQL Editor to create all tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    sa_id_number VARCHAR(13),
    role VARCHAR(20) DEFAULT 'member',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Monthly Contributions Table
CREATE TABLE IF NOT EXISTS monthly_contributions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    month VARCHAR(7) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    payment_date DATE,
    transaction_reference VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Global Account Sync Table
CREATE TABLE IF NOT EXISTS global_account_sync (
    id SERIAL PRIMARY KEY,
    total_balance DECIMAL(15, 2) DEFAULT 0,
    last_sync TIMESTAMP,
    fnb_account_id VARCHAR(100)
);

-- Investment Goals Table
CREATE TABLE IF NOT EXISTS investment_goals (
    id SERIAL PRIMARY KEY,
    current_month VARCHAR(7),
    monthly_target DECIMAL(10, 2),
    monthly_collected DECIMAL(10, 2),
    yearly_target DECIMAL(15, 2),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Votes Table
CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    suggestion_id INTEGER,
    vote_type VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, suggestion_id)
);

-- Investment Suggestions Table
CREATE TABLE IF NOT EXISTS investment_suggestions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    expected_return DECIMAL(10, 2),
    risk_level VARCHAR(20),
    priority VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Hall of Fame Table (for monthly archives)
CREATE TABLE IF NOT EXISTS hall_of_fame (
    id SERIAL PRIMARY KEY,
    month VARCHAR(7) NOT NULL,
    rank INTEGER NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    username VARCHAR(50),
    full_name VARCHAR(100),
    amount DECIMAL(10, 2),
    medal VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Market Data Table
CREATE TABLE IF NOT EXISTS market_data (
    id SERIAL PRIMARY KEY,
    repo_rate DECIMAL(5, 2),
    prime_rate DECIMAL(5, 2),
    inflation_rate DECIMAL(5, 2),
    jse_all_share DECIMAL(10, 2),
    usd_zar_rate DECIMAL(6, 2),
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Member Signatures Table (FICA Compliance)
CREATE TABLE IF NOT EXISTS member_signatures (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    signature_name VARCHAR(100),
    signed_at TIMESTAMP DEFAULT NOW(),
    ip_address VARCHAR(50),
    constitution_version VARCHAR(20)
);

-- Audit Log Table (for admin actions)
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100),
    details TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_contributions_user_month ON monthly_contributions(user_id, month);
CREATE INDEX IF NOT EXISTS idx_contributions_status ON monthly_contributions(status);
CREATE INDEX IF NOT EXISTS idx_votes_user_suggestion ON votes(user_id, suggestion_id);
CREATE INDEX IF NOT EXISTS idx_hall_of_fame_month ON hall_of_fame(month);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- Create views for common queries
CREATE OR REPLACE VIEW member_summary AS
SELECT 
    u.id,
    u.username,
    u.full_name,
    COUNT(mc.id) as total_contributions,
    SUM(CASE WHEN mc.status = 'Received' THEN mc.amount ELSE 0 END) as total_paid,
    SUM(CASE WHEN mc.status = 'Pending' THEN mc.amount ELSE 0 END) as total_pending
FROM users u
LEFT JOIN monthly_contributions mc ON u.id = mc.user_id
WHERE u.role = 'member' AND u.is_active = TRUE
GROUP BY u.id, u.username, u.full_name;

-- Create view for monthly statistics
CREATE OR REPLACE VIEW monthly_stats AS
SELECT 
    month,
    COUNT(DISTINCT user_id) as active_members,
    SUM(CASE WHEN status = 'Received' THEN amount ELSE 0 END) as collected,
    SUM(CASE WHEN status = 'Pending' THEN amount ELSE 0 END) as pending,
    COUNT(CASE WHEN status = 'Received' THEN 1 END) as paid_count,
    COUNT(CASE WHEN status = 'Pending' THEN 1 END) as pending_count
FROM monthly_contributions
GROUP BY month
ORDER BY month DESC;

-- Insert initial global account sync record
INSERT INTO global_account_sync (id, total_balance, last_sync)
VALUES (1, 0, NOW())
ON CONFLICT (id) DO NOTHING;

-- Insert initial investment goals record
INSERT INTO investment_goals (id, current_month, monthly_target, monthly_collected, yearly_target)
VALUES (1, TO_CHAR(NOW(), 'YYYY-MM'), 6000, 0, 72000)
ON CONFLICT (id) DO NOTHING;

-- Insert initial market data
INSERT INTO market_data (id, repo_rate, prime_rate, inflation_rate, jse_all_share, usd_zar_rate)
VALUES (1, 8.25, 11.75, 5.2, 78500, 18.50)
ON CONFLICT (id) DO NOTHING;

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE monthly_contributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE votes ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_signatures ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for users (members can only see their own data)
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text OR role = 'admin');

CREATE POLICY "Members can view own contributions" ON monthly_contributions
    FOR SELECT USING (auth.uid()::text = user_id::text OR EXISTS (
        SELECT 1 FROM users WHERE id = auth.uid()::integer AND role = 'admin'
    ));

-- Create RLS policies for votes (members can only vote once per suggestion)
CREATE POLICY "Members can view all votes" ON votes
    FOR SELECT USING (true);

CREATE POLICY "Members can insert own votes" ON votes
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- Grant permissions to authenticated users
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- Create function to update last_sync timestamp
CREATE OR REPLACE FUNCTION update_last_sync()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE global_account_sync SET last_sync = NOW() WHERE id = 1;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to auto-update last_sync
CREATE TRIGGER update_sync_timestamp
AFTER INSERT OR UPDATE ON monthly_contributions
FOR EACH ROW
EXECUTE FUNCTION update_last_sync();

-- Create function to calculate global balance
CREATE OR REPLACE FUNCTION calculate_global_balance()
RETURNS DECIMAL AS $$
DECLARE
    total DECIMAL;
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO total
    FROM monthly_contributions
    WHERE status = 'Received';
    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Khula Collective database schema created successfully!';
    RAISE NOTICE '📊 Tables created: 10';
    RAISE NOTICE '🔍 Views created: 2';
    RAISE NOTICE '🔒 RLS policies enabled';
    RAISE NOTICE '⚡ Triggers configured';
END $$;