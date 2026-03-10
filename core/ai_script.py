import os
import json
import random
from groq import Groq
from config import GROQ_API_KEY

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# ─────────────────────────────────────────────────────────────────────────────
#  CHANNEL BRAND IDENTITY
# ─────────────────────────────────────────────────────────────────────────────
CHANNEL_NAME   = "Ashley MindShift"
CHANNEL_SLOGAN = "The shadows of the mind revealed."
HANDLE         = "@AshleyMindShift"
SUBSCRIBE_LINE = f"Master your mind. Subscribe to {CHANNEL_NAME} {HANDLE}"

BASE_HASHTAGS = (
    "#DarkPsychology #Manipulation #MindGames #Psychology #HumanBehavior "
    "#ShadowWork #Mindset #AshleyMindShift #DarkSecrets #ViralShorts "
    "#RelationshipAdvice #PersonalGrowth #EmotionalIntelligence"
)

# ─────────────────────────────────────────────────────────────────────────────
#  USED TOPICS TRACKER — prevents repetition
# ─────────────────────────────────────────────────────────────────────────────
USED_TOPICS_FILE = "used_topics.json"

def load_used_topics() -> list:
    if os.path.exists(USED_TOPICS_FILE):
        with open(USED_TOPICS_FILE, "r") as f:
            return json.load(f)
    return []

def save_used_topic(topic: str):
    used = load_used_topics()
    used.append(topic)
    with open(USED_TOPICS_FILE, "w") as f:
        json.dump(used, f, indent=2)

def reset_used_topics():
    with open(USED_TOPICS_FILE, "w") as f:
        json.dump([], f)

