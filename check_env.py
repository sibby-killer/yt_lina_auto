import os
from dotenv import load_dotenv

print("--- ENV DIAGNOSTIC ---")
print(f"Current Dir: {os.getcwd()}")
print(f".env exists: {os.path.exists('.env')}")

load_dotenv()

# We check for key prefix to avoid leaking the secret in logs
key = os.getenv("GROQ_API_KEY")
if key:
    print(f"GROQ_API_KEY Found! Length: {len(key)}")
    print(f"Prefix: {key[:5]}...")
else:
    print("GROQ_API_KEY NOT FOUND in environment or .env file.")

# Check for other keys
print(f"PEXELS_API_KEY Found: {bool(os.getenv('PEXELS_API_KEY'))}")
print(f"SUPABASE_URL Found: {bool(os.getenv('NEXT_PUBLIC_SUPABASE_URL'))}")
