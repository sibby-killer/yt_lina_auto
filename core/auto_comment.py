"""
Auto-Comment Bot — Indigo Insights
"""
CTA_COMMENT_TEXT = (
    "Which psychological trick do you think is the MOST dangerous? 🧠 "
    "Master the art of the mind: Follow @AshleyMindShift "
    "Check the link in our bio for the masterclass! 🚀"
)

def post_pinned_comment(youtube, video_id: str) -> str | None:
    if not youtube or not video_id: return None
    try:
        insert_response = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {"snippet": {"textOriginal": CTA_COMMENT_TEXT}}
                }
            }
        ).execute()
        comment_id = insert_response["snippet"]["topLevelComment"]["id"]
        youtube.comments().setModerationStatus(id=comment_id, moderationStatus="published", banAuthor=False).execute()
        print(f"[Comment] Posted & Pinned on https://youtu.be/{video_id}")
        return comment_id
    except Exception as e:
        print(f"[Comment] Error: {e}")
        return None
