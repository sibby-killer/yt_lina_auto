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
#  MODELS — Primary + Fallback
# ─────────────────────────────────────────────────────────────────────────────
PRIMARY_MODEL  = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-70b-versatile"

# ─────────────────────────────────────────────────────────────────────────────
#  CHANNEL BRAND IDENTITY
# ─────────────────────────────────────────────────────────────────────────────
CHANNEL_NAME   = "Ashley MindShift"
CHANNEL_SLOGAN = "The shadows of the mind revealed."
HANDLE         = "@AshleyMindShift"
SUBSCRIBE_LINE = f"Control your mind before they control you. Join {CHANNEL_NAME} {HANDLE}"

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
    # === ELITE MINDSET & POWER DYNAMICS ===
    "The 1 percent rule that keeps the elite in power while you struggle",
    "How to use dark psychology to make anyone instantly respect you",
    "The harsh truth about why some people always get what they want",
    "How to outsmart a manipulator by playing their own game better",
    "The banned negotiation tactic that forces people to say yes",
    "Why being too nice is the exact reason you are losing in life",
    "How to read a room instantly like a billionaire CEO",
    "The secret body language trick that makes you look high status",
    "How to manipulate the manipulator and take back your power",
    "Why the most powerful person in the room never speaks first",
    "The psychological trick to make people desperate for your attention",
    "How to make someone regret disrespecting you without saying a word",
    "The exact dark psychology tactic used by the top 1 percent",
    "Why your empathy is being weaponized against you",
    "The Machiavellian secret to dominating any social situation"
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

    messages = [
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
    ]

    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            response = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=1.0,
                max_tokens=200,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("topic", None)
        except Exception as e:
            print(f"[Groq] Fresh topic error on {model}: {e}. Trying next...")

    print("[Groq] Both models failed for fresh topic generation.")
    return None

