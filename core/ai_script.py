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
You are the elite lead strategist and storyteller for "{CHANNEL_NAME}". 
Your style is professional, high-status, and enigmatic—inspired by the most viral "Dark Psychology" channels like Psycholo Secrets.

TARGET TOPIC: "{topic}"

=== CORE DIRECTIVE: UNPARALLELED UNIQUENESS ===
- NEVER reuse "Attention Withdrawal", "Mystery", or "Prize/Competition" as tricks unless the topic EXPLICITLY calls for them.
- For EVERY topic, you must BRAINSTORM 3 completely original, specific psychological patterns or 'tricks' that actually relate to the '{topic}'.
- If the topic is 'Why you feel watched', the tricks must be about spatial awareness, the limbic system, or peripheral vision—NOT about making people obsessed.
- Be creative. Research (simulate) unique psychological theories for each script.

=== CONTENT STRUCTURE: THE ASHLEY MINDSHIFT FORMULA ===
1. THE VIRAL HOOK (0-2s): A shocking or paradoxical claim specific to "{topic}".
2. THE DESIRE / BRIDGE (2-7s): Ask an emotional, status-driven question that hooks the viewer's ego.
3. THE HIDDEN REALITY (7-14s): Call out why traditional advice on this topic fails.
4. THE FREQUENCY SHIFT (14-21s): The "Shadow" pivot. "But if you're on this frequency, you know the truth is much darker..."
5. THE 3-TRICK BREAKDOWN (21s - 75s): 
   - Invent 3 FRESH, topic-specific 'Dark Secrets' or 'Psychological Methods'.
   - For each: Name it (e.g., "The Void Reflection", "The Gaze Anchor"), explain the technique, and the psychological 'Why'.
   - These MUST be different for Every. Single. Script.
6. THE FINAL REVELATION & SCARCITY CTA (75s - 90s):
   - A philosophical closing thought. 
   - "Follow Ashley MindShift now to stay ahead of the curve. Leave now, and you might lose this transmission forever."

=== SEO TITLE RULES ===
- High-status, mysterious, and viral. 
- Include 2-3 random hashtags: #DarkPsychology #ShadowWork #HumanBehavior #MindMastery #Viral #PsychologySecrets.

=== VISUAL B-ROLL KEYWORDS (ANIME/CARTOON ONLY) ===
- EXACTLY 5 search keywords. 
- Style: DARK NOIR ANIME, CINEMATIC DARK CARTOON, CREEPY MINIMALIST ILLUSTRATION.
- No real humans. No text.

=== OUTPUT ===
Return ONLY valid JSON:
{{
    "title": "Topic-Specific Viral Title with Hashtags",
    "description": "Unique breakdown of the 3 specific tricks.",
    "script": "Professional, intense spoken script. Use '...' for dramatic pauses.",
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
You are the master strategist and storyteller of "{CHANNEL_NAME}". 
Your mission is to produce a profound, high-status, cinematic deep-dive masterpiece about: "{topic}"

=== CORE DIRECTIVE: UNIQUE MASTERY ===
- This is NOT a Short. You must explore the deep philosophy and dark psychology of "{topic}".
- DO NOT use generic tricks (Mystery, Attention). 
- Imagine you are a mixture of a psychologist and a noir philosopher.
- Every insight must be specifically discovered for this topic.

=== LONG-FORM STRUCTURE (8-10 Minutes) ===
1. THE CINEMATIC OPENING (0-1 min): Hook the viewer with a paradox or a "forbidden" truth about "{topic}".
2. THE ARCHITECTURE OF THE SHADOW (1-3 min): Explain the hidden psychological foundation. Why does this exist?
3. THE 5 PILLARS OF MASTERY (3-6 min): Provide 5 specific, intense psychological patterns.
   - For each: Name it, give a detailed technical explanation, and a "Dark Context" example.
   - These MUST be profound and fresh. No surface-level advice.
4. THE MASTER CLASS CASE STUDY (6-8 min): Describe a hypothetical or historical example of this logic in action.
5. THE SHADOW WORK EXERCISE (8-9 min): Give the viewer a specific psychological exercise to practice.
6. THE FINAL REVELATION (9-10 min): A powerful, philosophical summary that leaves the viewer feeling enlightened yet unsettled.

=== SEO & VISUALS ===
- Title: Viral, high-status, and profoundly curious.
- B-Roll Keywords: Exactly 10 keywords. Style: DARK NOIR ANIME or CINEMATIC SCIFI ANIMATION. No text. No real humans.
- Script: Extensive, descriptive, and atmospheric (Approx 1500 words). Use "..." for pauses.

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
