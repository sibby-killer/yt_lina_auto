-- Run this in the Supabase SQL Editor to create the necessary table

CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT now(),
    title TEXT,
    topic TEXT,
    script TEXT,
    local_path TEXT,
    description TEXT,
    tags TEXT[],
    status TEXT DEFAULT 'generated',
    youtube_id TEXT,
    youtube_url TEXT
);

-- Enable RLS and create policies if needed
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;

-- Allow service role full access (Internal for the bot)
CREATE POLICY "Full access for service role" ON videos
    FOR ALL
    USING (true)
    WITH CHECK (true);
