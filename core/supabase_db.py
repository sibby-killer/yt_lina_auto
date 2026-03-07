import os
from datetime import datetime, timedelta
from config import SUPABASE_URL, SUPABASE_KEY

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
except Exception as e:
    print(f"Warning: Supabase client could not be initialised: {e}")
    supabase = None

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

def cleanup_old_logs(days=3):
    """
    Deletes logs older than X days to save space on Supabase free plan.
    """
    if not supabase: return
    try:
        threshold = (datetime.utcnow() - timedelta(days=days)).isoformat()
        print(f"[DB] Cleaning up logs older than {days} days ({threshold})...")
        
        # We assume the table has a 'created_at' column (default in Supabase)
        result = supabase.table("videos").delete().lt("created_at", threshold).execute()
        
        count = len(result.data) if result.data else 0
        print(f"[DB] Deleted {count} old records.")
    except Exception as e:
        print(f"[DB] Cleanup failed: {e}")