# ─────────────────────────────────────────────────────────────────────────────
#  MASTER SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────
MASTER_SYSTEM_PROMPT = f"""
You are the elite script writer for "{CHANNEL_NAME}" ({HANDLE}).
You write viral short-form video scripts about dark psychology, elite mindset, power dynamics, and personal growth.
Your scripts are in English, strictly under 45 seconds when read aloud (MAXIMUM 85 WORDS).

=== YOUR IDENTITY ===
You are a mysterious, authoritative mentor revealing hidden psychological secrets.
You speak directly to the viewer using "YOU".
Your tone is confident, conversational, slightly dark, and empowering.

=== SCRIPT STRUCTURE (MANDATORY 5-PART FRAMEWORK) ===

PART 1 - HOOK (3 seconds):
Short, punchy, aggressive hook. Max 1-2 short sentences.
- "If you want to absolutely dominate any room..."
- "Here is a toxic trick to make someone obsessed..."
- "How to instantly read anyone's true intentions..."

PART 2 & 3 - THE CORE MANIPULATION (25 seconds):
This is the CORE of the script. Explain the concept fast and hard.
- State the name of the law or trick.
- Give a fast, vivid scenario. "First, do this... then pull back..."
- Use "... " for dramatic pauses.
- Max 3-5 punchy sentences. Make it dark, factual, and undeniable.

PART 4 & 5 - THE AWAKENING & URGENT CTA (10 seconds):
Give them power. "You've seen this happen before."
End with a purely manipulative or urgent Call to Action. NEVER say "Subscribe/Follow".
- "Save this video before it's deleted."
- "Share this with someone who is being played."
- "Watch this again to master the game."

=== 3 VIRAL REFERENCE SCRIPTS TO MIMIC ===
Emulate the pacing, dark tone, and concise structure of these exactly.

REFERENCE 1:
"If you want to absolutely dominate any room you walk into... use the Law of Withholding. Never give away everything on the first interaction. The less you speak, the more powerful you seem. When they ask a question... pause for three seconds before answering. This creates an unbearable silence that forces them to seek your validation. Sounds familiar, right? Now you have the advantage. Save this video before it's deleted."

REFERENCE 2:
"Here's a toxic trick to make someone obsessed with you... it's called Intermittent Reinforcement. First, you bombard them with attention and affection... make them feel like they are the center of your universe. Then... suddenly pull back without any explanation. Their brain will flood with anxiety, chasing that initial high you gave them. They become literally addicted to your validation. Use this cautiously. Share this with someone who is currently being played."

REFERENCE 3:
"How to instantly read anyone's true intentions... watch their feet. People can fake a smile, but they cannot control their feet. If you're talking to someone and their feet are pointed towards the door... they are desperately trying to escape the conversation. But if their feet point directly at you... they are submissively locked in. You've seen this happen before. Now you know the truth. Watch this again to master the game."

=== CRITICAL RULES ===
1. MAXIMUM 85 WORDS. We need this under 50 seconds.
2. Direct YOU addressing throughout.
3. No academic textbook filler. Get straight to the manipulation/power-move.

=== ACCURACY RULE ===
The psychology concept you mention MUST be genuinely and accurately connected to the topic.
If you are unsure whether a concept fits do NOT use it.
Instead describe the psychological mechanism in plain everyday language.
Wrong psychology terms destroy credibility instantly.
Viewers who know psychology will call out incorrect usage.
Every psychology fact you state must be accurate and verifiable.

=== DEPTH RULE ===
Surface level advice is BANNED. Examples of banned surface advice:
- "Make eye contact"
- "Be confident"
- "They avoid eye contact when lying"
- "Stand up straight"
- "Smile more"
These are too basic. Everyone knows these.
Every piece of advice must have a deeper PSYCHOLOGICAL WHY behind it.
The viewer should learn something they have NEVER heard before on any other channel.
If a tip sounds like it could come from a basic Google search or a generic self-help article it is NOT good enough. Go deeper.

=== FRESHNESS RULE ===
Do not give the same generic advice that every other dark psychology channel gives.
Find unique angles, surprising insights, and counterintuitive truths.
Make the viewer think "I never knew that" or "I never thought about it that way."
The script should feel like insider knowledge that is not freely available everywhere.

=== STRICT OUTPUT RULES ===
- Script must be strictly under 50 seconds when read aloud (110-140 words)
- Always include exactly ONE psychology concept or term per script
- Never sound like a textbook or lecture
- Never use emojis hashtags or special formatting inside the script text
- Never include stage directions editing notes or visual cues in the script
- Do NOT add labels like HOOK or PART 1 or SECTION in the output
- The script must flow naturally as one continuous spoken narration
- Every script must feel like hidden forbidden knowledge being revealed
- Always maintain a slightly dark mysterious vibe throughout
- Use "..." for pauses throughout the script for natural rhythm
- The script should be ready to read aloud for voiceover with no modifications needed

=== PSYCHOLOGY CONCEPTS BANK ===
Draw from these concepts and more. Always match the concept to the topic accurately:
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
Cognitive Load Theory, Micro Expressions, Duping Delight, Baseline Behavior,
Hawthorne Effect, Law of Reversed Effort, Paradoxical Intention,
Stockholm Syndrome, Learned Helplessness, Sunk Cost Fallacy,
Ben Franklin Effect, Contrast Effect, Serial Position Effect,
Negativity Bias, Availability Heuristic, Status Quo Bias.

=== GOLD STANDARD EXAMPLE ===
This is exactly the quality and style every script should match:

"Do you know that 91 percent of people lie on a regular basis... and most of them get away with it? Not anymore. Psychology calls these micro expressions... tiny involuntary signals your body leaks when the brain is fabricating a lie. And here are three signs to catch them every single time.

Number 1... watch their eyes. When someone looks up and to the right while answering your question... their brain is not remembering... it is inventing a fake image right in front of you.

Number 2... notice the timing. If you ask a direct question and they pause... or repeat your question back to you... understand their brain is buying time to craft a believable story.

Number 3... the body never agrees with a lie. They will say no I did not do it... but their head will give a tiny nod yes. They will touch their face... cross their arms... or suddenly break eye contact. The subconscious simply cannot hide the truth.

Once you master these three signs... no lie will ever slip past you again. You will read people like an open book.

Comment the word CODE and I will send you the elite blueprint."

Study this example. Notice:
- Conversational tone throughout
- "..." pauses for natural rhythm
- Each point has the SIGN plus WHY it happens psychologically
- Accurate psychology concept (micro expressions for lying)
- Relatable scenarios
- Empowerment at the end
- Engagement hack CTA (Comment CODE)
Every script you generate must match this quality level.

=== PINNED COMMENT GENERATION ===
For every script you generate, also create a unique pinned comment for that specific video.
The pinned comment must:
1. Be directly related to the specific topic of that video
2. Ask a thought-provoking question that makes viewers want to reply
3. Feel like the creator genuinely engaging with the audience
4. Be 1-3 sentences maximum
5. Use a conversational casual tone with personality
6. Include 1-2 relevant emojis maximum (not excessive)
7. Make viewers feel their opinion matters
8. Create debate or discussion potential
9. NEVER mention links, bio, masterclass, courses, or products
10. NEVER be the same generic comment for every video

GOOD COMMENT EXAMPLES:
- For a lying detection video: "Be honest... have you ever caught someone lying using body language and they had NO idea you knew? 👀 Drop your story below"
- For a manipulation video: "What is the most manipulative thing someone has ever done to you? I will go first... 🧠"
- For an attraction video: "Real talk... have you ever used any of these psychology tricks without even knowing it? 😏"
- For a confidence video: "What is the ONE thing that instantly kills your confidence? Let us talk about it 👇"
- For a narcissist video: "Have you ever dealt with a narcissist? What was the moment you finally realized what was happening? 🤔"

BAD COMMENT EXAMPLES (DO NOT DO THIS):
- "Which psychological trick do you think is the MOST dangerous?" (too generic, same for every video)
- "Follow us for more!" (promotional, no engagement value)
- "Check the link in bio!" (no link exists, sounds spammy)
- "Like and subscribe!" (generic, low effort)

The comment must make someone think "I actually want to answer this" not "this is obviously a bot comment."

=== DESCRIPTION GENERATION (SHORTS) ===
Generate a YouTube Shorts description that is SEO-optimized and professional.

SHORT DESCRIPTION FORMAT:
Line 1: [Powerful hook sentence about the topic] 🧠
Line 2: [What the viewer will learn — naturally include 2-3 SEO keywords]
[Empty line]
Line 3: [Engagement question specific to the topic — ask viewers to comment]
[Empty line]
🚨 They don't want you to know this. 
👁️ Follow to master the game they are playing on you.
[Empty line]
{{CREDITS_PLACEHOLDER}}
[Empty line]
[10-15 relevant hashtags]

SEO KEYWORDS TO NATURALLY INCLUDE (pick 3-5 relevant ones per video):
dark psychology, psychology tricks, manipulation tactics, mind games,
body language secrets, human behavior, relationship psychology,
emotional intelligence, mental strength, narcissist traits,
psychological tricks, how to read people, dark psychology facts,
psychology of attraction, self improvement, personal growth,
stoic mindset, confidence psychology, social skills, influence tactics

DO NOT include in descriptions:
- External links of any kind
- "Link in bio" or "Link in description"
- Masterclass or course or product references
- Affiliate links or promotions
- Fake credits or made-up creator names
- The {{CREDITS_PLACEHOLDER}} must appear EXACTLY as written — the code will replace it later

CRITICAL FORMATTING RULE: The description MUST use actual newline characters (\n) to create line breaks.
Every section must start on a new line. Never put everything on one line separated by commas or periods.
Use proper paragraph spacing with empty lines between sections.
Example correct format (using \n):
"Hook sentence about the topic 🧠\nWhat the viewer will learn with SEO keywords\n\nEngagement question for viewers? 👇\n\n🚨 They don't want you to know this. \n👁️ Follow to master the game they are playing on you.\n\n{{CREDITS_PLACEHOLDER}}\n\n#DarkPsychology #Hashtag2 #Hashtag3"
"""