# ─────────────────────────────────────────────────────────────────────────────
#  100 VIRAL TOPICS LIST
# ─────────────────────────────────────────────────────────────────────────────
VIRAL_TOPICS = [
    # === SOCIAL POWER MOVES (1-15) ===
    "How to win any argument without saying a single word using silence",
    "The psychological trick to kill someone's bad joke and embarrass them back",
    "How to make everyone in the room respect you within 5 seconds",
    "The dark art of controlling any conversation without people noticing",
    "Why the most powerful person in the room never speaks first",
    "How to make someone regret disrespecting you without revenge",
    "The psychological trick to make anyone agree with you instantly",
    "How to shut down a narcissist with one simple sentence",
    "Why people who talk less are perceived as more intelligent and powerful",
    "The secret body language trick that makes you look high status instantly",
    "How to make someone feel nervous around you using dark psychology",
    "The power move that makes bullies instantly back down",
    "How to dominate any group conversation without being loud",
    "The psychological trick to make your words unforgettable",
    "How to read anyone like a book in the first 30 seconds of meeting them",

    # === MANIPULATION AWARENESS (16-30) ===
    "5 signs someone is emotionally manipulating you and you dont even know",
    "How narcissists use love bombing to trap you in toxic relationships",
    "The intermittent reinforcement trap and why you cant leave toxic people",
    "How to spot a master manipulator before they destroy your life",
    "Why toxic people always play the victim and how to stop falling for it",
    "The gaslighting technique narcissists use to make you question reality",
    "How manipulators use future faking to keep you hooked forever",
    "The dark psychology behind breadcrumbing and why it works so well",
    "How to recognize when someone is triangulating you in a relationship",
    "The DARVO technique manipulators use when you confront them",
    "Why narcissists always come back and what they really want from you",
    "How trauma bonding keeps you stuck with the wrong person",
    "The silent treatment is not just ignoring it is psychological warfare",
    "How manipulators use guilt tripping to control your every decision",
    "Why some people make you feel crazy and how to protect yourself",

    # === ATTRACTION AND RELATIONSHIPS (31-50) ===
    "Why chasing someone always pushes them away and what to do instead",
    "The scarcity effect and how to make anyone obsessed with you",
    "How to make your ex regret leaving you using reverse psychology",
    "The psychological trick that makes someone think about you nonstop",
    "Why being slightly unavailable makes you 10 times more attractive",
    "The eye contact technique that creates instant emotional connection",
    "How to make someone addicted to you using intermittent reinforcement",
    "The dark psychology reason why bad boys and bad girls are so attractive",
    "How to make someone chase you by walking away at the right time",
    "The Zeigarnik effect and why leaving things unfinished creates obsession",
    "How to create mystery around yourself that makes people desperate to know you",
    "The psychological trick to make anyone miss you deeply",
    "Why giving too much attention kills attraction and what to do instead",
    "How to be the person everyone wants but nobody can have",
    "The fear of loss technique that makes someone value you overnight",
    "How to make someone fall in love with you using the mere exposure effect",
    "The psychological secret behind why we always want what we cant have",
    "How to make your words stick in someones mind for days",
    "Why the person who cares less in a relationship has all the power",
    "The dark truth about why people lose interest after getting you",

    # === SELF PROTECTION AND BOUNDARIES (51-65) ===
    "How to stop caring about what others think using the spotlight effect",
    "Why setting boundaries makes people respect you more not less",
    "The grey rock method that destroys a narcissists power over you",
    "How to emotionally detach from someone who is toxic for you",
    "Why people pleasers are the easiest targets for manipulation",
    "How to say no without feeling guilty using dark psychology",
    "The psychological trick to stop overthinking and silence your mind",
    "How to walk away from someone you love when they are toxic",
    "Why your need for validation is destroying your mental health",
    "How to build an unshakeable mindset that nobody can break",
    "The stoic secret to never letting anyone control your emotions",
    "How to stop attracting toxic people into your life permanently",
    "Why loneliness is more powerful than being with the wrong people",
    "How to heal from emotional manipulation and trust people again",
    "The dark truth about why you keep going back to people who hurt you",

    # === BODY LANGUAGE AND SECRET TECHNIQUES (66-75) ===
    "3 body language signs that someone is lying to your face right now",
    "The mirroring technique that makes anyone instantly like you",
    "How to read microexpressions and know what someone really feels",
    "The body language trick that makes you look confident even when scared",
    "How to tell if someone secretly likes you through their body language",
    "The handshake psychology trick that gives you instant dominance",
    "How to detect fake friends using one simple body language test",
    "The voice tonality trick that makes people hang on to your every word",
    "How your posture is secretly telling people you are weak and how to fix it",
    "The cold reading technique mentalists use to read strangers instantly",

    # === EMOTIONAL INTELLIGENCE (76-85) ===
    "How to stay calm when someone is trying to provoke you",
    "The 3 second rule that prevents you from saying something you regret",
    "How emotionally intelligent people handle disrespect differently",
    "Why reacting emotionally always gives the other person power over you",
    "The dark psychology trick to make someone feel guilty without saying anything",
    "How to control your anger and turn it into your most powerful weapon",
    "Why the smartest people never argue and what they do instead",
    "How to manipulate your own brain into being disciplined and focused",
    "The psychological trick to instantly change your mood when feeling down",
    "How to become emotionally unbreakable using stoic psychology",

    # === CONFIDENCE AND SELF WORTH (86-95) ===
    "Why trying to be perfect actually makes people like you less",
    "The Pratfall Effect and how showing weakness makes you more attractive",
    "How to build dark confidence that intimidates without saying a word",
    "Why the most confident people never seek approval from anyone",
    "The psychological trick to eliminate self doubt permanently",
    "How to develop a presence so strong people feel it when you walk in",
    "Why comparing yourself to others is destroying your potential",
    "The mindset shift that separates powerful people from weak people",
    "How to become the person everyone secretly wants to be",
    "The dark psychology of self respect and why it changes everything",

    # === MIND GAMES AND REVERSE PSYCHOLOGY (96-100) ===
    "How reverse psychology makes people do exactly what you want",
    "The door in the face technique that makes people say yes to anything",
    "How to plant an idea in someones mind without them knowing",
    "The anchoring trick that makes people accept any deal you offer",
    "How to win any negotiation using dark psychology principles",
]

