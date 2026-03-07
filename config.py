import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# API Keys
GROQ_API_KEY      = os.getenv("GROQ_API_KEY")
PEXELS_API_KEY    = os.getenv("PEXELS_API_KEY")
YOUTUBE_PLAYLIST_ID = os.getenv("YOUTUBE_PLAYLIST_ID")

# Supabase
SUPABASE_URL      = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY      = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Reddit
REDDIT_CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT    = "IndigoInsights/1.0"

# Flask
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "indigo-insights-secret-2026")

# Folders
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR   = os.path.join(BASE_DIR, "temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
