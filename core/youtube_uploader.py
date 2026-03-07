import os
import glob
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from config import BASE_DIR

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

def _find_client_secret():
    matches = glob.glob(os.path.join(BASE_DIR, "client_secret*.json"))
    return matches[0] if matches else None

def get_authenticated_service():
    credentials = None
    client_secrets_file = _find_client_secret()
    env_token = os.getenv("YOUTUBE_TOKEN_JSON")
    if env_token:
        stripped_token = env_token.strip()
        if (stripped_token.startswith("'") and stripped_token.endswith("'")) or \
           (stripped_token.startswith('"') and stripped_token.endswith('"')):
            stripped_token = stripped_token[1:-1].strip()
        try:
            import json
            token_info = json.loads(stripped_token)
            credentials = Credentials.from_authorized_user_info(token_info, SCOPES)
            print("Authenticated using YOUTUBE_TOKEN_JSON env var.")
        except Exception as e:
            print(f"Error parsing YOUTUBE_TOKEN_JSON: {e}")

    if not credentials and os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        print("Authenticated using local token.json.")
        
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try: credentials.refresh(Request())
            except: credentials = None
        
        if not credentials:
            if not client_secrets_file: return None
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            credentials = flow.run_local_server(port=8080)
            
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def sanitize_text(text):
    if not text: return ""
    return text.replace("<", "").replace(">", "")

def upload_video(youtube, file_path, title, description, tags, privacy_status="private"):
    print(f"Uploading: {title}")
    safe_title = sanitize_text(title)[:100]
    safe_description = sanitize_text(description)[:5000]
    safe_tags = [sanitize_text(t)[:500] for t in (tags or [])]

    body = {
        "snippet": {"title": safe_title, "description": safe_description, "tags": safe_tags, "categoryId": "22"},
        "status": {"privacyStatus": privacy_status, "selfDeclaredMadeForKids": False}
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status: print(f"Uploaded {int(status.progress() * 100)}%")
    return response.get("id")

def find_or_create_playlist(youtube, title, description=""):
    try:
        request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
        response = request.execute()
        for item in response.get("items", []):
            if item["snippet"]["title"] == title: return item["id"]
        create_res = youtube.playlists().insert(
            part="snippet,status",
            body={"snippet": {"title": title, "description": description}, "status": {"privacyStatus": "public"}}
        ).execute()
        return create_res.get("id")
    except: return None

def add_video_to_playlist(youtube, video_id, playlist_id):
    if not playlist_id: return False
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={"snippet": {"playlistId": playlist_id, "resourceId": {"kind": "youtube#video", "videoId": video_id}}}
        ).execute()
        return True
    except: return False
