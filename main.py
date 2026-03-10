import os
import re
import argparse
from dotenv import load_dotenv

load_dotenv()

from core.ai_script import generate_video_content, CHANNEL_NAME
from core.tts import generate_voiceover
from core.yt_scraper import download_viral_b_roll
from core.video_editor import stitch_video
from core.supabase_db import log_video, update_video_upload, cleanup_old_logs
from config import VID_BG_DIR
import random


def create_short(topic: str = None, progress_callback=None) -> bool:
    """
    Master function for Ashley MindShift.
    """
    def log(msg):
        print(msg)
        if progress_callback:
            progress_callback(msg)

    # ── 0. DB Cleanup (Maintain Free Plan space) ──────────────────────────
    try:
        cleanup_old_logs(days=7)
    except Exception as e:
        print(f"[Cleanup] Failed: {e}")

    # ── 1. Generate Script & Metadata ──────────────────────────────────────
    # ai_script.py auto-picks a topic if none is passed
    log("[1/5] Brainstorming with Groq...")
    content = generate_video_content(topic)
    if not content:
        log("Failed to generate content. Exiting.")
        return False

    # Read the topic the AI actually used (may have been auto-selected)
    topic = content.get('topic_used', topic) or topic

    log(f"  Title   : {content.get('title')}")
    log(f"  Keywords: {content.get('b_roll_keywords')}")

    # ── 2. Generate Voiceover ───────────────────────────────────────────────
    log("\n[2/5] Recording Voiceover with Edge-TTS...")
    audio_path, srt_path = generate_voiceover(content.get('script'), filename="voiceover.mp3")

    # ── 3. Download B-Roll ─────────────────────────────────────────────────
    log("\n[3/5] Downloading Viral TikTok B-Roll...")
    keywords = content.get('b_roll_keywords', [])
    broll_paths, credits = download_viral_b_roll(keywords, clips_per_keyword=2, progress_callback=progress_callback)

    if not broll_paths:
        log("Failed to download B-roll. Exiting.")
        return False

    # ── 4. Assemble Video ──────────────────────────────────────────────────
    log("\n[4/5] Assembling Final MP4...")
    safe_title = re.sub(r'[\\/*?:"<>|#]', "", content.get("title", "video")).strip().replace(" ", "_")
    output_filename = f"{safe_title[:40]}_final.mp4"

    # Select random background music
    bg_music_path = None
    if os.path.exists(VID_BG_DIR):
        music_files = [f for f in os.listdir(VID_BG_DIR) if f.endswith(".mp3")]
        if music_files:
            bg_music_path = os.path.join(VID_BG_DIR, random.choice(music_files))
            log(f"Selected Professional BG Music: {os.path.basename(bg_music_path)}")

    final_video_path = stitch_video(
        audio_path, broll_paths,
        output_filename=output_filename,
        srt_path=srt_path,
        bg_music_path=bg_music_path
    )

    if not final_video_path:
        log("\nFAILED to assemble video.")
        return False

    log(f"\nSUCCESS! Video ready: {final_video_path}")

    # Build full SEO description with Pexels credits inserted at placeholder
    from core.ai_script import insert_credits_into_description
    final_desc = insert_credits_into_description(
        content.get('description', ''),
        credits  # list of creator names returned by download_viral_b_roll
    )

    # ── 5. Supabase Logging ────────────────────────────────────────────────
    log("\n[5/5] Logging to Supabase & Uploading to YouTube...")
    db_record = log_video(
        title=content.get('title', ''),
        topic=topic,
        script=content.get('script', ''),
        local_path=final_video_path,
        description=final_desc,
        tags=keywords,
        status='generated'
    )

    # ── 6. YouTube Upload ──────────────────────────────────────────────────
    from core.youtube_uploader import get_authenticated_service, upload_video, find_or_create_playlist, add_video_to_playlist
    youtube_service = get_authenticated_service()
    if youtube_service:
        video_tags = keywords + ["Psychology", "Mindset", "Success", "Manipulation", "Shorts"]
        yt_id = upload_video(
            youtube_service,
            final_video_path,
            content.get('title'),
            final_desc,
            video_tags,
            privacy_status="public"
        )
        if yt_id:
            if db_record:
                update_video_upload(db_record.get('id'), yt_id)
            
            # --- PLAYLIST INTEGRATION ---
            from config import YOUTUBE_PLAYLIST_ID
            plist_id = YOUTUBE_PLAYLIST_ID
            if not plist_id:
                plist_title = f"{CHANNEL_NAME} - The Art of Human Mastery"
                plist_desc  = (
                    f"Master the psychological patterns of human behavior with {CHANNEL_NAME}. "
                    "Secrets of persuasion, communication, and social dominance uploaded daily. #Psychology #Success"
                )
                plist_id = find_or_create_playlist(youtube_service, plist_title, plist_desc)
            
            if plist_id:
                add_video_to_playlist(youtube_service, yt_id, plist_id)
            
            # Post AI-generated pinned comment (falls back to pool if missing)
            from core.auto_comment import post_pinned_comment
            pinned_comment = content.get("pinned_comment", None)
            post_pinned_comment(youtube_service, yt_id, comment_text=pinned_comment)
            log(f"Successfully uploaded to YouTube! ID: {yt_id}")
    else:
        log("[Upload] YouTube auth not available — video saved locally only.")

    # ── 7. Facebook Reels Upload ──────────────────────────────────────────
    from core.facebook_uploader import upload_to_facebook_reels
    fb_page_id = os.getenv("FACEBOOK_PAGE_ID")
    fb_token   = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    if fb_page_id and fb_token:
        log("\n[6/7] Distributing to Facebook Reels...")
        upload_to_facebook_reels(final_video_path, content.get('title'), fb_page_id, fb_token)
    else:
        log("\n[6/7] Skipping Facebook - Credentials not set.")

    # ── 8. TikTok Upload ──────────────────────────────────────────────────
    from core.tiktok_uploader import upload_to_tiktok
    tt_cookies = os.getenv("TIKTOK_COOKIES_PATH", "tiktok_cookies.txt")
    if os.path.exists(tt_cookies):
        log("\n[7/7] Distributing to TikTok...")
        upload_to_tiktok(final_video_path, content.get('title'), tt_cookies)
    else:
        log("\n[7/7] Skipping TikTok - Cookies file not found.")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indigo Insights Video Generator")
    parser.add_argument("--topic", type=str, default=None, help="Override topic")
    args = parser.parse_args()
    create_short(topic=args.topic)
