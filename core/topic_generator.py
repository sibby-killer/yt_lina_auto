import random

FALLBACK_TOPICS = [
    "The Dark Triad: Machiavellianism, Narcissism, and Psychopathy",
    "How to spot a liar using the 3-second eye contact rule",
    "The Ben Franklin Effect: Making someone like you by asking for a favor",
    "The Push-Pull Technique in social dynamics",
    "The psychological power of the 'Silent Treatment'",
    "How to use mirroring to build instant subconscious trust",
    "The 'Door-in-the-Face' technique for persuasion",
    "Cognitive Dissonance: Why we justify our worst mistakes",
    "The Pygmalion Effect: How expectations shape reality",
    "Spotting micro-expressions of contempt",
    "The power of 'social proof' and how to manufacture it",
    "How to protect yourself from gaslighting",
    "The 'Scarcity Principle' in human attraction",
    "How posture affects your cortisol levels and confidence",
    "The psychology of color in persuasion",
    "Why humans are programmed to follow authority (Milgram Experiment)",
    "The bystander effect and how to break it",
    "How to win any argument with the Socratic method",
    "Understanding the 'uncanny valley' and fear",
    "How to use 'anchoring' to dominate negotiations",
    "The dark psychology of cult recruitment",
    "Why you feel watched when you are alone (The Primal Fear)",
    "How to make someone obsessed with your validation",
    "The psychological trick to stop an intruder's momentum",
    "How to read a person's handshake",
    "The 'Halo Effect' and how to use it for your advantage",
    "How to manipulate time perception in conversation",
    "The psychology of the 'Ikea Effect' (ownership bias)",
    "How to use silence to make others confess",
    "The 'Zeigarnik Effect': Why we remember unfinished tasks",
    "How to identify a 'covert narcissist' in 5 minutes",
    "The power of the 'Third Party' validation",
    "How to use the 'Contrast Principle' for sales",
    "Psychological tricks to wake up instantly",
    "The dark truth about 'Love Bombing'",
    "How to read someone's pupils for attraction or fear",
    "The 'Choice Paradox': Why less is more",
    "How to dominate a room without saying a word",
    "Psychology of the 'Forbidden Fruit' effect",
    "How to spot a fake smile instantly",
    "The 'Spotlight Effect': Why nobody is actually looking at you",
    "How to use 'Reverse Psychology' effectively on adults",
    "The power of using someone's name in conversation",
    "How to influence someone's dreams (The Inception Trick)",
    "The 'Foot-in-the-door' technique for compliance",
    "Understanding 'learned helplessness' in relationships",
    "How to use 'forced choice' to get what you want",
    "The 'Dunning-Kruger Effect' and its danger",
    "How breathing patterns reveal hidden anxiety",
    "The psychology of 'intermittent reinforcement' and addiction",
    "How to win a debate by staying calm",
    "The 'Primacy Effect': Why first impressions are everything",
    "How to detect verbal manipulation patterns",
    "The psychology of the 'Red Queen' effect in social status",
    "How to use 'Mirror neurons' for instant rapport",
    "The 'False Consensus Effect': Why we think others think like us",
    "How to identify emotional vampires",
    "The 'Barnum Effect': Why horoscopes feel so real",
    "How to use 'pacing and leading' for persuasion",
    "The psychology of the 'black sheep' in any group",
    "How to build a 'frame' that others must follow",
    "The 'Decoy Effect' in pricing and choices",
    "Understanding the 'limbic system's' role in flash anger",
    "How to use 'sensory anchoring' for memory",
    "The psychology of the 'Victim Complex'",
    "How to spot an 'Energy Thief' immediately",
    "The power of 'The Pause' in public speaking",
    "How to read leg and foot direction for interest",
    "The 'Reciprocity' rule: The most powerful social weapon",
    "How to use 'Negative Body Language' to push someone away",
    "The psychology of 'Stockholm Syndrome' in daily life",
    "How to use 'Cognitive Reframing' to kill fear",
    "The 'Loss Aversion' principle and how it controls you",
    "How to identify subconscious 'tells' in high stakes",
    "The 'Ostrich Effect': Why we ignore bad news",
    "How to use 'Cold Reading' basics in social settings",
    "The 'Backfire Effect': Why facts don't change minds",
    "How to use the 'Yes-Set' for easier agreement",
    "The psychology of 'Mass Hysteria' and how to avoid it",
    "How to read the 'Tilt' of a person's head",
    "The 'Mere Exposure Effect': Why we like what's familiar",
    "How to identify 'Passive-Aggressive' patterns",
    "The 'Gambler's Fallacy' in decision making",
    "How to use 'Future Pacing' to create desire",
    "The psychology of the 'Alpha' vs 'Sigma' mentalities",
    "How to break someone's concentration with a simple question",
    "The 'Self-Serving Bias' and how to exploit it",
    "How to use 'Color Psychology' for your clothing",
    "The 'Survivorship Bias' in success stories",
    "How to read someone's 'Comfort Zone' based on space",
    "The power of 'Repetition' in propaganda and branding",
    "How to keep your cool when being insulted",
    "The 'Just-World Hypothesis' and why it's a trap",
    "How to identify if someone is 'Mirroring' you for manipulation",
    "The psychological impact of 'Dark Patterns' in apps",
    "How to use 'Ego Depletion' for better negotiations",
    "The 'Priming' effect: How subtle cues change behavior",
    "How to recognize a 'flying monkey' in a narcissistic group",
    "The 'Sunk Cost Fallacy': Why we stay in bad situations",
    "How to use 'Vulnerability' as a tool for connection",
    "The final secret of human mastery: Autonomy"
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
    Placeholder for Supabase fetching of previously used topics.
    """
    # For now, we return empty so it picks from the pool
    return []

if __name__ == "__main__":
    print(f"Total Viral Topics: {len(FALLBACK_TOPICS)}")
    print(f"Sample Topic: {get_next_topic()}")
