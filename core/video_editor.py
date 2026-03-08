import os
import subprocess

# --- MONKEY PATCH FOR MOVIEPY PIL DEPENDENCY (Pillow >= 10) ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
# --------------------------------------------------------------

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx, CompositeAudioClip
    MOVIEPY_V2 = False
except ImportError:
    from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx, CompositeAudioClip
    MOVIEPY_V2 = True

from config import OUTPUT_DIR, TEMP_DIR

def stitch_video(audio_path: str, broll_paths: list, output_filename: str = "final_short.mp4", srt_path: str = None, orientation: str = "portrait", bg_music_path: str = None):
    """
    Stitches B-roll for Ashley MindShift with specific styling.
    Memory-optimized for long-form video (8-10 mins).
    """
    print(f"Starting video assembly ({orientation})...")
    
    if orientation == "landscape":
        target_size = (1920, 1080)
        target_ratio = 1920 / 1080.0
    else:
        target_size = (1080, 1920)
        target_ratio = 1080 / 1920.0

    # Initialize variables for cleanup
    audio = None
    bg_music = None
    final_audio = None
    processed_clips = []
    final_video = None

    try:
        # 1. Prepare Audio Mix
        print("Loading audio...")
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        
        if bg_music_path and os.path.exists(bg_music_path):
            print(f"Mixing background music: {bg_music_path}")
            bg_music = AudioFileClip(bg_music_path)
            
            # Loop bg music
            if bg_music.duration < total_duration:
                if MOVIEPY_V2:
                    bg_music = bg_music.with_effects([vfx.Loop(duration=total_duration)])
                else:
                    bg_music = bg_music.fx(vfx.loop, duration=total_duration)
            else:
                if MOVIEPY_V2:
                    bg_music = bg_music.subclipped(0, total_duration)
                else:
                    bg_music = bg_music.subclip(0, total_duration)
            
            # Volume Mix (15% background, 100% voice)
            if MOVIEPY_V2:
                bg_music = bg_music.with_volume_scaled(0.15) 
                audio = audio.with_volume_scaled(1.0)
            else:
                bg_music = bg_music.volumex(0.15)
                audio = audio.volumex(1.0)
            
            final_audio = CompositeAudioClip([audio, bg_music])
        else:
            final_audio = audio

        # 2. Process Video Clips
        current_time = 0
        print(f"Processing {len(broll_paths)} clips for {total_duration:.1f}s...")
        
        for path in broll_paths:
            if current_time >= total_duration:
                break
            
            try:
                clip = VideoFileClip(path).without_audio()
                
                # Truncate if over
                remaining = total_duration - current_time
                if clip.duration > remaining:
                    if MOVIEPY_V2: clip = clip.subclipped(0, remaining)
                    else: clip = clip.subclip(0, remaining)
                
                # Resize and Crop
                w, h = clip.size
                clip_ratio = w / float(h)
                
                if clip_ratio > target_ratio:
                    new_w = h * target_ratio
                    if MOVIEPY_V2: clip = clip.cropped(x_center=w/2, width=new_w)
                    else: clip = clip.crop(x_center=w/2, width=new_w)
                else:
                    new_h = w / target_ratio
                    if MOVIEPY_V2: clip = clip.cropped(y_center=h/2, height=new_h)
                    else: clip = clip.crop(y_center=h/2, height=new_h)
                    
                if MOVIEPY_V2: clip = clip.resized(target_size)
                else: clip = clip.resize(newsize=target_size)
                
                processed_clips.append(clip)
                current_time += clip.duration
            except Exception as clip_err:
                print(f"Warning: Skipping {path}: {clip_err}")
                continue
            
        if not processed_clips:
            print("Error: No valid clips processed.")
            return None
            
        # 3. Assemble Final Video
        print("Concatenating clips (Memory-efficient 'chain' method)...")
        final_video = concatenate_videoclips(processed_clips, method="chain")
        
        if MOVIEPY_V2: final_video = final_video.with_audio(final_audio)
        else: final_video = final_video.set_audio(final_audio)
        
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        temp_no_sub_path = os.path.join(TEMP_DIR, "temp_assembly.mp4")
        
        # 4. Render
        print(f"Rendering (Preset: medium, Threads: 2)...")
        final_video.write_videofile(
            temp_no_sub_path if srt_path else output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile=os.path.join(TEMP_DIR, "temp-audio.m4a"),
            remove_temp=True,
            threads=2,
            preset="medium",
            logger=None
        )
        
        # 5. Optional Subtitles (FFmpeg is much faster/lighter than MoviePy for this)
        if srt_path and os.path.exists(srt_path):
            print("Burning high-end subtitles with FFmpeg...")
            srt_abs = os.path.abspath(srt_path).replace('\\', '/')
            # Special formatting for FFmpeg subtitles filter on Windows
            if ":" in srt_abs:
                srt_abs = srt_abs.replace(":", "\\:")
            
            style = "FontName=Arial,FontSize=28,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=2,Alignment=10,Bold=1"
            
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            
            cmd = [
                ffmpeg_exe, "-y", "-i", temp_no_sub_path,
                "-vf", f"subtitles='{srt_abs}':force_style='{style}'",
                "-c:a", "copy",
                output_path
            ]
            subprocess.run(cmd, check=True)
            if os.path.exists(temp_no_sub_path): os.remove(temp_no_sub_path)

        print(f"Video assembly complete: {output_path}")
        return output_path

    except Exception as e:
        print(f"CRITICAL ERROR in assembly: {e}")
        return None
    finally:
        # MASTER CLEANUP: Essential to prevent Memory Leaks and 143 Errors
        print("Releasing media handles...")
        try:
            if processed_clips:
                for c in processed_clips: 
                    try: c.close()
                    except: pass
            if final_video: final_video.close()
            if audio: audio.close()
            if bg_music: bg_music.close()
            if final_audio: final_audio.close()
        except Exception as cleanup_err:
            print(f"Cleanup warning: {cleanup_err}")
