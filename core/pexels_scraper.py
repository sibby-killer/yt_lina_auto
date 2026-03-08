import os
import requests
import random
from config import PEXELS_API_KEY, TEMP_DIR

def download_pexels_b_roll(keywords: list, clips_per_keyword: int = 3, progress_callback=None):
    """
    Downloads landscape (16:9) B-roll from Pexels for long-form videos.
    """
    if not PEXELS_API_KEY:
        print("[Pexels] Error: PEXELS_API_KEY not set.")
        return [], []

    downloaded_files = []
    credits = []
    
    headers = {"Authorization": PEXELS_API_KEY}
    
    def log(msg):
        print(msg)
        if progress_callback: progress_callback(msg)

    for i, keyword in enumerate(keywords):
        log(f"Searching Pexels for: {keyword}...")
        
        # Search for videos
        url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=15&orientation=landscape&size=medium"
        
        try:
            res = requests.get(url, headers=headers, timeout=15)
            res.raise_for_status()
            data = res.json()
            
            videos = data.get('videos', [])
            if not videos:
                log(f"[Pexels] No videos found for {keyword}")
                continue
                
            random.shuffle(videos)
            selected_videos = videos[:clips_per_keyword]
            
            for j, vid in enumerate(selected_videos):
                # Get the best quality file (usually link under video_files)
                video_files = vid.get('video_files', [])
                if not video_files:
                    continue
                
                # Filter for Full HD if possible, otherwise first one
                # video_files are usually ordered by quality or have 'width'
                play_url = None
                for vf in video_files:
                    if vf.get('width') == 1920 or vf.get('quality') == 'hd':
                        play_url = vf.get('link')
                        break
                
                if not play_url:
                    play_url = video_files[0].get('link')
                
                author = vid.get('user', {}).get('name', 'Unknown Creator')
                
                log(f"Downloading Pexels clip {j+1}/{clips_per_keyword} for '{keyword}'...")
                
                try:
                    mp4_res = requests.get(play_url, stream=True, timeout=30)
                    mp4_res.raise_for_status()
                    
                    out_path = os.path.join(TEMP_DIR, f'broll_pexels_{i}_{j}.mp4')
                    with open(out_path, 'wb') as f:
                        for chunk in mp4_res.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.exists(out_path) and os.path.getsize(out_path) > 500 * 1024: # 500KB min for longform
                        downloaded_files.append(out_path)
                        if author not in credits:
                            credits.append(f"{author} (Pexels)")
                    else:
                        if os.path.exists(out_path): os.remove(out_path)
                except Exception as dl_err:
                    log(f"[Pexels] Clip download failed: {dl_err}")
                    continue
                    
        except Exception as e:
            log(f"[Pexels ERROR] Failed to fetch {keyword}: {e}")
            
    return downloaded_files, credits
