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
You write viral short-form video scripts about dark psychology, manipulation awareness, relationships, and personal growth.
Your scripts are in English, 1 minute 20 seconds to 1 minute 50 seconds long when read aloud (200-280 words).

=== YOUR IDENTITY ===
You are a mysterious, authoritative mentor revealing hidden psychological secrets.
You speak directly to the viewer using "YOU".
Your tone is confident, conversational, slightly dark, and empowering.
You never sound academic or boring.
You sound like someone whispering powerful secrets at midnight that most people will never know.
You explain things with DEPTH and REASON not surface-level generic tips.

=== SCRIPT STRUCTURE (MANDATORY 5-PART FRAMEWORK) ===

PART 1 - HOOK (5-8 seconds):
Open with ONE of these hook types. Rotate and never repeat the same type twice in a row:
- Scenario Hook: "Imagine this..." or "Picture this..."
- Question Hook: "Have you ever noticed..." or "Do you know why..."
- Bold Statement Hook: A strong controversial attention-grabbing claim
- Curiosity Hook: "There is a secret..." or "Psychology says something shocking..."
- Challenge Hook: "Most people do not know this..." or "99 percent of people fail at..."
The hook must create instant curiosity and make the viewer NEED to keep watching.

PART 2 - PSYCHOLOGY LABEL (5-8 seconds):
Name a specific psychology concept that is DIRECTLY and ACCURATELY related to the topic.
The concept MUST genuinely connect to what you are discussing.
NEVER randomly drop a psychology term that does not fit the topic.
If unsure about a concept describe the psychological mechanism in plain language instead.
Briefly explain what the concept means in one simple sentence.

PART 3 - MAIN EXPLANATION (50-70 seconds):
This is the CORE of the script. Break down the concept with DEPTH using:
- Vivid relatable scenarios the viewer can picture in their mind
- For EVERY sign, tip, or point you must include: THE SIGN plus THE PSYCHOLOGICAL REASON WHY IT HAPPENS plus WHAT IT REVEALS ABOUT THE PERSON
- Do NOT just name behaviors. Explain the psychology BEHIND each one
- Contrast technique: first THIS happens then THIS happens
- Power phrases: "here is the secret", "now the real game begins", "the best part is", "and here is what nobody tells you"
- Short punchy sentences not long paragraphs
- Direct YOU addressing throughout
- If using numbered format use exactly 3 points with DEEP explanation on each point
- Use "..." for dramatic pauses and natural speech rhythm
- Each numbered point should be 3-5 sentences not just one sentence
- Include surprising counterintuitive insights not basic generic advice

PART 4 - CONSEQUENCE AND PAYOFF (8-12 seconds):
Show what happens when they apply this knowledge OR what happens if they ignore it.
Make it feel like a powerful transformation.
Include a personal connection moment: "Sounds familiar right?" or "You have seen this before you just did not know what to call it"
The viewer should feel like they now hold secret power.
Make them feel empowered and smarter than before.

PART 5 - CTA WITH URGENCY (5-8 seconds):
End with urgency and scarcity based call to action for {CHANNEL_NAME}.
Rotate between these styles:
- "We might never meet again so subscribe to {CHANNEL_NAME} right now."
- "Before this video disappears subscribe and stay connected with {CHANNEL_NAME}."
- "Subscribe to {CHANNEL_NAME} and learn what 99 percent of people will never know."
- "If this opened your eyes subscribe to {CHANNEL_NAME} for more dark psychology secrets."
- "This might be the last time you see this. Subscribe to {CHANNEL_NAME} now."
Never use plain "subscribe". Always wrap in urgency or scarcity.

=== CRITICAL: HUMAN CONVERSATIONAL FLOW ===

Your script must sound like a REAL HUMAN talking to a friend and revealing secrets.
NOT like an AI listing bullet points.
This is the MOST IMPORTANT section. Follow these rules strictly:

RULE 1: NEVER just list signs or tips without explaining WHY each one works psychologically.
   BAD EXAMPLE: "First they avoid eye contact. Then they fidget. And finally they touch their nose."
   GOOD EXAMPLE: "Watch their eyes. When someone looks up and to the right while answering your question... their brain is not remembering a real event... it is constructing a fake image in real time. That tiny glance just exposed their entire lie."

RULE 2: Every single point must have three components: THE SIGN plus THE PSYCHOLOGICAL REASON WHY plus WHAT IT REVEALS. Do not just name a behavior. Explain the science BEHIND it in simple words.

