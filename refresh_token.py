import os
import google_auth_oauthlib.flow
from config import BASE_DIR

# Requesting full access to YouTube and comments
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

def refresh():
    secret_file = "client_secret.json" # Change this if your file has a different name
    if not os.path.exists(secret_file):
        # Look for glob
        import glob
        matches = glob.glob("client_secret*.json")
        if matches: secret_file = matches[0]
        else:
            print("Error: client_secret.json not found in the current directory.")
            return

    print(f"Starting authentication flow using {secret_file}...")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
    credentials = flow.run_local_server(port=8080)
    
    with open("token.json", 'w') as token:
        token.write(credentials.to_json())
    
    print("\nSUCCESS! token.json has been generated.")
    print("====================================================")
    print("NEW ACTION REQUIRED:")
    print("1. Open token.json")
    print("2. Copy the entire content (the JSON string)")
    print("3. Go to your NEW GitHub Repository Settings -> Secrets and variables -> Actions")
    print("4. Add a repository secret named: YOUTUBE_TOKEN_JSON")
    print("5. Paste the content of token.json there.")
    print("====================================================")

if __name__ == "__main__":
    refresh()
