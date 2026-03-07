import os
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx
from config import OUTPUT_DIR, TEMP_DIR

def stitch_video(audio_path: str, broll_paths: list, output_filename: str = "final_short.mp4", srt_path: str = None):
    """
    Stitches B-roll for Indigo Insights with specific styling.
    """
    print("Starting video assembly...")
    
    if not os.path.exists(audio_path):
        print(f"Error: Audio file {audio_path} not found.")
        return None
        
    if not broll_paths:
        print("Error: No B-roll files provided.")
        return None

    try:
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        
        num_clips = len(broll_paths)
        clip_duration = total_duration / num_clips
        
        processed_clips = []
        for path in broll_paths:
            if not os.path.exists(path):
                continue
                
            clip = VideoFileClip(path)
            
            if clip.duration < clip_duration:
                clip = clip.fx(vfx.loop, duration=clip_duration)
            else:
                clip = clip.subclip(0, clip_duration)
                
            w, h = clip.size
            target_ratio = 1080 / 1920.0
            clip_ratio = w / float(h)
            
            if clip_ratio > target_ratio:
                new_w = h * target_ratio
                clip = clip.crop(x_center=w/2, width=new_w)
            else:
                new_h = w / target_ratio
                clip = clip.crop(y_center=h/2, height=new_h)
                
            clip = clip.resize(newsize=(1080, 1920))
            processed_clips.append(clip)
            
        if not processed_clips:
            return None
            
        print("Concatenating video clips...")
        final_video = concatenate_videoclips(processed_clips, method="compose")
        
        print("Adding voiceover...")
        final_video = final_video.set_audio(audio)
        
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        if srt_path and os.path.exists(srt_path):
            temp_output = os.path.join(TEMP_DIR, "temp_no_subs.mp4")
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

            # Indigo Insights Style: White Text, Cyan Outline (Glow effect), Mid-Center, Bold
            # Primary: White (&HFFFFFF), Outline: Cyan (&HFFFF00)
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
        return None
