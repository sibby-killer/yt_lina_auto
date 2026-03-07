import os
import random
import requests
from config import TEMP_DIR

def download_viral_b_roll(keywords: list, clips_per_keyword: int = 2, progress_callback=None):
    """
    Downloads B-roll for Ashley MindShift.
    Focuses on cleaner, darker, cinematic visuals without text overlays.
    """
    downloaded_files = []
    credits = []
    
    def log(msg):
        print(msg)
        if progress_callback: progress_callback(msg)
            
    for i, keyword in enumerate(keywords):
        # Removing "satisfying" to avoid text-heavy videos and adding "cinematic"
        clean_keyword = f"{keyword} cinematic no text"
        log(f"Searching TikTok for: {clean_keyword}...")
        
        url = "https://tikwm.com/api/feed/search"
        data = {
            "keywords": clean_keyword,
            "count": 15, # Fetch more to have a better chance of finding good ones
            "cursor": 0
        }
        
        try:
            res = requests.post(url, data=data, timeout=15)
            res.raise_for_status()
            json_data = res.json()
            
            videos = json_data.get('data', {}).get('videos', [])
            if not videos:
                log(f"[TikTok] No videos found for {keyword}")
                continue
                
            # Randomize to get fresh content
            random.shuffle(videos)
            selected_videos = videos[:clips_per_keyword]
            
            for j, vid in enumerate(selected_videos):
                play_url = vid.get('play')
                author = vid.get('author', {}).get('nickname', 'Unknown Creator')
                
                if not play_url:
                    continue
                    
                log(f"Downloading clip {j+1}/{clips_per_keyword} for '{keyword}'...")
                
                # Stream the MP4 to disk
                mp4_res = requests.get(play_url, stream=True, timeout=20)
                mp4_res.raise_for_status()
                
                out_path = os.path.join(TEMP_DIR, f'broll_tiktok_{i}_{j}.mp4')
                with open(out_path, 'wb') as f:
                    for chunk in mp4_res.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                if os.path.exists(out_path):
                    downloaded_files.append(out_path)
                    if author not in credits:
                        credits.append(f"@{author} (TikTok)")
                        
        except Exception as e:
            log(f"[TikTok ERROR] Failed to fetch {keyword}: {e}")
            
    return downloaded_files, credits
