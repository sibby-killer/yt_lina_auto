"""
video_database.py — Ashley MindShift
Tracks all uploaded YouTube videos to enable cross-promotion between
Short-form and Long-form content. Database persists via git commit in GitHub Actions.
"""

import json
import os
from datetime import datetime

VIDEO_DATABASE_FILE = "video_database.json"


# ─────────────────────────────────────────────────────────────────────────────
#  LOAD / SAVE
# ─────────────────────────────────────────────────────────────────────────────
def load_video_database() -> dict:
    """Loads the video database from JSON. Returns empty structure if file doesn't exist."""
    if os.path.exists(VIDEO_DATABASE_FILE):
        try:
            with open(VIDEO_DATABASE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[VideoDB] Warning: could not read database ({e}). Starting fresh.")
    return {"shorts": [], "long_form": []}


def save_video_database(db: dict):
    """Saves the video database to JSON."""
    try:
        with open(VIDEO_DATABASE_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[VideoDB] Warning: could not save database ({e})")


# ─────────────────────────────────────────────────────────────────────────────
#  ADD VIDEOS
# ─────────────────────────────────────────────────────────────────────────────
def add_video_to_database(video_id: str, title: str, video_type: str, topic: str = ""):
    """
    Adds a newly uploaded video to the database.

    Args:
        video_id:   YouTube video ID (e.g. "dQw4w9WgXcQ")
        title:      Video title
        video_type: "short" or "long_form"
        topic:      The topic used to generate this video
    """
    if not video_id or not title:
        return

    db = load_video_database()

    entry = {
        "video_id":        video_id,
        "title":           title,
        "topic":           topic,
        "url":             f"https://youtu.be/{video_id}",
        "uploaded_at":     datetime.now().isoformat(),
        "promotion_count": 0,   # how many times this video was promoted in other videos
    }

    if video_type == "short":
        db["shorts"].append(entry)
    elif video_type == "long_form":
        db["long_form"].append(entry)
    else:
        print(f"[VideoDB] Unknown video_type '{video_type}' — not saved.")
        return

    save_video_database(db)
    print(f"[VideoDB] Saved {video_type}: '{title[:60]}' ({video_id})")


# ─────────────────────────────────────────────────────────────────────────────
#  PROMOTION TRACKING
# ─────────────────────────────────────────────────────────────────────────────
def get_least_promoted_long_form() -> dict | None:
    """
    Returns the long-form video that has been least promoted so far.
    Ensures even distribution of promotion across all long-form videos.
    Returns None if no long-form videos exist yet.
    """
    db = load_video_database()
    videos = db.get("long_form", [])
    if not videos:
        print("[VideoDB] No long-form videos in database to promote yet.")
        return None
    return min(videos, key=lambda v: v.get("promotion_count", 0))


def get_least_promoted_long_form_videos(count: int = 2) -> list:
    """
    Returns up to `count` long-form videos sorted by promotion count ascending.
    Skips any video that matches the current context (avoids self-promotion).
    """
    db = load_video_database()
    videos = db.get("long_form", [])
    if not videos:
        return []
    return sorted(videos, key=lambda v: v.get("promotion_count", 0))[:count]


def increment_promotion_count(video_id: str):
    """Increments the promotion counter for a long-form video after it has been linked."""
    db = load_video_database()
    for video in db.get("long_form", []):
        if video["video_id"] == video_id:
            video["promotion_count"] = video.get("promotion_count", 0) + 1
            break
    save_video_database(db)


# ─────────────────────────────────────────────────────────────────────────────
#  DESCRIPTION CROSS-PROMOTION INJECTION
# ─────────────────────────────────────────────────────────────────────────────
def add_video_promotion_to_description(description: str, video_type: str = "short",
                                       current_video_id: str = None) -> str:
    """
    Injects cross-promotion links into a video description.
    - Shorts get a link to the least-promoted long-form video.
    - Long-form gets links to up to 2 other long-form videos.

    Links are inserted before {{CREDITS_PLACEHOLDER}} or before 📌 TAGS.
    Returns description unchanged if no videos are available to promote.
    """
    if video_type == "short":
        promo = get_least_promoted_long_form()
        if not promo:
            return description

        promo_section = (
            f"\n\n🎬 WATCH THE FULL DEEP-DIVE:\n"
            f"▶️ {promo['title']}\n"
            f"🔗 {promo['url']}"
        )
        increment_promotion_count(promo["video_id"])
        print(f"[PROMO] Short → Long-form: '{promo['title'][:50]}'")

    elif video_type == "long_form":
        # exclude the video currently being uploaded from its own promotion list
        all_promos = get_least_promoted_long_form_videos(count=3)
        promos = [v for v in all_promos if v.get("video_id") != current_video_id][:2]
        if not promos:
            return description

        lines = ["\n\n🎬 WATCH MORE DEEP-DIVES:"]
        for pv in promos:
            lines.append(f"▶️ {pv['title']}")
            lines.append(f"🔗 {pv['url']}")
            lines.append("")
            increment_promotion_count(pv["video_id"])
        promo_section = "\n".join(lines)
        print(f"[PROMO] Long-form → {len(promos)} other video(s)")

    else:
        return description

    # Insert before the credits placeholder (preferred position)
    if "{{CREDITS_PLACEHOLDER}}" in description:
        return description.replace("{{CREDITS_PLACEHOLDER}}",
                                   f"{promo_section}\n\n{{{{CREDITS_PLACEHOLDER}}}}")

    # Fallback: insert before tags section
    for tag_marker in ("📌 TAGS:", "📌 Tags:"):
        if tag_marker in description:
            return description.replace(tag_marker, f"{promo_section}\n\n{tag_marker}")

    # Final fallback: append at end
    return f"{description}\n{promo_section}"


# ─────────────────────────────────────────────────────────────────────────────
#  STATS
# ─────────────────────────────────────────────────────────────────────────────
def get_database_stats() -> dict:
    """Returns a quick summary of the video database."""
    db = load_video_database()
    return {
        "total_shorts":    len(db.get("shorts", [])),
        "total_long_form": len(db.get("long_form", [])),
        "total_videos":    len(db.get("shorts", [])) + len(db.get("long_form", [])),
    }