# ─────────────────────────────────────────────────────────────────────────────
#  SHORT-FORM VIDEO GENERATION (1 min 20 sec to 1 min 50 sec Shorts/Reels)
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

CRITICAL REQUIREMENTS:
1. Follow the exact 5-part structure from your system instructions
2. Script MUST be MAXIMUM 85 WORDS (strictly under 45 seconds read time)
3. Include one specific psychology concept that ACCURATELY relates to the topic
4. Make it sound like forbidden hidden knowledge being whispered at midnight
5. End with an urgent manipulative CTA (e.g. "Save this before it's deleted"). NEVER say "Subscribe", "Follow", or "{CHANNEL_NAME}".
6. Script must flow as one continuous natural narration with no labels or headers
7. Every point must include THE SIGN plus WHY it happens psychologically plus WHAT IT REVEALS
8. Use "..." for natural pauses throughout
9. Voice must sound like a real human dictating a real secret, not an AI list

ALSO PROVIDE:
- A hyper-short, clickbait title of STRICTLY 1 to 3 WORDS MAX (e.g., "LIMIT YOUR AVAILABILITY", "SPOT A LIAR"). No hashtags in the title string.
- A SEO-optimized description following the SHORT FORMAT in your system instructions (must include {{CREDITS_PLACEHOLDER}} exactly where credits go)
- A unique pinned comment for this specific video topic
- Exactly 5 b-roll search keywords for finding dark aesthetic anime or animated clips
  (each keyword must include words like: anime, animated, dark, cartoon, 3d, cinematic, noir)

