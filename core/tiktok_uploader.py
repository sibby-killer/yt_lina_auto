import os
import json
import time

def upload_to_tiktok(video_path: str, description: str, cookies_path: str):
    """
    Uploads a video to TikTok using a headless browser and exported cookies.
    """
    if not os.path.exists(cookies_path):
        print(f"[TikTok] Error: Cookies file not found at {cookies_path}")
        return False

    try:
        from tiktok_uploader.upload import upload_video
        
        # TikTok Uploader uses the library to handle browsers
        # It's better than writing a raw Playwright script for the user to manage
        print(f"[TikTok] Attempting upload for: {os.path.basename(video_path)}")
        
        success = upload_video(
            video_path,
            description=description,
            cookies=cookies_path,
            browser='chrome', # Assumes user has chrome installed
            headless=True
        )
        
        if success:
            print("[TikTok] Video uploaded successfully through headless browser.")
            return True
        else:
            print("[TikTok] Upload failed (check cookies or browser logs).")
            return False

    except ImportError:
        print("[TikTok] Error: 'tiktok-uploader' library not installed.")
        return False
    except Exception as e:
        print(f"[TikTok ERROR] Failed to upload: {e}")
        return False

    return False
