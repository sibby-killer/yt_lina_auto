import os
import json
from groq import Groq
from config import GROQ_API_KEY

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# ─────────────────────────────────────────────────────────────────────────────
#  CHANNEL BRAND IDENTITY: ASHLEY MINDSHIFT (The Dark & Deep Edition)
# ─────────────────────────────────────────────────────────────────────────────
CHANNEL_NAME   = "Ashley MindShift"
CHANNEL_SLOGAN = "The shadows of the mind revealed."
Channel_URL = "http://www.youtube.com/@AshleyMindShift"
HANDLE = "@AshleyMindShift"
SUBSCRIBE_LINE = f"Master your mind. Subscribe to {CHANNEL_NAME} {HANDLE}"

# Dark, mysterious hashtag pool
BASE_HASHTAGS = (
    "#DarkPsychology #Manifestation #Mindshift #Psychology #HumanBehavior "
    "#ShadowWork #Mysteries #DarkAesthetic #Mindset #AshleyMindShift #ViralShorts"
)


def generate_video_content(topic: str = "how to read anyone instantly") -> dict | None:
    """
    Uses Groq Llama-3 to generate high-intensity Dark Psychology scripts.
    formula: 5s Hook -> 35s Deep Solution/Breakdown -> 10s Scarcity CTA.
    """
    if not client:
        print("Error: GROQ_API_KEY not set.")
        return None

    prompt = f"""
You are the lead storyteller for the YouTube channel "{CHANNEL_NAME}".
Slogan: "{CHANNEL_SLOGAN}"
Atmosphere: Dark, eerie, and psychological.
Goal: Provide a COMPLETE, broken-down solution to a psychological mystery or manipulation trick.

Target: 50-60s Shorts.

=== SCRIPT FORMULA: THE DEEP SOLUTION ===
1. THE SHOCKING HOOK (0-5s): A slow, heavy claim that locks the viewer in.
   Example: "There is a reason you feel watched in an empty room... and today, you will learn how to own that fear."
2. THE FULL BREAKDOWN (6-45s): Do not cut it short. Provide a step-by-step breakdown of the solution or method.
   Explain the "Why", then the "How". Use short, punchy sentences. 
   Focus on the biological or psychological reality.
3. THE SCARCITY CTA (46-60s): Deliver a powerful, psychological nudge.
   EXACT TEXT STYLE: "If you haven't subscribed to {CHANNEL_NAME} yet, this might be the last time you ever see us... Our secrets are for the masters, not the followers. Subscribe now, or remain in the shadows forever."

=== SEO TITLE RULES ===
- Intense, curious, and professional.
- EXAMPLE: "The True Solution to Reading Anyone's Mind #DarkPsychology #Mastery #Secrets"

=== DESCRIPTION RULES ===
- Break down the FACTS in bullet points.
- Create a sense of "Exclusive Knowledge".
- {SUBSCRIBE_LINE}
- {BASE_HASHTAGS}

=== VISUAL B-ROLL KEYWORDS ===
- Provide EXACTLY 4 keywords. 
- Must be: DARK, WEIRD, CREATURES, ANIME GIRLS (Dark aesthetic), NO TEXT.
- Example: "Dark eerie creature in shadows cinematic no text", "Cyberpunk blue eyes girl no captions", "Weird biological organism moving slowly dark background".

=== OUTPUT ===
Return ONLY valid JSON:
{{
    "title": "string",
    "description": "string",
    "script": "string (spoken words only — use ... for atmospheric pauses)",
    "b_roll_keywords": ["string", "string", "string", "string"]
}}
"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.75,
            max_tokens=2048,
            response_format={"type": "json_object"}
        )
        content_str = response.choices[0].message.content
        return json.loads(content_str)

    except Exception as e:
        print(f"Error generating script: {e}")
        return None

if __name__ == "__main__":
    test = generate_video_content("How to gain absolute control in a room")
    print(json.dumps(test, indent=2))