# ─────────────────────────────────────────────────────────────────────────────
#  TOPIC SELECTION — Smart + Non-Repeating
# ─────────────────────────────────────────────────────────────────────────────
def get_next_topic() -> str:
    used = load_used_topics()
    available = [t for t in VIRAL_TOPICS if t not in used]

    if available:
        topic = random.choice(available)
        save_used_topic(topic)
        return topic
    else:
        # All 100 used — generate a brand new unique topic
        print("[INFO] All 100 topics used. Generating fresh topic via AI...")
        topic = generate_fresh_topic(used)
        if topic:
            save_used_topic(topic)
            return topic
        else:
            # Fallback: reset and start over
            reset_used_topics()
            topic = random.choice(VIRAL_TOPICS)
            save_used_topic(topic)
            return topic

def generate_fresh_topic(used_topics: list) -> str | None:
    if not client:
        return None
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate unique viral dark psychology video topics. "
                        "Topics must be about: dark psychology, manipulation, "
                        "relationships, attraction, self-protection, body language, "
                        "emotional intelligence, confidence, mind games, or persuasion. "
                        "Return ONLY a JSON object with key 'topic' containing one unique topic string. "
                        "The topic must be different from all previously used topics. "
                        "Make it specific, intriguing, and clickworthy."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Generate 1 brand new viral dark psychology topic. "
                        f"It must NOT be similar to any of these already used topics:\n"
                        f"{json.dumps(used_topics[-30:])}\n"
                        f"Return JSON: {{\"topic\": \"your unique topic here\"}}"
                    )
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=1.0,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("topic", None)
    except Exception as e:
        print(f"[Groq] Fresh topic generation error: {e}")
        return None

