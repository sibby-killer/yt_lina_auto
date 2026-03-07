"""
Topic Generator for Indigo Insights
Focus: Practical Psychology, Body Language, Mirroring, and Manipulation.
"""
import random
import logging

log = logging.getLogger(__name__)

REDDIT_SUBREDDITS = [
    "psychology",
    "socialengineering",
    "communication",
    "sociopath", # For "dark" insights
    "bodylanguage",
]

FALLBACK_TOPICS = [
    "The 3-second rule for reading anyone's intentions",
    "How to use mirroring to make someone trust you instantly",
    "The dark art of the silent treatment and why it works",
    "How to spot a liar using only their eyes",
    "The 'Push-Pull' technique: the ultimate psychological attraction hack",
    "How to remain calm in an argument using the 'Gray Rock' method",
    "Why you should never say the word 'Actually' in a negotiation",
    "The power of the pregnant pause: make them reveal more than they want",
    "How to use 'The Benjamin Franklin Effect' to turn an enemy into a friend",
    "The psychological reason why people can't look you in the eye",
    "How to detect a fake smile in less than a second",
    "The 'Love Bombing' red flags you need to know",
    "How to use active listening to control any conversation",
    "The secret of 'Anchoring' in salary negotiations",
    "Why you should always sit on the left side of your boss",
    "How to win any debate using the 'Socratic Method'",
    "The mystery of the 'Columbo' technique for finding the truth",
    "How to build instant rapport with a total stranger",
    "The 'Foot-in-the-Door' technique: how to get people to say yes",
    "Why wearing blue makes people trust you more",
]

def get_next_topic(used_topics: list[str] | None = None) -> str:
    """Returns a psychology-focused topic."""
    used = set(t.lower() for t in (used_topics or []))
    available = [t for t in FALLBACK_TOPICS if t.lower() not in used]
    if not available: available = FALLBACK_TOPICS
    chosen = random.choice(available)
    print(f"[Topics] Psychology topic selected: {chosen}")
    return chosen

def get_used_topics_from_db(): return [] # Placeholder
