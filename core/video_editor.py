import os
import gc
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


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 1 & 6: CLIP VALIDATION — catches corrupted/empty clips before assembly
# ─────────────────────────────────────────────────────────────────────────────
def validate_clip(filepath: str) -> bool:
    """
    Validates that a downloaded video clip is usable before loading it for assembly.
    Returns True if clip is valid, False if corrupted/empty/unreadable.
    Prevents 'index 0 is out of bounds for axis 0 with size 0' numpy errors.
    """
    try:
        # Check file exists
        if not os.path.exists(filepath):
            print(f"[SKIP] File does not exist: {filepath}")
            return False

        # Check file size — anything under 10KB is almost certainly corrupted
        file_size = os.path.getsize(filepath)
        if file_size < 10000:
            print(f"[SKIP] File too small ({file_size} bytes): {filepath}")
            return False

        # Try to load and inspect the clip
        test_clip = VideoFileClip(filepath)

        # Check duration
        if test_clip.duration is None or test_clip.duration < 0.5:
            print(f"[SKIP] Clip too short or no duration: {filepath}")
            test_clip.close()
            return False

        # Check dimensions
        if test_clip.size is None or test_clip.size[0] < 10 or test_clip.size[1] < 10:
            print(f"[SKIP] Clip has invalid dimensions: {filepath}")
            test_clip.close()
            return False

        # Try to read the first frame — this is the key check that catches
        # moviepy clips that "open" but have an empty internal numpy frame array
        try:
            frame = test_clip.get_frame(0)
            if frame is None or frame.size == 0:
                print(f"[SKIP] Clip has empty frames: {filepath}")
                test_clip.close()
                return False
        except Exception as frame_err:
            print(f"[SKIP] Cannot read frames from clip ({frame_err}): {filepath}")
            test_clip.close()
            return False

        test_clip.close()
        return True

    except Exception as e:
        print(f"[SKIP] Clip validation failed ({e}): {filepath}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 2: SAFE CLIP LOADING — individual clip failures don't kill the pipeline
# ─────────────────────────────────────────────────────────────────────────────
def safe_load_clip(filepath: str, target_size: tuple, target_ratio: float) -> VideoFileClip | None:
    """
    Safely loads, crops, and resizes a video clip with full error handling.
    Returns None if the clip cannot be loaded or processed — caller must filter these out.
    """
    try:
        clip = VideoFileClip(filepath).without_audio()

        # Re-check duration after load (some clips pass validation but lose duration)
        if clip.duration is None or clip.duration < 0.5:
            print(f"[SKIP] Loaded clip has no duration: {filepath}")
            clip.close()
            return None

        if clip.size is None or clip.size[0] < 10 or clip.size[1] < 10:
            print(f"[SKIP] Loaded clip has invalid size: {filepath}")
            clip.close()
            return None

        # Verify first frame is readable
        try:
            frame = clip.get_frame(0)
            if frame is None or frame.size == 0:
                print(f"[SKIP] Loaded clip has empty first frame: {filepath}")
                clip.close()
                return None
        except Exception:
            print(f"[SKIP] Cannot read frame from: {filepath}")
            clip.close()
            return None

        # Crop to target aspect ratio
        w, h = clip.size
        clip_ratio = w / float(h)

        try:
            if clip_ratio > target_ratio:
                new_w = h * target_ratio
                if MOVIEPY_V2:
                    clip = clip.cropped(x_center=w / 2, width=new_w)
                else:
                    clip = clip.crop(x_center=w / 2, width=new_w)
            else:
                new_h = w / target_ratio
                if MOVIEPY_V2:
                    clip = clip.cropped(y_center=h / 2, height=new_h)
                else:
                    clip = clip.crop(y_center=h / 2, height=new_h)
        except Exception as crop_err:
            print(f"[WARN] Crop failed for {filepath}: {crop_err}")

        # Resize to target resolution
        try:
            if MOVIEPY_V2:
                clip = clip.resized(target_size)
            else:
                clip = clip.resize(newsize=target_size)
        except Exception as resize_err:
            print(f"[WARN] Resize failed for {filepath}, using cropped size: {resize_err}")

        return clip

    except Exception as e:
        print(f"[SKIP] Failed to load clip ({e}): {filepath}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 4: SAFE CONCATENATION — falls back to compose method if chain fails
# ─────────────────────────────────────────────────────────────────────────────
def safe_concatenate(clips: list) -> VideoFileClip | None:
    """
    Safely concatenates a list of video clips.
    Tries 'chain' method first, falls back to 'compose' if it fails.
    Returns None if both methods fail.
    """
    if not clips:
        print("[ERROR] No clips to concatenate")
        return None

    if len(clips) == 1:
        print("[INFO] Only one clip, skipping concatenation")
        return clips[0]

    # Primary attempt: 'chain' is memory-efficient for long-form video
    try:
        print(f"[ASSEMBLY] Concatenating {len(clips)} clips (method: chain)...")
        final = concatenate_videoclips(clips, method="chain")

        if final.duration is None or final.duration < 1:
            print("[ERROR] Concatenated video has no duration")
            return None

        print(f"[ASSEMBLY] Concatenation successful. Duration: {final.duration:.1f}s")
        return final

    except Exception as e:
        print(f"[ERROR] 'chain' concatenation failed: {e}")

    # Fallback: 'compose' is slower but more compatible
    try:
        print("[INFO] Retrying concatenation with 'compose' method...")
        final = concatenate_videoclips(clips, method="compose")

        if final.duration is None or final.duration < 1:
            print("[ERROR] Compose concatenated video has no duration")
            return None

        print(f"[ASSEMBLY] Compose concatenation successful. Duration: {final.duration:.1f}s")
        return final

    except Exception as e2:
        print(f"[ERROR] 'compose' concatenation also failed: {e2}")

    return None


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 5: SAFE AUDIO LOADING — prevents empty audio arrays crashing the render
# ─────────────────────────────────────────────────────────────────────────────
def safe_load_audio(filepath: str) -> AudioFileClip | None:
    """
    Safely loads an audio file with size and duration validation.
    Returns None if the file is missing, empty, or unreadable.
    """
    try:
        if not os.path.exists(filepath):
            print(f"[WARN] Audio file not found: {filepath}")
            return None

        file_size = os.path.getsize(filepath)
        if file_size < 1000:
            print(f"[WARN] Audio file too small ({file_size} bytes): {filepath}")
            return None

        audio = AudioFileClip(filepath)

        if audio.duration is None or audio.duration < 1:
            print(f"[WARN] Audio has no duration: {filepath}")
            audio.close()
            return None

        return audio

    except Exception as e:
        print(f"[WARN] Failed to load audio ({e}): {filepath}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 7: MEMORY CLEANUP HELPER
# ─────────────────────────────────────────────────────────────────────────────
def cleanup_clips(clips: list):
    """Properly closes clip objects and triggers garbage collection to free memory on GitHub Actions runner."""
    for clip in clips:
        try:
            if clip is not None:
                clip.close()
        except Exception:
            pass
    gc.collect()


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN ASSEMBLY FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def stitch_video(audio_path: str, broll_paths: list, output_filename: str = "final_short.mp4",
                 srt_path: str = None, orientation: str = "portrait", bg_music_path: str = None):
    """
    Stitches B-roll for Ashley MindShift with specific styling.
    Memory-optimized for long-form video (8-10 mins).
    All clips are validated and safely loaded — corrupted clips are skipped gracefully.
    """
    print(f"Starting video assembly ({orientation})...")
    print(f"[ASSEMBLY] Total clip files received: {len(broll_paths)}")

    if orientation == "landscape":
        target_size  = (1920, 1080)
        target_ratio = 1920 / 1080.0
    else:
        target_size  = (1080, 1920)
        target_ratio = 1080 / 1920.0

    print(f"[ASSEMBLY] Target resolution: {target_size[0]}x{target_size[1]}")

    # Track objects for cleanup
    audio       = None
    bg_music    = None
    final_audio = None
    loaded_clips       = []   # clips that passed safe_load_clip
    processed_clips    = []   # clips trimmed to fit remaining duration
    final_video = None

    try:
        # ── 1. Load & Validate Voiceover Audio ────────────────────────────
        print("Loading audio...")
        audio = safe_load_audio(audio_path)
        if audio is None:
            print("[CRITICAL] Voiceover audio could not be loaded. Aborting assembly.")
            return None

        total_duration = audio.duration
        print(f"[ASSEMBLY] Target duration: {total_duration:.1f}s")

        # ── 2. Load & Mix Background Music ────────────────────────────────
        if bg_music_path and os.path.exists(bg_music_path):
            print(f"Mixing background music: {bg_music_path}")
            bg_music = safe_load_audio(bg_music_path)

            if bg_music:
                # Loop or trim bg music to match voiceover length
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

                # Volume mix: 15% background, 100% voice
                if MOVIEPY_V2:
                    bg_music = bg_music.with_volume_scaled(0.15)
                    audio    = audio.with_volume_scaled(1.0)
                else:
                    bg_music = bg_music.volumex(0.15)
                    audio    = audio.volumex(1.0)

                final_audio = CompositeAudioClip([audio, bg_music])
            else:
                print("[WARN] Background music failed to load — using voiceover only.")
                final_audio = audio
        else:
            final_audio = audio

        # ── 3. FIX 1: VALIDATE ALL CLIPS BEFORE LOADING ───────────────────
        print(f"\nValidating {len(broll_paths)} clips...")
        valid_paths = [p for p in broll_paths if validate_clip(p)]
        print(f"[ASSEMBLY] Clips passed validation: {len(valid_paths)}/{len(broll_paths)}")

        # FIX 7: free memory after validation pass
        gc.collect()

        # FIX 8: graceful failure if no clips survived validation
        if len(valid_paths) == 0:
            error_msg = (
                f"[ASSEMBLY FAILED] No valid clips available for assembly.\n"
                f"  Total clips received: {len(broll_paths)}\n"
                f"  Clips passed validation: 0\n"
                f"  Target duration: {total_duration:.1f}s\n"
                f"  Check if Pexels clips are actually being downloaded correctly."
            )
            print(error_msg)
            return None

        if len(valid_paths) < 5:
            print(f"[WARNING] Only {len(valid_paths)} valid clips. Video may be shorter than expected.")

        # ── 4. FIX 2: SAFE CLIP LOADING ────────────────────────────────────
        print(f"\nLoading {len(valid_paths)} validated clips...")
        for path in valid_paths:
            clip = safe_load_clip(path, target_size, target_ratio)
            loaded_clips.append(clip)   # keep None entries temporarily for count logging

        # FIX 3: FILTER OUT NONE CLIPS BEFORE CONCATENATION
        valid_clips = [c for c in loaded_clips if c is not None]
        print(f"[ASSEMBLY] Clips successfully loaded: {len(valid_clips)}/{len(loaded_clips)}")

        if len(valid_clips) == 0:
            error_msg = (
                f"[ASSEMBLY FAILED] All clips failed during loading.\n"
                f"  Clips passed validation: {len(valid_paths)}\n"
                f"  Clips successfully loaded: 0"
            )
            print(error_msg)
            return None

        # gc after loading
        gc.collect()

        # ── 5. Trim Clips to Fit Target Duration ───────────────────────────
        current_time = 0
        print(f"\nTrimming clips to fit {total_duration:.1f}s...")

        for clip in valid_clips:
            if current_time >= total_duration:
                clip.close()
                continue

            remaining = total_duration - current_time
            try:
                if clip.duration > remaining:
                    if MOVIEPY_V2:
                        clip = clip.subclipped(0, remaining)
                    else:
                        clip = clip.subclip(0, remaining)

                processed_clips.append(clip)
                current_time += clip.duration
            except Exception as trim_err:
                print(f"[WARN] Clip trim failed: {trim_err}")
                try:
                    clip.close()
                except Exception:
                    pass
                continue

        print(f"[ASSEMBLY] Trimmed clips ready: {len(processed_clips)} | Covered: {current_time:.1f}s / {total_duration:.1f}s")

        if not processed_clips:
            print("[CRITICAL] No processable clips after trimming. Aborting.")
            return None

        # ── 6. FIX 4: SAFE CONCATENATION ─────────────────────────────────
        final_video = safe_concatenate(processed_clips)

        if final_video is None:
            error_msg = (
                f"[ASSEMBLY FAILED] Concatenation returned no output.\n"
                f"  Clips processed: {len(processed_clips)}\n"
                f"  Duration covered: {current_time:.1f}s"
            )
            print(error_msg)
            return None

        # Attach audio
        if MOVIEPY_V2:
            final_video = final_video.with_audio(final_audio)
        else:
            final_video = final_video.set_audio(final_audio)

        output_path  = os.path.join(OUTPUT_DIR, output_filename)
        temp_no_sub  = os.path.join(TEMP_DIR, "temp_assembly.mp4")
        render_target = temp_no_sub if srt_path else output_path

        # ── 7. Render ──────────────────────────────────────────────────────
        print(f"[ASSEMBLY] Starting render...")
        print(f"[ASSEMBLY] Preset: medium, Threads: 2")
        print(f"[ASSEMBLY] Final video duration: {final_video.duration:.1f}s")

        final_video.write_videofile(
            render_target,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile=os.path.join(TEMP_DIR, "temp-audio.m4a"),
            remove_temp=True,
            threads=2,
            preset="medium",
            logger=None
        )

        # FIX 7: release clip memory after render is complete
        cleanup_clips(processed_clips)
        processed_clips = []
        gc.collect()

        # ── 8. Optional Subtitles (FFmpeg — faster/lighter than MoviePy) ──
        if srt_path and os.path.exists(srt_path):
            print("Burning high-end subtitles with FFmpeg...")
            srt_abs = os.path.abspath(srt_path).replace('\\', '/')
            if ":" in srt_abs:
                srt_abs = srt_abs.replace(":", "\\:")

            style = (
                "FontName=Arial,FontSize=28,PrimaryColour=&HFFFFFF&,"
                "OutlineColour=&H000000&,Outline=2,Alignment=10,Bold=1"
            )

            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

            cmd = [
                ffmpeg_exe, "-y", "-i", temp_no_sub,
                "-vf", f"subtitles='{srt_abs}':force_style='{style}'",
                "-c:a", "copy",
                output_path
            ]
            subprocess.run(cmd, check=True)
            if os.path.exists(temp_no_sub):
                os.remove(temp_no_sub)

        print(f"[ASSEMBLY] Video assembly complete: {output_path}")
        return output_path

    except Exception as e:
        print(f"CRITICAL ERROR in assembly: {e}")
        # FIX 8: print diagnostic info to help debug GitHub Actions logs
        print(f"[DEBUG] broll_paths count: {len(broll_paths)}")
        print(f"[DEBUG] loaded_clips count: {len(loaded_clips)}")
        print(f"[DEBUG] processed_clips count: {len(processed_clips)}")
        return None

    finally:
        # MASTER CLEANUP: prevents memory leaks and signal-143 OOM kills
        print("Releasing media handles...")
        try:
            cleanup_clips(processed_clips)
            if final_video:
                final_video.close()
            if audio:
                audio.close()
            if bg_music:
                bg_music.close()
            if final_audio:
                final_audio.close()
            gc.collect()
        except Exception as cleanup_err:
            print(f"Cleanup warning: {cleanup_err}")
