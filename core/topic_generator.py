import random

FALLBACK_TOPICS = [
    # 1-20: Dark Triad & Personality
    "The Dark Triad: Machiavellianism, Narcissism, and Psychopathy",
    "How to spot a liar using the 3-second eye contact rule",
    "How to identify a 'covert narcissist' in 5 minutes",
    "The dark truth about 'Love Bombing'",
    "How to recognize a 'flying monkey' in a narcissistic group",
    "The psychology of the 'Alpha' vs 'Sigma' mentalities",
    "The 'Halo Effect' and how to use it for your advantage",
    "How to read someone's pupils for attraction or fear",
    "Spotting micro-expressions of contempt",
    "How to identify emotional vampires",
    "The 'Barnum Effect': Why horoscopes feel so real",
    "How to read a person's handshake",
    "The psychology of the 'black sheep' in any group",
    "Understanding 'learned helplessness' in relationships",
    "How to identify 'Passive-Aggressive' patterns",
    "The 'Self-Serving Bias' and how to exploit it",
    "How to detect verbal manipulation patterns",
    "The psychology of 'Stockholm Syndrome' in daily life",
    "How to recognize if someone is 'Mirroring' you for manipulation",
    "The 'Spotlight Effect': Why nobody is actually looking at you",

    # 21-40: Social Influence & Persuasion
    "The Ben Franklin Effect: Making someone like you by asking for a favor",
    "The Push-Pull Technique in social dynamics",
    "The psychological power of the 'Silent Treatment'",
    "How to use mirroring to build instant subconscious trust",
    "The 'Door-in-the-Face' technique for persuasion",
    "The 'Foot-in-the-door' technique for compliance",
    "The 'Scarcity Principle' in human attraction",
    "The 'Reciprocity' rule: The most powerful social weapon",
    "How to use 'Reverse Psychology' effectively on adults",
    "The power of using someone's name in conversation",
    "How to use 'forced choice' to get what you want",
    "How to use 'anchoring' to dominate negotiations",
    "The 'Contrast Principle' for sales",
    "How to use 'pacing and leading' for persuasion",
    "How to build a 'frame' that others must follow",
    "The 'Decoy Effect' in pricing and choices",
    "The 'Mere Exposure Effect': Why we like what's familiar",
    "How to use 'False Consensus' to influence groups",
    "The 'Backfire Effect': Why facts don't change minds",
    "The power of 'The Pause' in public speaking",

    # 41-60: Cognitive Biases & Mind Hacks
    "Cognitive Dissonance: Why we justify our worst mistakes",
    "The Pygmalion Effect: How expectations shape reality",
    "The 'Zeigarnik Effect': Why we remember unfinished tasks",
    "The 'Ikea Effect': Why we overvalue what we build",
    "The 'Choice Paradox': Why less is more",
    "The 'Dunning-Kruger Effect' and its danger",
    "The 'Ostrich Effect': Why we ignore bad news",
    "The 'Gambler's Fallacy' in decision making",
    "The 'Survivorship Bias' in success stories",
    "The 'Sunk Cost Fallacy': Why we stay in bad situations",
    "The 'Just-World Hypothesis' and why it's a trap",
    "The 'False Memory' phenomenon and how it's implanted",
    "The 'Confirmation Bias' and how it blinds you",
    "The 'Availability Heuristic' and media manipulation",
    "The 'Anchoring Bias' in every purchase you make",
    "The 'Primacy Effect': Why first impressions are everything",
    "Psychological tricks to wake up instantly",
    "How to use 'Cognitive Reframing' to kill fear",
    "The power of 'Repetition' in propaganda and branding",
    "The 'Loss Aversion' principle and how it controls you",

    # 61-80: Body Language & Bio-Hacks
    "How posture affects your cortisol levels and confidence",
    "How breathing patterns reveal hidden anxiety",
    "How to read leg and foot direction for interest",
    "How to read someone's 'Comfort Zone' based on space",
    "How to spot a fake smile instantly",
    "The 'Uncanny Valley' and the fear of the human-like",
    "How to manipulate time perception in conversation",
    "How to influence someone's dreams (The Inception Trick)",
    "Understanding the 'limbic system's' role in flash anger",
    "How to use 'sensory anchoring' for memory",
    "How to use 'Negative Body Language' to push someone away",
    "How to build extreme 'presence' without speaking",
    "The psychology of color in persuasion",
    "How to keep your cool when being insulted",
    "How to break someone's concentration with a simple question",
    "The 'Mirror Neuron' secret for instant rapport",
    "How to use 'Ego Depletion' for better negotiations",
    "The 'Priming' effect: How subtle cues change behavior",
    "How to read the 'Tilt' of a person's head",
    "The psychology of the 'Third Party' validation",

    # 81-100: Deep Psychology & Fear
    "The dark psychology of cult recruitment",
    "Why you feel watched when you are alone (The Primal Fear)",
    "The psychology of 'intermittent reinforcement' and addiction",
    "The bystander effect and how to break it",
    "How to make someone obsessed with your validation",
    "The psychological trick to stop an intruder's momentum",
    "The psychology of the 'Victim Complex'",
    "The final secret of human mastery: Autonomy",
    "Why humans are programmed to follow authority (Milgram Experiment)",
    "The psychology of 'Mass Hysteria' and how to avoid it",
    "How to use 'Cold Reading' basics in social settings",
    "How to use 'Future Pacing' to create desire",
    "How to spot an 'Energy Thief' immediately",
    "The 'Red Queen' effect in social status",
    "The 'Yes-Set' for easier agreement",
    "The psychology of 'Dark Patterns' in apps",
    "The 'Vulnerability' trap in connections",
    "How to own a room with the 'Socratic Method'",
    "The 'Black Swan' event and human preparation",
    "The 'Prisoner's Dilemma' in everyday life",

    # 101-125: Relationship Mastery & Obsession (New Pysc-Secrets style)
    "How to create a 'Need' for your presence by disappearing",
    "The 'Push-Pull' method for peak attraction",
    "Why mystery is more powerful than beauty in relationships",
    "How to use 'Validation' as a reward, not a gift",
    "The 'Forbidden Fruit' effect: Why secrecy builds passion",
    "How to make someone feel they are 'winning' you",
    "The psychology of the 'Chase' and why you must never be the one",
    "How to use 'Casual Jealousy' to test interest",
    "Why being 'Too Nice' is a psychological death sentence",
    "The 'Hero Instinct' and how to trigger it subconsciously",
    "How to use 'Investment' to make someone never want to leave",
    "The 'Benjamin Franklin' trick for romantic interest",
    "How to identify a 'Taker' before they drain you",
    "The 'Power of No': Why setting boundaries is magnetic",
    "How to use 'Intermittent Ghosting' for psychological dominance",
    "The 'Broken Window' theory in personal relationships",
    "How to create a 'Shared Secret' to bind someone to you",
    "The 'Damsel in Distress' vs 'Knight in Shining Armor' triggers",
    "Why 'Confidence' is just a series of deliberate micro-acts",
    "How to use 'Silent Presence' to dominate a conversation",
    "The 'Zeigarnik Effect' in unfinished romantic business",
    "How to spot 'Future Faking' in a potential partner",
    "The 'Love Map' theory: How to learn someone's hidden desires",
    "How to use 'Tactical Empathy' to get any truth",
    "The 'Contrast Effect' in dating and presentation",

    # 126-150: Peak Performance & Social Hacking (Viral Focus)
    "The '30-Second Rule' for networking success",
    "How to use 'Strategic Informality' to disarm authority",
    "The 'Gaze' technique for absolute social power",
    "How to use 'Social Proof' when you have zero followers",
    "The 'Expert' frame: How to speak and have everyone listen",
    "How to identify 'Social Hierarchies' in any room instantly",
    "The 'Scarcity of Words': Why leaders speak the least",
    "How to handle 'High-Status' individuals without acting small",
    "The 'Pre-Suasion' secret: Setting the stage before you ask",
    "How to use 'Negative Visualization' to become fearless",
    "The 'Stoic' response to public embarrassment",
    "How to create 'Artificial Urgency' in any situation",
    "The 'Authority Bias' and how to dress for it",
    "How to use 'Physical Anchoring' to switch on focus",
    "The 'Pareto Principle' in social influence (The 80/20 Rule)",
    "How to read 'Group Dynamics' by looking at shoulder angles",
    "The 'Pivot' method for awkward conversations",
    "How to use 'Self-Deprecation' without losing respect",
    "The 'Master-Slave' dialectic in modern office politics",
    "How to identify 'Insecure' leaders through their praise",
    "The 'Quiet Room' trick for negotiation dominance",
    "How to use 'Flattery' the right way (The Target's Blindspot)",
    "The 'Prophet' frame: Predicting the future to gain followers",
    "How to use 'Symbolism' and 'Myth' to build a personal brand",
    "The 'Death Awareness' hack for ultimate productive focus"
]

def get_next_topic(used_topics=None):
    """
    Returns a fresh topic from the viral pool.
    """
    if used_topics is None:
        used_topics = []
    
    available = [t for t in FALLBACK_TOPICS if t not in used_topics]
    if not available:
        return random.choice(FALLBACK_TOPICS)
    
    return random.choice(available)

def get_used_topics_from_db():
    """
    Fetches previously used topics from Supabase.
    """
    from core.supabase_db import get_used_topics
    return get_used_topics()
