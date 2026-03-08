import os
import requests
import time

def upload_to_facebook_reels(video_path: str, caption: str, page_id: str, access_token: str):
    """
    Uploads a video to Facebook Reels using the Meta Graph API.
    """
    if not page_id or not access_token:
        print("[Facebook] Error: Missing Page ID or Access Token.")
        return None

    # Step 1: Initialize the upload
    init_url = f"https://graph.facebook.com/v19.0/{page_id}/video_reels"
    init_params = {
        "upload_phase": "start",
        "access_token": access_token
    }

    try:
        res = requests.post(init_url, params=init_params)
        res.raise_for_status()
        video_id = res.json().get('video_id')
        upload_url = res.json().get('upload_url')

        if not video_id or not upload_url:
            print(f"[Facebook] Initialization failed: {res.text}")
            return None

        print(f"[Facebook] Initialized. Video ID: {video_id}")

        # Step 2: Upload the actual video file
        # Meta expects the binary data in the request body
        with open(video_path, 'rb') as f:
            headers = {
                "Authorization": f"OAuth {access_token}",
                "offset": "0",
                "file_size": str(os.path.getsize(video_path))
            }
            upload_res = requests.post(upload_url, data=f, headers=headers)
            upload_res.raise_for_status()

        print("[Facebook] Upload complete.")

        # Step 3: Publish the Reel
        publish_url = f"https://graph.facebook.com/v19.0/{page_id}/video_reels"
        publish_params = {
            "upload_phase": "finish",
            "video_id": video_id,
            "video_state": "PUBLISHED",
            "description": caption,
            "access_token": access_token
        }
        
        publish_res = requests.post(publish_url, params=publish_params)
        publish_res.raise_for_status()
        
        print(f"[Facebook] Reel published successfully! Result: {publish_res.json()}")
        return video_id

    except Exception as e:
        print(f"[Facebook ERROR] Failed to upload Reel: {e}")
        return None

def upload_to_facebook_video(video_path: str, description: str, page_id: str, access_token: str):
    """
    Uploads a long-form video (non-Reel) to a Facebook Page.
    """
    if not page_id or not access_token:
        print("[Facebook] Error: Missing Page ID or Access Token.")
        return None

    url = f"https://graph.facebook.com/v19.0/{page_id}/videos"
    
    try:
        with open(video_path, 'rb') as f:
            files = {'source': f}
            data = {
                'description': description,
                'access_token': access_token
            }
            res = requests.post(url, files=files, data=data)
            res.raise_for_status()
            
        print(f"[Facebook] Long-form video published! ID: {res.json().get('id')}")
        return res.json().get('id')
    except Exception as e:
        print(f"[Facebook ERROR] Long-form upload failed: {e}")
        return None

    return None