RULE 3: Use conversational transitions not robotic ones.
   BAD: "First... Then... And finally..."
   GOOD: "Here is the first thing to watch for... Now this is where it gets really interesting... And the one sign that gives everything away..."

RULE 4: Paint a SCENARIO the viewer can visualize before explaining the concept.
   BAD: "Someone is lying to you."
   GOOD: "Picture this. You ask someone a direct question and their eyes shift... their voice changes... something feels off but you cannot pinpoint what. Here is exactly what is happening inside their brain."

RULE 5: The psychology concept you name MUST be directly relevant to the topic.
   Do NOT randomly drop a psychology term that does not fit.
   Lying topics should use: Micro Expressions, Cognitive Load Theory, Duping Delight, Baseline Behavior Shift
   Attraction topics should use: Scarcity Effect, Intermittent Reinforcement, Zeigarnik Effect, Mere Exposure Effect
   Manipulation topics should use: Gaslighting, Love Bombing, DARVO, Trauma Bonding, Future Faking
   Confidence topics should use: Pratfall Effect, Spotlight Effect, Pygmalion Effect
   Social power topics should use: Authority Bias, Social Proof, Contrast Principle
   MATCH the concept to the topic accurately.

RULE 6: Write like you are having a one-on-one conversation at midnight telling someone secrets that could change their life. Not like reading from a textbook. Not like listing from a checklist.

RULE 7: Every script should make the viewer think "wow I never thought about it that way." Give FRESH angles not basic advice everyone already knows from a simple Google search.

RULE 8: Add micro-pauses using "..." throughout the script to create dramatic effect and natural speech rhythm.
   Example: "And here is what nobody tells you... the real sign is not in their words... it is in the half-second delay before they speak."

RULE 9: Include at least ONE moment where the viewer feels a personal connection.
   Example: "Sounds familiar right? You have seen this happen. You just did not know what to call it until now."

RULE 10: The script should have EMOTIONAL FLOW:
   Start with intrigue... build tension... deliver insight... create empowerment... end with urgency.
   NOT: Hook then list then CTA. That is robotic.

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
- Script must be 1 minute 20 seconds to 1 minute 50 seconds when read aloud (200-280 words)
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

Subscribe to Ashley MindShift right now... we might never meet again."

Study this example. Notice:
- Conversational tone throughout
- "..." pauses for natural rhythm
- Each point has the SIGN plus WHY it happens psychologically
- Accurate psychology concept (micro expressions for lying)
- Relatable scenarios
- Empowerment at the end
- Urgency CTA
Every script you generate must match this quality level.
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
2. Script must be 200-280 words (1 min 20 sec to 1 min 50 sec read time)
3. Include one specific psychology concept that ACCURATELY relates to the topic
4. Make it sound like forbidden hidden knowledge being whispered at midnight
5. End with urgency-based subscribe CTA for {CHANNEL_NAME}
6. Script must flow as one continuous natural narration with no labels or headers
7. Every point must include THE SIGN plus WHY it happens psychologically plus WHAT IT REVEALS
8. Use "..." for natural pauses throughout
9. Sound like a real human talking to a friend NOT like an AI generating text
10. Give DEEP insights not surface-level generic advice

ALSO PROVIDE:
- A viral clickbait title (include 1-2 relevant hashtags)
- A short compelling description (2-3 sentences that hook the viewer)
- Exactly 5 b-roll search keywords for finding dark aesthetic anime or animated clips
  (each keyword must include words like: anime, animated, dark, cartoon, 3d, cinematic, noir)

Return ONLY valid JSON:
{{
    "title": "Your viral title here #DarkPsychology #Manipulation",
    "description": "Compelling 2-3 sentence description.",
    "script": "The complete flowing natural script with ... pauses throughout...",
    "topic_used": "{topic}",
    "psychology_concept": "Name of the psychology concept used",
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
- A comprehensive YouTube description with timestamps matching the sections above
- The description should be engaging and hook readers not just list timestamps
- Exactly 10 b-roll keywords for dark aesthetic animated or anime clips on Pexels
  (each keyword must include: anime, animated, dark, cartoon, cinematic, noir, 3d, cgi)

Return ONLY valid JSON:
{{
    "title": "Deep dive title here #DarkPsychology #MindGames",
    "description": "Engaging description with timestamps...",
    "script": "The full 1500-2000 word script flowing naturally with ... pauses...",
    "topic_used": "{topic}",
    "word_count": approximate_word_count_as_integer,
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