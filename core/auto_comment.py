"""
Auto-Comment Bot — Ashley MindShift
Posts and pins a unique AI-generated comment on each video.
Falls back to a curated pool if no AI comment is available.
"""

import random

# ─────────────────────────────────────────────────────────────────────────────
#  FALLBACK COMMENT POOL
#  Used only when ai_script.py did NOT return a pinned_comment value.
# ─────────────────────────────────────────────────────────────────────────────
FALLBACK_COMMENTS = [
    "This one hit different... what part resonated with you the most? 🧠 Drop it below",
    "Be honest... did you already know this or did this just blow your mind? 👀",
    "Which point from this video are you going to start using TODAY? Let me know 👇",
    "Real talk... has anyone ever used these psychology tricks on YOU without you knowing? �",
    "What is the darkest psychology fact you have ever learned? Share it below... 😏",
    "Plot twist... most people will watch this and do nothing. Will you be different? 👇",
    "I am curious... what topic should I cover next? Drop your suggestions below 🧠",
    "The scariest part about dark psychology is that it is happening to you every single day... agree or disagree? 🤔",
    "Which psychology concept from this video surprised you the most? Be honest 👀",
    "Have you ever caught yourself unconsciously using any of these techniques? Tell me your story 👇",
]


def get_comment_text(ai_generated_comment: str = None) -> str:
    """Returns AI-generated comment if available, otherwise picks from fallback pool."""
    if ai_generated_comment and len(ai_generated_comment.strip()) > 10:
        return ai_generated_comment.strip()
    return random.choice(FALLBACK_COMMENTS)


def post_pinned_comment(youtube, video_id: str, comment_text: str = None) -> str | None:
    """
    Posts and pins a comment on the specified video.

    Args:
        youtube:      Authenticated YouTube API client.
        video_id:     The YouTube video ID to comment on.
        comment_text: AI-generated comment from video_content.get("pinned_comment").
                      If None or empty, a random fallback comment is used.

    Returns:
        comment_id on success, None on failure.
    """
    if not youtube or not video_id:
        return None

    final_comment = get_comment_text(comment_text)

    try:
        insert_response = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": final_comment
                        }
                    }
                }
            }
        ).execute()

        comment_id = insert_response["snippet"]["topLevelComment"]["id"]

        youtube.comments().setModerationStatus(
            id=comment_id,
            moderationStatus="published",
            banAuthor=False
        ).execute()

        print(f"[Comment] Posted & Pinned: '{final_comment[:60]}...'")
        print(f"[Comment] Video: https://youtu.be/{video_id}")
        return comment_id

    except Exception as e:
        print(f"[Comment] Error posting comment: {e}")
        return None
