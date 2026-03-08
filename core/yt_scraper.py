import os
import random
import requests
from config import TEMP_DIR

def download_viral_b_roll(keywords: list, clips_per_keyword: int = 2, progress_callback=None):
    """
    Downloads B-roll for Ashley MindShift from TikTok.
    Focuses on cleaner, darker, cinematic visuals without text overlays.
    """
    downloaded_files = []
    credits = []
    
    def log(msg):
        print(msg)
        if progress_callback: progress_callback(msg)
            
    for i, keyword in enumerate(keywords):
        # Adding "cinematic no text" to get better results
        clean_keyword = f"{keyword} cinematic no text"
        log(f"Searching TikTok for: {clean_keyword}...")
        
        url = "https://tikwm.com/api/feed/search"
        data = {
            "keywords": clean_keyword,
            "count": 15, 
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
                
            random.shuffle(videos)
            selected_videos = videos[:clips_per_keyword]
            
            for j, vid in enumerate(selected_videos):
                play_url = vid.get('play')
                author = vid.get('author', {}).get('nickname', 'Unknown Creator')
                
                if not play_url:
                    continue
                    
                log(f"Downloading clip {j+1}/{clips_per_keyword} for '{keyword}'...")
                
                try:
                    mp4_res = requests.get(play_url, stream=True, timeout=20)
                    mp4_res.raise_for_status()
                    
                    out_path = os.path.join(TEMP_DIR, f'broll_tiktok_{i}_{j}.mp4')
                    with open(out_path, 'wb') as f:
                        for chunk in mp4_res.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.exists(out_path):
                        file_size = os.path.getsize(out_path)
                        if file_size < 100 * 1024:
                            log(f"[TikTok] Rejected small file ({file_size} bytes): {out_path}")
                            if os.path.exists(out_path): os.remove(out_path)
                            continue
                        
                        downloaded_files.append(out_path)
                        if author not in credits:
                            credits.append(f"@{author} (TikTok)")
                except Exception as dl_err:
                    log(f"[TikTok] Download failed: {dl_err}")
                    continue
                        
        except Exception as e:
            log(f"[TikTok ERROR] Failed to fetch {keyword}: {e}")
            
    return downloaded_files, credits