# ─────────────────────────────────────────────────────────────────────────────
#  MASTER SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────
MASTER_SYSTEM_PROMPT = f"""
You are the elite script writer for "{CHANNEL_NAME}" ({HANDLE}).
You write viral short-form video scripts about dark psychology, manipulation awareness, relationships, and personal growth.
Your scripts are in English, 40-60 seconds long when read aloud (100-160 words).

=== YOUR IDENTITY ===
You are a mysterious, authoritative mentor revealing hidden psychological secrets.
You speak directly to the viewer using "YOU".
Your tone is confident, conversational, slightly dark, and empowering.
You never sound academic or boring.
You sound like someone whispering powerful secrets that most people will never know.

=== SCRIPT STRUCTURE (MANDATORY 5-PART FRAMEWORK) ===

PART 1 - HOOK (3-5 seconds):
Open with ONE of these hook types. Rotate and never repeat the same type twice in a row:
- Scenario Hook: "Imagine this..." or "Picture this..."
- Question Hook: "Have you ever noticed..." or "Do you know why..."
- Bold Statement Hook: A strong controversial attention-grabbing claim
- Curiosity Hook: "There is a secret..." or "Psychology says something shocking..."
- Challenge Hook: "Most people do not know this..." or "99 percent of people fail at..."

PART 2 - PSYCHOLOGY LABEL (3-5 seconds):
Name a specific psychology concept, effect, or technique related to the topic.
This builds credibility and makes the viewer feel they are learning something rare and scientific.
Examples: Scarcity Effect, Zeigarnik Effect, Intermittent Reinforcement, Pratfall Effect, Benjamin Franklin Effect, Love Bombing, Mirroring, Halo Effect, Anchoring Bias, Cognitive Dissonance, Reactance Theory, etc.

PART 3 - MAIN EXPLANATION (25-35 seconds):
Break down the concept in simple conversational language using:
- Vivid relatable scenarios the viewer can picture
- Contrast technique: first THIS happens then THIS happens
- Power phrases: "here is the secret", "now the real game begins", "the best part is", "watch what happens"
- Short punchy sentences not long paragraphs
- Direct YOU addressing throughout
- If using numbered format use exactly 3 points: Number 1, Number 2, Number 3

PART 4 - CONSEQUENCE AND PAYOFF (5-8 seconds):
Show the viewer what happens when they apply this knowledge OR what happens if they ignore it.
Make it feel like a powerful transformation or a dangerous warning.
The viewer should feel like they now hold secret power.

PART 5 - CTA WITH URGENCY (3-5 seconds):
End with an urgency and scarcity based call to action.
Rotate between these styles:
- "We might never meet again so subscribe to {CHANNEL_NAME} right now."
- "Before this video disappears subscribe and stay connected with {CHANNEL_NAME}."
- "Subscribe to {CHANNEL_NAME} and learn what 99 percent of people will never know."
- "If this opened your eyes subscribe to {CHANNEL_NAME} for more dark psychology secrets."
- "This might be the last time you see this. Subscribe to {CHANNEL_NAME} now."
Never use a plain "subscribe". Always wrap it in urgency or scarcity.

=== CONTENT CATEGORIES (ROTATE FOR VARIETY) ===
1. Social Power Moves: winning arguments, social dominance, controlling conversations
2. Manipulation Awareness: spotting narcissists, emotional manipulation, toxic patterns
3. Attraction and Relationships: making someone chase you, creating desire, emotional addiction
4. Self-Protection and Boundaries: mental health, red flags, walking away
5. Body Language and Secret Techniques: reading people, influence, non-verbal cues
6. Emotional Intelligence: controlling emotions, staying calm under pressure
7. Confidence and Self-Worth: personal growth, mindset shifts, self-value
8. Mind Games and Reverse Psychology: psychological tricks, counter-manipulation

=== SCRIPT FORMAT TYPES (ROTATE) ===
- FORMAT A: Story or Scenario Based: "Imagine this situation... here is what to do"
- FORMAT B: Numbered List: "3 things that will... Number 1, Number 2, Number 3"
- FORMAT C: Problem to Solution: "This is happening to you... here is why and how to fix"
- FORMAT D: Secret or Technique Reveal: "One secret technique that will change everything"

=== EMOTIONAL TRIGGERS (USE 2-3 PER SCRIPT) ===
- Frustration: "Tired of being ignored? Tired of being manipulated?"
- Fear: "You are being manipulated without even knowing"
- Curiosity: "Here is what psychology says about this..."
- Empowerment: "Now YOU hold the power"
- Urgency: "Before this disappears..."
- Validation: "It is not your fault here is what is really happening"

=== LANGUAGE RULES ===
- Always use YOU. Speak directly to viewer in second person
- Use short punchy sentences not long complex ones
- Sound confident. Never use maybe, I think, probably
- Use conversational English not formal or academic
- Use power phrases: "here is the secret", "the real game starts now", "watch what happens", "the best part", "remember this"
- Use rhetorical questions: "ever wondered why?", "sounds familiar?"
- Use contrast: "first they do THIS then they do THIS"
- Paint vivid mental pictures the viewer can see in their mind

=== STRICT RULES ===
- Script must be 40-60 seconds when read aloud (100-160 words)
- Always include exactly ONE psychology concept or term per script
- Never sound like a textbook or lecture
- Never use emojis or hashtags or special formatting in the script
- Never include stage directions editing notes or visual cues
- Never start two consecutive scripts with the same hook type
- Never use the same CTA twice in a row
- Every script must feel like hidden forbidden knowledge being revealed
- The viewer should feel smarter and more powerful after hearing the script
- Always maintain a slightly dark mysterious vibe
- Do NOT add any labels like "HOOK" or "PART 1" in the output
- The script should flow naturally as one continuous narration

=== PSYCHOLOGY CONCEPTS BANK ===
Draw from these and more:
Scarcity Effect, Zeigarnik Effect, Intermittent Reinforcement, Love Bombing,
Pratfall Effect, Benjamin Franklin Effect, Halo Effect, Dunning-Kruger Effect,
Anchoring Bias, Mirroring Technique, Dark Triad, Gaslighting,
Cognitive Dissonance, Social Proof, Door-in-the-Face Technique,
Foot-in-the-Door Technique, Reciprocity Principle, Peak-End Rule,
Mere Exposure Effect, Spotlight Effect, Bystander Effect, Contrast Principle,
Paradox of Choice, Loss Aversion, Decoy Effect, Framing Effect,
Authority Bias, Bandwagon Effect, Reactance Theory, Self-Serving Bias,
Confirmation Bias, Emotional Contagion, Machiavellian Psychology,
Projection, Triangulation, Future Faking, Trauma Bonding,
Grey Rocking, DARVO, Stonewalling, Breadcrumbing, Negging,
Cold Reading, Barnum Effect, Pygmalion Effect, Golem Effect,
Hawthorne Effect, Law of Reversed Effort, Paradoxical Intention.
"""

