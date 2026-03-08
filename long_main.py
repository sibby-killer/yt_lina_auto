import os
import re
import argparse
from dotenv import load_dotenv

load_dotenv()

from core.ai_script import generate_long_video_content, CHANNEL_NAME
from core.tts import generate_voiceover
from core.pexels_scraper import download_pexels_b_roll
from core.video_editor import stitch_video
from core.supabase_db import log_video, update_video_upload, cleanup_old_logs
from config import VID_BG_DIR
import random


def create_long_video(topic: str = None, progress_callback=None) -> bool:
    """
    Master function for Ashley MindShift Long-Form Videos (8min+).
    """
    def log(msg):
        print(msg)
        if progress_callback:
            progress_callback(msg)

    # ── 0. DB Cleanup ──────────────────────────
    try:
        cleanup_old_logs(days=7) # Keeping longform logs a bit longer
    except Exception as e:
        print(f"[Cleanup] Failed: {e}")

    # Auto-pick topic if not supplied
    if not topic:
        from core.topic_generator import get_next_topic, get_used_topics_from_db
        used = get_used_topics_from_db()
        log(f"[Topic] Found {len(used)} used topics in DB.")
        topic = get_next_topic(used_topics=used)
        log(f"[Topic] Selected NEW topic: {topic}")

    log(f"\n===========================================")
    log(f"  {CHANNEL_NAME.upper()} LONG-FORM: {topic[:70]}")
    log(f"===========================================\n")

    # ── 1. Generate Long Script & Metadata ───────────────────────────────────
    log("[1/5] Brainstorming Long-Form with Groq...")
    content = generate_long_video_content(topic)
    if not content:
        log("Failed to generate content. Exiting.")
        return False

    log(f"  Title   : {content.get('title')}")
    log(f"  Keywords: {content.get('b_roll_keywords')}")

    # ── 2. Generate Voiceover ───────────────────────────────────────────────
    log("\n[2/5] Recording Long Voiceover with Edge-TTS...")
    # Using a slightly calmer voice for long-form? Let's stick to Christopher for now but maybe less speed reduction
    audio_path, srt_path = generate_voiceover(content.get('script'), filename="long_voiceover.mp3")

    # ── 3. Download Pexels B-Roll ──────────────────────────────────────────
    log("\n[3/5] Downloading Pexels 16:9 B-Roll...")
    # For ~10 minutes, we need roughly 40-50 clips if each is 12-15s.
    # 10 keywords * 5 clips each = 50 clips.
    keywords = content.get('b_roll_keywords', [])
    broll_paths, credits = download_pexels_b_roll(keywords, clips_per_keyword=5, progress_callback=progress_callback)

    if not broll_paths:
        log("Failed to download B-roll. Exiting.")
        return False

    # ── 4. Assemble Video ──────────────────────────────────────────────────
    log("\n[4/5] Assembling Final 16:9 Video...")
    safe_title = re.sub(r'[\\/*?:"<>|#]', "", content.get("title", "video")).strip().replace(" ", "_")
    output_filename = f"{safe_title[:40]}_long_final.mp4"

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
        orientation="landscape",
        bg_music_path=bg_music_path
    )

    if not final_video_path:
        log("\nFAILED to assemble video.")
        return False

    log(f"\nSUCCESS! Video ready: {final_video_path}")

    # Build description
    credits_text = "Background Video Credits (Pexels):\n" + "\n".join([f"  {c}" for c in credits])
    final_desc = content.get('description', '') + f"\n\n{credits_text}"

    # ── 5. DB Logging & Upload ─────────────────────────────────────────────
    log("\n[5/5] Logging & Uploading...")
    # Tags
    video_tags = keywords + ["Dark Psychology", "Shadow Work", "Mindshift", "Human Behavior", "Philosophy"]
    
    db_record = log_video(
        title=content.get('title', ''),
        topic=topic,
        script=content.get('script', ''),
        local_path=final_video_path,
        description=final_desc,
        tags=video_tags,
        status='generated'
    )

    from core.youtube_uploader import get_authenticated_service, upload_video
    youtube_service = get_authenticated_service()
    if youtube_service:
        yt_id = upload_video(
            youtube_service,
            final_video_path,
            content.get('title'),
            final_desc,
            video_tags,
            privacy_status="public"
        )
        if yt_id and db_record:
            update_video_upload(db_record.get('id'), yt_id)
            log(f"Successfully uploaded: {yt_id}")
    else:
        log("YouTube auth not available. Saved locally.")

    # ── 6. Facebook Video Upload ──────────────────────────────────────────
    from core.facebook_uploader import upload_to_facebook_video
    fb_page_id = os.getenv("FACEBOOK_PAGE_ID")
    fb_token   = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")
    if fb_page_id and fb_token:
        log("\n[6/7] Distributing to Facebook Video...")
        upload_to_facebook_video(final_video_path, content.get('title'), fb_page_id, fb_token)
    else:
        log("\n[6/7] Skipping Facebook - Credentials not set.")

    # ── 7. TikTok Upload ──────────────────────────────────────────────────
    from core.tiktok_uploader import upload_to_tiktok
    tt_cookies = os.getenv("TIKTOK_COOKIES_PATH", "tiktok_cookies.txt")
    if os.path.exists(tt_cookies):
        log("\n[7/7] Distributing to TikTok...")
        # Note: TikTok handles up to 10 min videos now.
        upload_to_tiktok(final_video_path, content.get('title'), tt_cookies)
    else:
        log("\n[7/7] Skipping TikTok - Cookies file not found.")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Indigo Insights Long-Form Generator")
    parser.add_argument("--topic", type=str, default=None, help="Override topic")
    args = parser.parse_args()
    create_long_video(topic=args.topic)
