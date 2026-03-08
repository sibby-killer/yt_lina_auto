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
    orientation: "portrait" (1080x1920) or "landscape" (1920x1080)
    bg_music_path: Optional path to background music file.
    """
    print(f"Starting video assembly ({orientation})...")
    
    if orientation == "landscape":
        target_size = (1920, 1080)
        target_ratio = 1920 / 1080.0
    else:
        target_size = (1080, 1920)
        target_ratio = 1080 / 1920.0

    if not os.path.exists(audio_path):
        print(f"Error: Audio file {audio_path} not found.")
        return None
        
    if not broll_paths:
        print("Error: No B-roll files provided.")
        return None

    try:
        # Load Voiceover
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        
        # Determine background music mix
        if bg_music_path and os.path.exists(bg_music_path):
            print(f"Mixing background music: {bg_music_path}")
            bg_music = AudioFileClip(bg_music_path)
            
            # Loop bg music if shorter than voiceover
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
            
            # Adjust volume (bg music low, voiceover clear)
            if MOVIEPY_V2:
                bg_music = bg_music.with_volume_scaled(0.15) # 15% volume
                audio = audio.with_volume_scaled(1.0)
            else:
                bg_music = bg_music.volumex(0.15)
                audio = audio.volumex(1.0)
                
            final_audio = CompositeAudioClip([audio, bg_music])
        else:
            final_audio = audio
            
        num_clips = len(broll_paths)
        clip_duration = total_duration / num_clips
        
        processed_clips = []
        for path in broll_paths:
            if not os.path.exists(path):
                continue
            
            try:
                clip = VideoFileClip(path)
                
                # Duration handling
                if clip.duration < clip_duration:
                    if MOVIEPY_V2:
                        clip = clip.with_effects([vfx.Loop(duration=clip_duration)])
                    else:
                        clip = clip.fx(vfx.loop, duration=clip_duration)
                else:
                    if MOVIEPY_V2:
                        clip = clip.subclipped(0, clip_duration) # Correct v2 subclip
                    else:
                        clip = clip.subclip(0, clip_duration)
                    
                w, h = clip.size
                clip_ratio = w / float(h)
                
                if clip_ratio > target_ratio:
                    new_w = h * target_ratio
                    if MOVIEPY_V2:
                        clip = clip.cropped(x_center=w/2, width=new_w)
                    else:
                        clip = clip.crop(x_center=w/2, width=new_w)
                else:
                    new_h = w / target_ratio
                    if MOVIEPY_V2:
                        clip = clip.cropped(y_center=h/2, height=new_h)
                    else:
                        clip = clip.crop(y_center=h/2, height=new_h)
                    
                if MOVIEPY_V2:
                    clip = clip.resized(target_size)
                else:
                    clip = clip.resize(newsize=target_size)
                processed_clips.append(clip)
            except Exception as clip_err:
                print(f"Warning: Skipping corrupted B-roll clip {path}: {clip_err}")
                continue
            
        if not processed_clips:
            if audio: audio.close()
            if 'bg_music' in locals(): bg_music.close()
            return None
            
        print("Concatenating video clips...")
        final_video = concatenate_videoclips(processed_clips, method="compose")
        
        print("Adding audio mix...")
        if MOVIEPY_V2:
            final_video = final_video.with_audio(final_audio)
        else:
            final_video = final_video.set_audio(final_audio)
        
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        if srt_path and os.path.exists(srt_path):
            temp_output = os.path.join(TEMP_DIR, "temp_no_subs.mp4")
            # write_videofile has some changed params in v2 but logger=None and threads=1 are safe
            final_video.write_videofile(
                temp_output,
                fps=30,
                codec="libx264",
                audio_codec="aac",
                preset="ultrafast",
                threads=1,
                logger=None
            )
            
            print("Burning dynamic CYAN subtitles using FFmpeg...")
            srt_abs = os.path.abspath(srt_path)
            if len(srt_abs) >= 2 and srt_abs[1] == ':':
                drive   = srt_abs[0]
                rest    = srt_abs[2:].replace('\\', '/')
                ffmpeg_srt_path = f"{drive}\\\\:{rest}"
            else:
                ffmpeg_srt_path = srt_abs.replace('\\', '/')

            style = "FontName=Arial,FontSize=28,PrimaryColour=&HFFFFFF&,OutlineColour=&HFFFF00&,Outline=3,Alignment=10,Bold=1"
            
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            
            ffmpeg_cmd = [
                ffmpeg_exe, "-y",
                "-i", temp_output,
                "-vf", f"subtitles={ffmpeg_srt_path}:force_style='{style}'",
                "-c:a", "copy",
                output_path
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            
            if os.path.exists(temp_output):
                try: os.remove(temp_output)
                except: pass
        else:
            final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", preset="ultrafast", threads=1, logger=None)
        
        # Cleanup
        for clip in processed_clips: clip.close()
        audio.close()
        final_video.close()
        
        return output_path

    except Exception as e:
        print(f"Error during video editing: {e}")
        # Ensure cleanup on fail
        try:
            if 'audio' in locals(): audio.close()
            if 'processed_clips' in locals(): 
                for c in processed_clips: c.close()
            if 'final_video' in locals(): final_video.close()
        except: pass
        return None

