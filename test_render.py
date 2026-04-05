from dotenv import load_dotenv
load_dotenv()

from core.ai_script import generate_video_content
from core.tts import generate_voiceover
from core.yt_scraper import download_viral_b_roll
from core.video_editor import stitch_video_remotion
import random

def test():
    topic = "The Power of Silence"
    print(f"Testing with topic: {topic}")
    
    # 1. Generate Content
    content = generate_video_content(topic)
    if not content:
        print("Failed to generate content")
        return

    print(f"Title: {content['title']}")
    print(f"Script: {content['script'][:50]}...")
    
    # 2. Voiceover
    audio_path, srt_path = generate_voiceover(content['script'], filename="test_vo.mp3")
    
    # 3. B-Roll (using existing ones if available or downloading 1)
    keywords = content.get('b_roll_keywords', ["dark anime cinematic"])
    broll_paths, _ = download_viral_b_roll(keywords, clips_per_keyword=1)
    
    if not broll_paths:
        print("No b-roll found")
        return

    # 4. Render
    output_filename = "test_render_final.mp4"
    final_video_path = stitch_video_remotion(
        audio_path=audio_path, 
        broll_paths=broll_paths,
        title=content.get('title', 'SILENCE'),
        output_filename=output_filename,
        srt_path=srt_path
    )
    
    if final_video_path:
        print(f"SUCCESS: Rendered to {final_video_path}")
    else:
        print("FAILED to render")

if __name__ == "__main__":
    test()
