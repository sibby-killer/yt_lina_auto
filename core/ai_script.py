import os
import json
from groq import Groq
from config import GROQ_API_KEY

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# ─────────────────────────────────────────────────────────────────────────────
#  CHANNEL BRAND IDENTITY: ASHLEY MINDSHIFT (Psycholo Secrets Pivot)
# ─────────────────────────────────────────────────────────────────────────────
CHANNEL_NAME   = "Ashley MindShift"
CHANNEL_SLOGAN = "The shadows of the mind revealed."
HANDLE         = "@AshleyMindShift"
SUBSCRIBE_LINE = f"Master your mind. Subscribe to {CHANNEL_NAME} {HANDLE}"

# Dark, mysterious hashtag pool
BASE_HASHTAGS = (
    "#DarkPsychology #Manifestation #Mindshift #Psychology #HumanBehavior "
    "#ShadowWork #Mysteries #DarkAesthetic #Mindset #AshleyMindShift #ViralShorts"
)


def generate_video_content(topic: str) -> dict | None:
    """
    Uses Groq Llama-3 to generate high-intensity "Psycholo Secrets" style scripts.
    formula: 15s Hook/Build-up -> 60-70s 3-Step Trick Breakdown -> 10s Scarcity CTA.
    Total Duration: 80-90 seconds.
    """
    if not client:
        print("Error: GROQ_API_KEY not set.")
        return None

    prompt = f"""
You are the master elite strategist for "{CHANNEL_NAME}". 
Vision: High-status, enigmatic, dark psychology deep-dives.

TARGET TOPIC: "{topic}"

=== VISUAL BRAND IDENTITY: CRITICAL ===
- ONLY 2D/3D ANIMATION. NO REAL LIFE CLIPS. NO REAL HUMANS. 
- Style: DARK NOIR ANIME, CINEMATIC DARK CARTOON, EERIE MINIMALIST ILLUSTRATION.
- NO CAPTIONS OR TEXT on source clips.

=== CONTENT STRUCTURE ===
1. THE VIRAL HOOK (0-2s): Paradoxical claim about "{topic}".
2. THE DESIRE (2-7s): Emotional bridge.
3. THE HIDDEN REALITY (7-14s): Why traditional advice fails.
4. THE FREQUENCY SHIFT (14-21s): The "Shadow" pivot.
5. THE 3-TRICK BREAKDOWN (21s - 75s): 
   - 3 FRESH, topic-specific 'Dark Secrets'. 
   - Name them (e.g., "The Void Reflection"), explain technique & 'Why'.
6. THE FINAL REVELATION & SCARCITY CTA (75s - 90s):
   - "Follow Ashley MindShift now. Leave now, and you might lose this transmission."

=== VISUAL B-ROLL KEYWORDS (ANIME ONLY) ===
- Deliver EXACTLY 5 search keywords specifically for TIKTOK search.
- Keywords MUST include adjectives like: anime, animated, cartoon, drawing, sketch.
- Example: "dark anime girl eyes", "animated brain mapping", "shadow figure drawing".

=== OUTPUT ===
Return ONLY valid JSON:
{{
    "title": "Topic-Specific Viral Title with Hashtags",
    "description": "Unique breakdown of the 3 specific tricks.",
    "script": "Professional script (90s). Use '...' for pauses.",
    "b_roll_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}
"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )
        content_str = response.choices[0].message.content
        return json.loads(content_str)

    except Exception as e:
        print(f"[Groq] Error generating script: {e}")
        return None

def generate_long_video_content(topic: str) -> dict | None:
    """
    Generates 8-10 minute long-form content (approx 1200-1500 words).
    Formula: Introduction -> The Core Mystery -> 5-7 Deep Insights -> Case Study -> Practical Exercise -> Conclusion.
    """
    if not client:
        return None

    prompt = f"""
You are the master lead strategist for "{CHANNEL_NAME}". 
Objective: Create a profound, high-status, cinematic deep-dive masterpiece (8-10 Min).

TARGET TOPIC: "{topic}"

=== VISUAL BRAND IDENTITY: CRITICAL ===
- ONLY 2D/3D ANIMATION, CINEMATIC CGI, OR STYLIZED ART.
- NO REAL WORLD CLIPS. NO REAL HUMANS.
- Style: DARK NOIR ANIME or CINEMATIC SCIFI ANIMATION.

=== LONG-FORM STRUCTURE ===
1. THE CINEMATIC OPENING (0-1 min): Paradoxical truth.
2. THE ARCHITECTURE OF THE SHADOW (1-3 min): Hidden foundation.
3. THE 5 PILLARS OF MASTERY (3-6 min): 5 profound patterns.
4. THE MASTER CLASS CASE STUDY (6-8 min): Historical/hypothetical example.
5. THE SHADOW WORK EXERCISE (8-9 min): Psychological exercise.
6. THE FINAL REVELATION (9-10 min): Philosophical summary.

=== VISUAL B-ROLL KEYWORDS (ANIME ONLY) ===
- Deliver EXACTLY 10 search keywords specifically for PEXELS search.
- Keywords MUST include adjectives like: anime, animated, cartoon, cgi, 3d render.
- Example: "noir anime city dark rain", "3d render of human soul glowing", "dark animated library".

=== OUTPUT ===
Return ONLY valid JSON:
{{
    "title": "Topic-Specific Deep-Dive Title",
    "description": "Comprehensive video description with timestamps.",
    "script": "The full 1500 word script...",
    "b_roll_keywords": ["keyword1", ..., "keyword10"]
}}
"""
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.75,
            max_tokens=6000,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"[Groq] Long-form error: {e}")
        return None