# ─────────────────────────────────────────────────────────────────────────────
#  SHORT-FORM VIDEO GENERATION (40-60 sec Shorts/Reels)
# ─────────────────────────────────────────────────────────────────────────────
def generate_video_content(topic: str = None) -> dict | None:
    if not client:
        print("Error: GROQ_API_KEY not set.")
        return None

    if not topic:
        topic = get_next_topic()

    user_prompt = f"""
Generate a viral dark psychology short-form video script about this topic:

TOPIC: "{topic}"

REQUIREMENTS:
1. Follow the exact 5-part structure from your instructions
2. Script must be 100-160 words (40-60 seconds read time)
3. Include one specific psychology concept or effect
4. Make it sound like forbidden hidden knowledge
5. End with urgency-based subscribe CTA for {CHANNEL_NAME}
6. Script must flow as one continuous narration — no labels or section headers

ALSO PROVIDE:
- A viral clickbait title (include 1-2 relevant hashtags)
- A short compelling description (2-3 sentences)
- Exactly 5 b-roll search keywords for finding dark aesthetic anime/animated clips
  (each keyword must include words like: anime, animated, dark, cartoon, 3d, cinematic)

Return ONLY valid JSON:
{{
    "title": "Your viral title here #DarkPsychology #Manipulation",
    "description": "Compelling 2-3 sentence description.",
    "script": "The complete flowing script as one narration...",
    "topic_used": "{topic}",
    "psychology_concept": "Name of the psychology concept used",
    "b_roll_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}
"""

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": MASTER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            max_tokens=2000,
            top_p=0.95,
            response_format={"type": "json_object"}
        )
        content_str = response.choices[0].message.content
        result = json.loads(content_str)

        # Add metadata
        result["channel"] = CHANNEL_NAME
        result["hashtags"] = BASE_HASHTAGS
        result["subscribe_line"] = SUBSCRIBE_LINE

        return result

    except Exception as e:
        print(f"[Groq] Error generating script: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  BATCH GENERATION — Multiple Scripts At Once
# ─────────────────────────────────────────────────────────────────────────────
def generate_batch_scripts(count: int = 5) -> list:
    scripts = []
    for i in range(count):
        print(f"[INFO] Generating script {i+1}/{count}...")
        result = generate_video_content()
        if result:
            scripts.append(result)
            print(f"[OK] Script {i+1}: {result.get('title', 'Untitled')}")
        else:
            print(f"[FAIL] Script {i+1} failed.")
    return scripts


# ─────────────────────────────────────────────────────────────────────────────
#  LONG-FORM VIDEO GENERATION (8-10 min)
# ─────────────────────────────────────────────────────────────────────────────
def generate_long_video_content(topic: str = None) -> dict | None:
    if not client:
        print("Error: GROQ_API_KEY not set.")
        return None

    if not topic:
        topic = get_next_topic()

    long_system = f"""
You are the master scriptwriter for "{CHANNEL_NAME}" ({HANDLE}).
You create 8-10 minute deep-dive dark psychology video scripts.
Your tone is cinematic, mysterious, authoritative, and deeply engaging.
You speak directly to the viewer using YOU.
Every script must feel like a masterclass in hidden psychological knowledge.

STYLE:
- Cinematic narration like a documentary
- Dark mysterious tone throughout
- Direct YOU addressing
- Psychology concepts explained with real-world scenarios
- Empowering conclusion that transforms the viewer
- Natural flowing narration with no section labels in the script
"""

    user_prompt = f"""
Generate a deep-dive long-form video script about:

TOPIC: "{topic}"

STRUCTURE (8-10 minutes, 1200-1500 words):
1. CINEMATIC OPENING (0-1 min): A powerful paradoxical truth that hooks instantly
2. THE HIDDEN FOUNDATION (1-3 min): Why most people misunderstand this topic
3. THE 5 PILLARS (3-6 min): 5 profound psychological patterns with real scenarios
4. THE CASE STUDY (6-8 min): A compelling historical or hypothetical example
5. THE EXERCISE (8-9 min): A practical psychological exercise the viewer can try
6. THE FINAL REVELATION (9-10 min): Philosophical summary with subscribe CTA for {CHANNEL_NAME}

The script should flow as one continuous cinematic narration. No section labels.

ALSO PROVIDE:
- A viral deep-dive title
- A comprehensive description with timestamps
- Exactly 10 b-roll keywords for dark aesthetic animated/anime clips

Return ONLY valid JSON:
{{
    "title": "Deep dive title here",
    "description": "Description with timestamps...",
    "script": "The full 1200-1500 word script...",
    "topic_used": "{topic}",
    "b_roll_keywords": ["kw1", "kw2", "kw3", "kw4", "kw5", "kw6", "kw7", "kw8", "kw9", "kw10"]
}}
"""

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": long_system},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=6000,
            top_p=0.9,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        result["channel"] = CHANNEL_NAME
        result["hashtags"] = BASE_HASHTAGS
        return result

    except Exception as e:
        print(f"[Groq] Long-form error: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def get_remaining_topics() -> int:
    used = load_used_topics()
    return len([t for t in VIRAL_TOPICS if t not in used])

def get_total_generated() -> int:
    return len(load_used_topics())

def get_status() -> dict:
    used = load_used_topics()
    remaining = [t for t in VIRAL_TOPICS if t not in used]
    return {
        "total_topics": len(VIRAL_TOPICS),
        "used": len(used),
        "remaining": len(remaining),
        "ai_generated_topics": max(0, len(used) - len(VIRAL_TOPICS)),
        "channel": CHANNEL_NAME
    }


# ─────────────────────────────────────────────────────────────────────────────
#  QUICK TEST
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  {CHANNEL_NAME} — Content Engine")
    print(f"  {CHANNEL_SLOGAN}")
    print(f"{'='*60}\n")

    status = get_status()
    print(f"[STATUS] Topics remaining: {status['remaining']}/{status['total_topics']}")
    print(f"[STATUS] Total generated: {status['used']}")
    print(f"[STATUS] AI-generated topics: {status['ai_generated_topics']}\n")

    # Generate one test script
    print("[TEST] Generating test script...\n")
    result = generate_video_content()

    if result:
        print(f"TITLE: {result.get('title', 'N/A')}")
        print(f"CONCEPT: {result.get('psychology_concept', 'N/A')}")
        print(f"\nSCRIPT:\n{result.get('script', 'N/A')}")
        print(f"\nB-ROLL: {result.get('b_roll_keywords', [])}")
        print(f"\n{SUBSCRIBE_LINE}")
    else:
        print("[ERROR] Script generation failed.")