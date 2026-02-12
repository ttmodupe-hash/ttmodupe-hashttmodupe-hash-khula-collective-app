-- Reviews Table for Member Feedback
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS member_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username VARCHAR(100),
    full_name VARCHAR(200),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON member_reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON member_reviews(created_at DESC);

-- Enable Row Level Security
ALTER TABLE member_reviews ENABLE ROW LEVEL SECURITY;

-- Policy: Members can insert their own reviews
CREATE POLICY "Members can insert own reviews" ON member_reviews
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

-- Policy: Members can view their own reviews
CREATE POLICY "Members can view own reviews" ON member_reviews
    FOR SELECT USING (auth.uid()::text = user_id::text);

-- Policy: Admin can view all reviews
CREATE POLICY "Admin can view all reviews" ON member_reviews
    FOR SELECT USING (EXISTS (
        SELECT 1 FROM users WHERE id = auth.uid()::integer AND is_admin = 1
    ));

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Member Reviews table created successfully!';
END $$;