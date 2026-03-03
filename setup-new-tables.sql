-- ============================================
-- Leap Dashboard - New Tables and RLS Policies
-- Run this in the Supabase SQL Editor
-- ============================================

-- ============================================
-- 1. TODOS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    list_type TEXT NOT NULL CHECK (list_type IN ('day', 'week', 'month')),
    completed BOOLEAN DEFAULT FALSE,
    date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_todos_user_id ON todos(user_id);
CREATE INDEX IF NOT EXISTS idx_todos_list_type ON todos(list_type);
CREATE INDEX IF NOT EXISTS idx_todos_date ON todos(date);

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_todos_updated_at
    BEFORE UPDATE ON todos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 2. EXPENSES TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS expenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    amount NUMERIC(12, 2) NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category);

-- Trigger to update updated_at
CREATE TRIGGER update_expenses_updated_at
    BEFORE UPDATE ON expenses
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 3. RLS POLICIES FOR NEW TABLES
-- ============================================

-- Enable RLS on todos
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

-- Todos policies
CREATE POLICY "Users can view their own todos"
    ON todos FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own todos"
    ON todos FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own todos"
    ON todos FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own todos"
    ON todos FOR DELETE
    USING (auth.uid() = user_id);

-- Enable RLS on expenses
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;

-- Expenses policies
CREATE POLICY "Users can view their own expenses"
    ON expenses FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own expenses"
    ON expenses FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own expenses"
    ON expenses FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own expenses"
    ON expenses FOR DELETE
    USING (auth.uid() = user_id);

-- ============================================
-- 4. RLS POLICIES FOR EXISTING TABLES
-- ============================================

-- Add user_id column to existing tables (if not exists)
-- Note: These will only work if tables exist. Check table names from seed.py.

-- daily_logs
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'daily_logs') THEN
        IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'daily_logs' AND column_name = 'user_id') THEN
            ALTER TABLE daily_logs ADD COLUMN user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;
        END IF;
        ALTER TABLE daily_logs ENABLE ROW LEVEL SECURITY;
        
        DROP POLICY IF EXISTS "Users can view their own daily_logs" ON daily_logs;
        CREATE POLICY "Users can view their own daily_logs" ON daily_logs FOR SELECT USING (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can insert their own daily_logs" ON daily_logs;
        CREATE POLICY "Users can insert their own daily_logs" ON daily_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can update their own daily_logs" ON daily_logs;
        CREATE POLICY "Users can update their own daily_logs" ON daily_logs FOR UPDATE USING (auth.uid() = user_id);
    END IF;
END $$;

-- consistency_streaks
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'consistency_streaks') THEN
        IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'consistency_streaks' AND column_name = 'user_id') THEN
            ALTER TABLE consistency_streaks ADD COLUMN user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;
        END IF;
        ALTER TABLE consistency_streaks ENABLE ROW LEVEL SECURITY;
        
        DROP POLICY IF EXISTS "Users can view their own streaks" ON consistency_streaks;
        CREATE POLICY "Users can view their own streaks" ON consistency_streaks FOR SELECT USING (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can insert their own streaks" ON consistency_streaks;
        CREATE POLICY "Users can insert their own streaks" ON consistency_streaks FOR INSERT WITH CHECK (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can update their own streaks" ON consistency_streaks;
        CREATE POLICY "Users can update their own streaks" ON consistency_streaks FOR UPDATE USING (auth.uid() = user_id);
    END IF;
END $$;

-- portfolio_snapshots
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'portfolio_snapshots') THEN
        IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'portfolio_snapshots' AND column_name = 'user_id') THEN
            ALTER TABLE portfolio_snapshots ADD COLUMN user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;
        END IF;
        ALTER TABLE portfolio_snapshots ENABLE ROW LEVEL SECURITY;
        
        DROP POLICY IF EXISTS "Users can view their own portfolio" ON portfolio_snapshots;
        CREATE POLICY "Users can view their own portfolio" ON portfolio_snapshots FOR SELECT USING (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can insert their own portfolio" ON portfolio_snapshots;
        CREATE POLICY "Users can insert their own portfolio" ON portfolio_snapshots FOR INSERT WITH CHECK (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can update their own portfolio" ON portfolio_snapshots;
        CREATE POLICY "Users can update their own portfolio" ON portfolio_snapshots FOR UPDATE USING (auth.uid() = user_id);
    END IF;
END $$;

-- school_deadlines
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'school_deadlines') THEN
        IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'school_deadlines' AND column_name = 'user_id') THEN
            ALTER TABLE school_deadlines ADD COLUMN user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;
        END IF;
        ALTER TABLE school_deadlines ENABLE ROW LEVEL SECURITY;
        
        DROP POLICY IF EXISTS "Users can view their own deadlines" ON school_deadlines;
        CREATE POLICY "Users can view their own deadlines" ON school_deadlines FOR SELECT USING (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can insert their own deadlines" ON school_deadlines;
        CREATE POLICY "Users can insert their own deadlines" ON school_deadlines FOR INSERT WITH CHECK (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can update their own deadlines" ON school_deadlines;
        CREATE POLICY "Users can update their own deadlines" ON school_deadlines FOR UPDATE USING (auth.uid() = user_id);
    END IF;
END $$;

-- workouts
DO $$
BEGIN
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'workouts') THEN
        IF NOT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'workouts' AND column_name = 'user_id') THEN
            ALTER TABLE workouts ADD COLUMN user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;
        END IF;
        ALTER TABLE workouts ENABLE ROW LEVEL SECURITY;
        
        DROP POLICY IF EXISTS "Users can view their own workouts" ON workouts;
        CREATE POLICY "Users can view their own workouts" ON workouts FOR SELECT USING (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can insert their own workouts" ON workouts;
        CREATE POLICY "Users can insert their own workouts" ON workouts FOR INSERT WITH CHECK (auth.uid() = user_id);
        
        DROP POLICY IF EXISTS "Users can update their own workouts" ON workouts;
        CREATE POLICY "Users can update their own workouts" ON workouts FOR UPDATE USING (auth.uid() = user_id);
    END IF;
END $$;

-- ============================================
-- 5. CREATE AUTH USER TRIGGER (optional)
-- ============================================

-- Optional: Automatically create a default user record when a new auth user signs up
-- Uncomment if needed:

-- CREATE OR REPLACE FUNCTION public.handle_new_user()
-- RETURNS TRIGGER AS $$
-- BEGIN
--     -- You can add any default data initialization here
--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql SECURITY DEFINER;

-- DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
-- CREATE TRIGGER on_auth_user_created
--     AFTER INSERT ON auth.users
--     FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- END OF SETUP SCRIPT
-- ============================================