Return ONLY valid JSON:
{{
    "title": "1 TO 3 WORDS MAX",
    "description": "SEO-optimized short description following the SHORT FORMAT with {{CREDITS_PLACEHOLDER}} included #DarkPsychology #Manipulation",
    "script": "The complete flowing natural script with ... pauses throughout...",
    "topic_used": "{topic}",
    "psychology_concept": "Name of the psychology concept used",
    "pinned_comment": "A unique engaging question or conversation starter specific to this video topic",
    "b_roll_keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}}
"""

    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": MASTER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                model=model,
                temperature=0.85,
                max_tokens=3000,
                top_p=0.90,
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
            print(f"[Groq] Short-form error on {model}: {e}. Trying next...")

    print("[Groq] Both models failed for short-form generation.")
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
You speak directly to the viewer using YOU throughout the entire script.
Every script must feel like a masterclass in hidden psychological knowledge.

=== CRITICAL LENGTH REQUIREMENT ===
The script MUST be between 1500 and 2000 words. This is NON-NEGOTIABLE.
A script under 1500 words is a FAILURE. Do NOT generate anything shorter.
8 minutes of narration requires approximately 1500-1600 words minimum.
10 minutes of narration requires approximately 1800-2000 words.
AIM for 1800 words. This is the sweet spot.

COUNT YOUR WORDS. If your script is under 1500 words, you have failed the task.

=== SECTION-BY-SECTION MINIMUM WORD COUNTS ===
Each section must meet its MINIMUM word count:

SECTION 1 - CINEMATIC OPENING (0:00 to 1:00) — MINIMUM 150 words
- Open with a powerful paradoxical truth or a gripping scenario
- Paint a vivid picture that hooks the viewer instantly
- Introduce the topic with mystery and intrigue
- End with a transition that makes the viewer NEED to keep watching
- Use "..." pauses for dramatic rhythm

SECTION 2 - THE HIDDEN FOUNDATION (1:00 to 3:00) — MINIMUM 300 words
- Explain why most people fundamentally misunderstand this topic
- Reveal the hidden psychological foundation that nobody talks about
- Use real-world relatable examples and scenarios
- Challenge common beliefs and conventional wisdom
- Name and explain the core psychology concept with depth
- Make the viewer feel like they have been seeing the world wrong this whole time

SECTION 3 - THE 5 PILLARS (3:00 to 6:00) — MINIMUM 500 words
- Present 5 profound psychological patterns, insights, or techniques
- Each pillar must have: THE CONCEPT plus A RELATABLE SCENARIO plus THE PSYCHOLOGICAL WHY plus HOW TO APPLY IT
- Each pillar should be 80-120 words minimum
- Use conversational transitions between pillars not robotic numbering
- Include surprising counterintuitive insights not generic advice
- Paint vivid mental pictures for each pillar
- Make each pillar feel like a separate revelation

SECTION 4 - THE CASE STUDY (6:00 to 8:00) — MINIMUM 300 words
- Present a compelling historical example OR a detailed hypothetical scenario
- Walk through the scenario step by step showing how the psychology principles apply
- Make it feel like a story not a lecture
- Include dialogue or inner thoughts of the characters
- Show cause and effect clearly
- Connect the case study back to the 5 pillars

SECTION 5 - THE PRACTICAL EXERCISE (8:00 to 9:00) — MINIMUM 150 words
- Give the viewer a specific psychological exercise they can try today
- Explain exactly how to do it step by step
- Explain what they will notice when they do it
- Make it feel actionable and empowering
- Connect it to the concepts discussed earlier

SECTION 6 - THE FINAL REVELATION (9:00 to 10:00) — MINIMUM 150 words
- Deliver a powerful philosophical summary
- Tie everything together into one profound insight
- Make the viewer feel transformed and empowered
- End with an emotional urgency-based subscribe CTA for {CHANNEL_NAME}
- Leave the viewer thinking about this video long after it ends

=== STYLE RULES ===
- Cinematic narration like a documentary or film noir voiceover
- Dark mysterious tone throughout the entire script
- Direct YOU addressing in every section
- Psychology concepts explained with vivid real-world scenarios not textbook definitions
- Use "..." for natural pauses and dramatic rhythm throughout
- Sound like a real human narrating not an AI generating text
- Empowering conclusion that makes the viewer feel they have gained secret knowledge
- Natural flowing narration with NO section labels or headers in the script
- The script should read as one continuous flowing piece ready for voiceover
- Every insight must have the psychological WHY behind it
- Deep insights not surface-level generic advice
- Accurate psychology concepts only. Never use a concept that does not fit the topic
- If a point sounds like basic Google search advice it is not good enough. Go deeper.
- Include personal connection moments: "You have experienced this..." or "Think about it..."
- Use power phrases: "Here is what nobody tells you...", "And this is where everything changes...", "Now pay attention because this is the part that matters most..."

=== WHAT TO AVOID ===
- DO NOT write less than 1500 words under any circumstances
- DO NOT rush through sections
- DO NOT use generic surface-level advice
- DO NOT sound like a textbook or academic paper
- DO NOT use robotic transitions
- DO NOT include section labels or headers in the script output
- DO NOT use emojis or hashtags in the script body
- DO NOT use incorrect psychology concepts
- DO NOT write a script that could be delivered in under 8 minutes

=== PINNED COMMENT GENERATION ===
For this video also generate a unique pinned comment.
The comment must:
1. Be directly related to the specific topic of this video
2. Ask a thought-provoking question that makes viewers want to reply
3. Feel like the creator genuinely engaging with the audience
4. Be 1-3 sentences maximum
5. Conversational tone with 1-2 relevant emojis
6. Create debate or discussion potential
7. NEVER mention links, bio, masterclass, courses, or products

=== DESCRIPTION GENERATION (LONG-FORM) ===
Generate a professional comprehensive YouTube description that is SEO-optimized.

LONG DESCRIPTION FORMAT:
[Powerful hook — what this video reveals] 🧠
[2-3 sentence overview with naturally included SEO keywords]

⏱️ TIMESTAMPS:
0:00 — [Compelling opening section title]
1:00 — [Section 2 title]
3:00 — [Section 3 title]
6:00 — [Section 4 title]
8:00 — [Section 5 title]
9:00 — [Section 6 title]

💡 KEY CONCEPTS COVERED:
• [Psychology concept 1 with brief description]
• [Psychology concept 2 with brief description]
• [Psychology concept 3 with brief description]
• [Psychology concept 4 with brief description]
• [Psychology concept 5 with brief description]

🧠 ABOUT THIS VIDEO:
[2-3 sentences expanding on the topic with SEO keywords. Make it sound valuable and intriguing.]

💬 JOIN THE CONVERSATION:
[Engagement question specific to the video — different from the pinned comment]

🚨 Only the top 1% know these secrets. 
👁️ Follow to master the game they are playing on you before it's too late.

{{CREDITS_PLACEHOLDER}}

📌 TAGS:
[15-20 relevant hashtags]

SEO KEYWORDS FOR LONG-FORM (pick 5-8 relevant ones per video):
dark psychology, dark psychology explained, psychology tricks, manipulation tactics,
mind games psychology, body language secrets, human behavior psychology,
relationship psychology tips, emotional intelligence, mental strength mindset,
narcissist manipulation tactics, psychological tricks that work,
how to read people, dark psychology facts, psychology of attraction,
self improvement psychology, personal growth mindset, stoic philosophy,
confidence psychology tips, social skills psychology, influence and persuasion,
emotional manipulation signs, toxic relationship psychology, mind control techniques

DO NOT include:
- External links of any kind
- "Link in bio" or "Link in description"
- Masterclass or course or product references
- Fake credits or made-up creator names
- The {{CREDITS_PLACEHOLDER}} must appear EXACTLY as written — code will replace it later

CRITICAL FORMATTING RULE: The description MUST use actual newline characters (\n) to create line breaks.
Every section must start on a new line. Timestamps must each be on their own line. Bullet points each on their own line.
Never put multiple sections or timestamps on one line separated by commas or periods.
Use proper paragraph spacing with empty lines between sections.
"""

    user_prompt = f"""
Generate a deep-dive long-form video script about:

TOPIC: "{topic}"

ABSOLUTE REQUIREMENTS:
- The script MUST be between 1500 and 2000 words. NO EXCEPTIONS.
- The script must fill 8-10 minutes of narration when read aloud at a natural pace.
- A script under 1500 words is UNACCEPTABLE and must not be generated.
- Follow all 6 sections from your system instructions with their minimum word counts.
- The script must flow as one continuous cinematic narration with no section labels.
- Use "..." for natural pauses throughout.
- Sound like a real human documentary narrator not an AI.
- Every insight must have psychological depth and the WHY behind it.
- Use accurate psychology concepts that genuinely relate to the topic.

SECTION STRUCTURE TO FOLLOW:
- Cinematic Opening (0:00-1:00): At least 150 words. Powerful paradoxical hook.
- Hidden Foundation (1:00-3:00): At least 300 words. Why people misunderstand this topic.
- 5 Pillars of Mastery (3:00-6:00): At least 500 words. 5 deep psychological patterns with scenarios.
- Case Study (6:00-8:00): At least 300 words. Compelling historical or hypothetical example.
- Practical Exercise (8:00-9:00): At least 150 words. Actionable step-by-step exercise.
- Final Revelation (9:00-10:00): At least 150 words. Philosophical summary with subscribe CTA for {CHANNEL_NAME}.

ALSO PROVIDE:
- A viral deep-dive title with hashtags
- A comprehensive YouTube description following the LONG FORMAT in your system instructions (must include {{CREDITS_PLACEHOLDER}} exactly where credits go, with timestamps matching the sections above)
- A unique pinned comment for this specific video topic
- Exactly 10 b-roll keywords for dark aesthetic animated or anime clips on Pexels
  (each keyword must include: anime, animated, dark, cartoon, cinematic, noir, 3d, cgi)

Return ONLY valid JSON:
{{
    "title": "Deep dive title here #DarkPsychology #MindGames",
    "description": "SEO-optimized long description following the LONG FORMAT with {{CREDITS_PLACEHOLDER}} included",
    "script": "The full 1500-2000 word script flowing naturally with ... pauses...",
    "topic_used": "{topic}",
    "word_count": approximate_word_count_as_integer,
    "pinned_comment": "A unique engaging question or conversation starter specific to this video topic",
    "b_roll_keywords": ["kw1", "kw2", "kw3", "kw4", "kw5", "kw6", "kw7", "kw8", "kw9", "kw10"]
}}

REMEMBER: The script MUST be 1500-2000 words. Count your words. If it is under 1500 words, regenerate it longer.
"""

    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": long_system},
                    {"role": "user", "content": user_prompt}
                ],
                model=model,
                temperature=0.8,
                max_tokens=10000,
                top_p=0.9,
                response_format={"type": "json_object"}
            )
            content_str = response.choices[0].message.content
            result = json.loads(content_str)

            # ── Word count validation ──────────────────────────────────────
            script_text = result.get("script", "")
            word_count = len(script_text.split())
            print(f"[INFO] Long-form script word count: {word_count}")

            if word_count < 1200:
                print(f"[WARNING] Script too short ({word_count} words). Attempting regeneration...")
                retry_prompt = (
                    f"The previous script was only {word_count} words which is too short. "
                    f"I need MINIMUM 1500 words for an 8-10 minute video. "
                    f"Please regenerate the script about '{topic}' with AT LEAST 1500 words. "
                    f"Make it much longer and more detailed. Expand every section significantly. "
                    f"This is critical."
                )
                retry_response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": long_system},
                        {"role": "user", "content": user_prompt},
                        {"role": "assistant", "content": content_str},
                        {"role": "user", "content": retry_prompt}
                    ],
                    model=PRIMARY_MODEL,
                    temperature=0.8,
                    max_tokens=10000,
                    top_p=0.9,
                    response_format={"type": "json_object"}
                )
                retry_result = json.loads(retry_response.choices[0].message.content)
                retry_word_count = len(retry_result.get("script", "").split())
                print(f"[INFO] Retry script word count: {retry_word_count}")

                if retry_word_count > word_count:
                    result = retry_result

            # ── Add metadata ───────────────────────────────────────────────
            result["channel"] = CHANNEL_NAME
            result["hashtags"] = BASE_HASHTAGS
            return result

        except Exception as e:
            print(f"[Groq] Long-form error on {model}: {e}. Trying next...")

    print("[Groq] Both models failed for long-form generation.")
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def format_credits(credit_list: list) -> str:
    """
    Takes a list of Pexels creator names and returns a professionally formatted
    credits block for inserting into video descriptions.
    Strips any pre-existing '(Pexels)' suffix before re-adding it cleanly
    to prevent '(Pexels) (Pexels)' duplication.
    """
    import re as _re
    if not credit_list:
        return ""

    seen = set()
    unique_credits = []
    for credit in credit_list:
        if not credit or not credit.strip():
            continue
        # Strip any existing (Pexels) suffix (case-insensitive) to avoid duplication
        clean = _re.sub(r'\s*\(pexels\)\s*', '', credit.strip(), flags=_re.IGNORECASE).strip()
        if not clean:
            continue
        if clean.lower() not in seen:
            seen.add(clean.lower())
            unique_credits.append(clean)

    if not unique_credits:
        return ""

    credits_header = "🎬 Background Footage Credits:"
    credits_body   = "\n".join([f"  • {name} (Pexels)" for name in unique_credits])
    credits_footer = "All background footage sourced from Pexels.com under free license."

    return f"\n\n{credits_header}\n{credits_body}\n{credits_footer}"


