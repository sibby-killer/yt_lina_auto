import os
from config import SUPABASE_URL, SUPABASE_KEY

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
except Exception as e:
    print(f"Warning: Supabase client could not be initialised: {e}")
    supabase = None

VIDEOS_TABLE = "videos_v2" # Using a separate table or suffix for V2 if desired, but default is 'videos'

def log_video(title, topic, script, local_path, description="", tags=None, status="generated"):
    if not supabase: return None
    record = {
        "title": title, "topic": topic, "script": script, "local_path": local_path,
        "description": description, "tags": tags or [], "status": status
    }
    try:
        result = supabase.table("videos").insert(record).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"[DB] Insert failed: {e}")
    return None

def update_video_upload(record_id, youtube_id):
    if not supabase: return False
    try:
        supabase.table("videos").update({
            "status": "uploaded", "youtube_id": youtube_id, "youtube_url": f"https://youtu.be/{youtube_id}"
        }).eq("id", record_id).execute()
        return True
    except Exception as e:
        print(f"[DB] Update failed: {e}")
        return False
