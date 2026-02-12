-- Khula Collective Database Schema
-- Investment Club for 20 Members - R300/month commitment

-- Users Table (Extended for FICA Compliance)
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    id_number VARCHAR(13) UNIQUE NOT NULL,
    rica_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    gender VARCHAR(10),
    date_of_birth DATE,
    yearly_target DECIMAL(15, 2) DEFAULT 3600.00,
    constitution_signed BOOLEAN DEFAULT 0,
    constitution_signed_date TIMESTAMP,
    id_document_path TEXT,
    proof_of_residence_path TEXT,
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Monthly Contributions Table
CREATE TABLE IF NOT EXISTS Monthly_Contributions (
    contribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_reference VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Pending',
    verified BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    UNIQUE(user_id, month, year)
);

-- Transactions Table (From Stitch API)
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount DECIMAL(15, 2) NOT NULL,
    description TEXT,
    bank_reference VARCHAR(100),
    transaction_date DATE NOT NULL,
    is_verified BOOLEAN DEFAULT 0,
    allocated BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Investment Goals Table
CREATE TABLE IF NOT EXISTS Investment_Goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    goal_name VARCHAR(200) NOT NULL,
    target_amount DECIMAL(15, 2) NOT NULL,
    current_amount DECIMAL(15, 2) DEFAULT 0,
    target_date DATE,
    investment_type VARCHAR(100),
    risk_level VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Global Account Sync (Total Pot)
CREATE TABLE IF NOT EXISTS GlobalAccountSync (
    sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_balance DECIMAL(15, 2) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- WhatsApp Notifications Log
CREATE TABLE IF NOT EXISTS WhatsApp_Notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message_type VARCHAR(50),
    message_content TEXT,
    sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    twilio_sid VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Investment Suggestions Log
CREATE TABLE IF NOT EXISTS Investment_Suggestions (
    suggestion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_balance DECIMAL(15, 2),
    suggestion_type VARCHAR(100),
    suggested_amount DECIMAL(15, 2),
    expected_return DECIMAL(5, 2),
    risk_level VARCHAR(20),
    suggestion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    implemented BOOLEAN DEFAULT 0
);

-- Admin Actions Log
CREATE TABLE IF NOT EXISTS Admin_Actions (
    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_user_id INTEGER,
    action_type VARCHAR(100),
    action_details TEXT,
    action_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_user_id) REFERENCES Users(user_id)
);

-- Constitution Document
CREATE TABLE IF NOT EXISTS Constitution (
    constitution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    version VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    effective_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_transactions_user ON Transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON Transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_contributions_user ON Monthly_Contributions(user_id);
CREATE INDEX IF NOT EXISTS idx_contributions_date ON Monthly_Contributions(year, month);
CREATE INDEX IF NOT EXISTS idx_users_id_number ON Users(id_number);
CREATE INDEX IF NOT EXISTS idx_users_rica ON Users(rica_number);