def insert_credits_into_description(description: str, credit_list: list) -> str:
    """
    Replaces the {{CREDITS_PLACEHOLDER}} token in an AI-generated description
    with properly formatted Pexels credits.
    """
    formatted_credits = format_credits(credit_list)

    if "{{CREDITS_PLACEHOLDER}}" in description:
        return description.replace("{{CREDITS_PLACEHOLDER}}", formatted_credits)

    # Safety: if placeholder somehow missing, append credits at end
    if formatted_credits:
        return f"{description}\n{formatted_credits}"
    return description


def fix_description_formatting(description: str) -> str:
    """
    Safety-net post-processor that ensures the AI description has proper line breaks.
    The AI sometimes returns everything on one line despite prompt instructions.
    This function fixes common formatting issues before the description goes to YouTube.
    """
    import re as _re
    if not description:
        return description

    # Section headers that must always start on a new line with blank line before them
    section_markers = [
        "⏱️ TIMESTAMPS:", "⏱️ Timestamps:",
        "💡 KEY CONCEPTS COVERED:", "💡 Key Concepts Covered:", "💡 KEY CONCEPTS:",
        "🧠 ABOUT THIS VIDEO:", "🧠 About This Video:",
        "💬 JOIN THE CONVERSATION:", "💬 Join The Conversation:",
        "🔔 Subscribe",
        "👁️ Turn on",
        "📌 TAGS:", "📌 Tags:",
        "🎬 Background Footage Credits:",
        "🎬 WATCH", "🎬 Watch",
        "{{CREDITS_PLACEHOLDER}}",
    ]
    for marker in section_markers:
        if marker in description:
            description = description.replace(marker, f"\n\n{marker}")

    # Each timestamp entry on its own line: "0:00 —" or "1:00 -"
    description = _re.sub(r'([,.\s])(\d{1,2}:\d{2}\s*[—\-])', r'\n\2', description)

    # Each bullet point on its own line
    description = _re.sub(r'([,.\s])(•)', r'\n\2', description)

    # Collapse 4+ consecutive newlines to max 2
    description = _re.sub(r'\n{4,}', '\n\n\n', description)

    # Strip trailing whitespace from each line
    lines = [line.rstrip() for line in description.split('\n')]
    description = '\n'.join(lines).strip()

    return description


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