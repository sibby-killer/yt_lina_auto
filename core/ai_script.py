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


def generate_video_content(topic: str = "how to read anyone instantly") -> dict | None:
    """
    Uses Groq Llama-3 to generate high-intensity "Psycholo Secrets" style scripts.
    formula: 15s Hook/Build-up -> 60-70s 3-Step Trick Breakdown -> 10s Scarcity CTA.
    Total Duration: 80-90 seconds.
    """
    if not client:
        print("Error: GROQ_API_KEY not set.")
        return None

    prompt = f"""
You are the lead storyteller for "{CHANNEL_NAME}".
Your style is inspired by "Psycholo Secrets" - fast, high-energy, authoritative, and forbidden.
Atmosphere: Dark, enigmatic, addictive.

=== CONTENT STRUCTURE: THE PSYCHOLO FORMULA ===
1. THE VIRAL HOOK (0-2s): A shocking claim.
   Example: "Three psychological tricks that make anyone obsessed with you."
2. THE DESIRE / BRIDGE (2-7s): Ask a direct, emotional question.
   Example: "Want to know how to make someone think about you constantly? How to become the person they can't stop obsessing over?"
3. THE REALITY CHECK (7-14s): Call out common mistakes.
   Example: "Most people try too hard. They text too much. They're always available. They chase."
4. THE CLIMAX SHIFT (14-21s): The "Secret" pivot.
   Example: "But if you're already following Ashley MindShift's secrets, you know obsession isn't created by being present. It's created by being unpredictable. And I'm about to show you exactly how. Watch this."
5. THE 3-TRICK BREAKDOWN (21s - 75s):
   - For each trick: Name it, explain EXACTLY what to do, then explain the "Why" (The Biological/Psychological Addiction).
   - Trick 1: Give attention, then withdraw it. (Explain brain addiction to attention highs).
   - Trick 2: Be mysterious. (Explain mystery creates curiosity/obsession).
   - Trick 3: The Prize/Competition. (Explain humans want what others want).

6. THE FINAL LESSON & CTA (75s - 90s):
   - Recap the secret: "Obsession isn't created by being perfect. It's created by being unpredictable."
   - SCARCITY CTA: "Follow Ashley MindShift secrets now. And learn the dark psychology that makes people addicted to you. If you leave now, you might never find this frequency again."

=== SEO TITLE RULES ===
- Intense, curious, and professional.
- MUST INCLUDE 2 to 3 random hashtags from this pool: #DarkPsychology, #ShadowWork, #Manipulation, #MindMastery, #PsychologySecrets, #HumanBehavior, #ForbiddenKnowledge, #Viral, #Shorts.
- EXAMPLE: "3 Tricks to Make Anyone Obsessed #DarkPsychology #MindMastery #Viral"

=== VISUAL B-ROLL KEYWORDS (ANIME/CARTOON ONLY) ===
- Deliver EXACTLY 5 search keywords.
- Must be: DARK ANIME ANIMATION, CINEMATIC CARTOON, CREEPY ILLUSTRATION, STYLIZED GRAPHICS.
- NO REAL FOOTAGE. NO TEXT ON SCREEN. 
- Example keywords: "Dark anime boy with glowing eyes cinematic no text", "Creepy stylized cartoon character lurking in shadows", "Noir anime city rain high contrast", "Stylized brain mapping psychological animation", "Dark anime girl looking mysterious and cold".

=== OUTPUT ===
Return ONLY valid JSON:
{{
    "title": "Intense Viral Title (e.g. 3 Tricks to Control Anyone followed by hashtags)",
    "description": "Short, bullet-point breakdown of the tricks.",
    "script": "The full spoken script (Spoken words only). Use pauses as ...",
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

if __name__ == "__main__":
    test = generate_video_content("How to make someone obsessed with you")
    if test:
        print(json.dumps(test, indent=2))
