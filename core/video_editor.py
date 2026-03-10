import os
import gc
import subprocess

# --- MONKEY PATCH FOR MOVIEPY PIL DEPENDENCY (Pillow >= 10) ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
# --------------------------------------------------------------

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx
    MOVIEPY_V2 = False
except ImportError:
    from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, vfx
    MOVIEPY_V2 = True

from config import OUTPUT_DIR, TEMP_DIR


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER: get ffmpeg executable (uses imageio_ffmpeg so version is consistent)
# ─────────────────────────────────────────────────────────────────────────────
def _ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"   # fall back to system ffmpeg


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 1: CLIP VALIDATION — filters corrupted clips before they reach assembly
# ─────────────────────────────────────────────────────────────────────────────
def validate_clip(filepath: str) -> bool:
    """
    Validates a downloaded clip file is usable.
    Returns True if valid, False if corrupted/empty/unreadable.
    Prevents 'index 0 is out of bounds for axis 0 with size 0' numpy errors.
    """
    try:
        if not os.path.exists(filepath):
            print(f"[SKIP] File does not exist: {filepath}")
            return False

        # Files under 10 KB are almost certainly corrupted partial downloads
        if os.path.getsize(filepath) < 10000:
            print(f"[SKIP] File too small ({os.path.getsize(filepath)} bytes): {filepath}")
            return False

        clip = VideoFileClip(filepath)

        if clip.duration is None or clip.duration < 0.5:
            print(f"[SKIP] Clip too short or no duration: {filepath}")
            clip.close()
            return False

        if clip.size is None or clip.size[0] < 10 or clip.size[1] < 10:
            print(f"[SKIP] Invalid dimensions: {filepath}")
            clip.close()
            return False

        # Read first frame — catches clips that open but have empty numpy arrays
        try:
            frame = clip.get_frame(0)
            if frame is None or frame.size == 0:
                print(f"[SKIP] Empty frame array: {filepath}")
                clip.close()
                return False
        except Exception as fe:
            print(f"[SKIP] Cannot read frame ({fe}): {filepath}")
            clip.close()
            return False

        clip.close()
        return True

    except Exception as e:
        print(f"[SKIP] Validation failed ({e}): {filepath}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 2: SAFE CLIP LOADING — individual failures don't crash the pipeline
# ─────────────────────────────────────────────────────────────────────────────
def safe_load_clip(filepath: str, target_size: tuple, target_ratio: float):
    """
    Loads a clip without audio, crops to target aspect ratio, resizes.
    Returns None on any error — caller must filter these out.
    """
    try:
        clip = VideoFileClip(filepath).without_audio()

        if clip.duration is None or clip.duration < 0.5:
            clip.close(); return None
        if clip.size is None or clip.size[0] < 10:
            clip.close(); return None

        # Verify first frame is still readable after load
        try:
            frame = clip.get_frame(0)
            if frame is None or frame.size == 0:
                clip.close(); return None
        except Exception:
            clip.close(); return None

        # Crop to correct aspect ratio
        w, h = clip.size
        clip_ratio = w / float(h)
        try:
            if clip_ratio > target_ratio:
                new_w = h * target_ratio
                clip = clip.cropped(x_center=w/2, width=new_w) if MOVIEPY_V2 else clip.crop(x_center=w/2, width=new_w)
            else:
                new_h = w / target_ratio
                clip = clip.cropped(y_center=h/2, height=new_h) if MOVIEPY_V2 else clip.crop(y_center=h/2, height=new_h)
        except Exception as ce:
            print(f"[WARN] Crop failed for {filepath}: {ce}")

        # Resize
        try:
            clip = clip.resized(target_size) if MOVIEPY_V2 else clip.resize(newsize=target_size)
        except Exception as re_:
            print(f"[WARN] Resize failed for {filepath}: {re_}")

        return clip

    except Exception as e:
        print(f"[SKIP] Load failed ({e}): {filepath}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 4: SAFE CONCATENATION — falls back to compose if chain fails
# ─────────────────────────────────────────────────────────────────────────────
def safe_concatenate(clips: list):
    """Concatenates clips using 'chain', falls back to 'compose'. Returns None on total failure."""
    if not clips:
        print("[ERROR] No clips to concatenate"); return None
    if len(clips) == 1:
        return clips[0]

    for method in ("chain", "compose"):
        try:
            print(f"[ASSEMBLY] Concatenating {len(clips)} clips (method: {method})...")
            final = concatenate_videoclips(clips, method=method)
            if final.duration and final.duration >= 1:
                print(f"[ASSEMBLY] Concatenation successful. Duration: {final.duration:.1f}s")
                return final
            print(f"[ERROR] Resulting clip has no duration after {method}")
        except Exception as e:
            print(f"[ERROR] '{method}' concatenation failed: {e}")
            if method == "chain":
                print("[INFO] Retrying with 'compose'...")

    return None


# ─────────────────────────────────────────────────────────────────────────────
#  FIX 7: MEMORY CLEANUP
# ─────────────────────────────────────────────────────────────────────────────
def cleanup_clips(clips: list):
    """Closes clip objects and triggers GC to free memory on the GitHub Actions runner."""
    for c in clips:
        try:
            if c: c.close()
        except Exception:
            pass
    gc.collect()


# ─────────────────────────────────────────────────────────────────────────────
#  AUDIO MIX VIA FFMPEG — bypasses moviepy CompositeAudioClip entirely
# ─────────────────────────────────────────────────────────────────────────────
def _mix_audio_ffmpeg(voice_path: str, music_path: str, output_path: str,
                      total_duration: float, music_vol: float = 0.15) -> bool:
    """
    Mixes voiceover and background music using FFmpeg amix.
    - Voice is at 100% volume.
    - Background music is looped/trimmed to total_duration and reduced to music_vol.
    Returns True on success, False on failure.
    """
    ffmpeg = _ffmpeg()
    try:
        cmd = [
            ffmpeg, "-y",
            "-i", voice_path,
            "-stream_loop", "-1", "-i", music_path,   # loop music indefinitely
            "-filter_complex",
            (
                f"[1:a]volume={music_vol},atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS[bg];"
                "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[out]"
            ),
            "-map", "[out]",
            "-t", f"{total_duration:.3f}",
            "-ac", "2", "-ar", "44100",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except subprocess.CalledProcessError as e:
        print(f"[WARN] FFmpeg audio mix failed: {e.stderr.decode()[:300] if e.stderr else e}")
        return False
    except Exception as e:
        print(f"[WARN] FFmpeg audio mix error: {e}")
        return False


def _mux_video_audio_ffmpeg(video_path: str, audio_path: str, output_path: str) -> bool:
    """
    Muxes a silent video file with an audio file using FFmpeg stream copy (fast, lossless).
    Returns True on success.
    """
    ffmpeg = _ffmpeg()
    try:
        cmd = [
            ffmpeg, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 10000
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg mux failed: {e.stderr.decode()[:300] if e.stderr else e}")
        return False
    except Exception as e:
        print(f"[ERROR] FFmpeg mux error: {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN ASSEMBLY FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def stitch_video(audio_path: str, broll_paths: list, output_filename: str = "final_short.mp4",
                 srt_path: str = None, orientation: str = "portrait", bg_music_path: str = None):
    """
    Stitches B-roll clips for Ashley MindShift.
    Audio is handled entirely by FFmpeg to avoid moviepy CompositeAudioClip bugs on Linux.
    Memory-optimised for 50-clip long-form videos on GitHub Actions (2-core runner).
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

    # Temp file paths used during pipeline
    silent_video_path = os.path.join(TEMP_DIR, "temp_silent.mp4")
    mixed_audio_path  = os.path.join(TEMP_DIR, "temp_mixed_audio.aac")
    temp_no_sub       = os.path.join(TEMP_DIR, "temp_assembly.mp4")
    output_path       = os.path.join(OUTPUT_DIR, output_filename)

    loaded_clips    = []
    processed_clips = []
    final_video     = None

    try:
        # ── 1. Validate Voiceover ──────────────────────────────────────────
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 1000:
            print(f"[CRITICAL] Voiceover file missing or empty: {audio_path}")
            return None

        # Read voiceover duration via moviepy (lightweight — just reads header)
        vo_clip = AudioFileClip(audio_path)
        total_duration = vo_clip.duration
        vo_clip.close()
        print(f"[ASSEMBLY] Target duration: {total_duration:.1f}s")

        # ── 2. FIX 1: Validate all clips before loading ────────────────────
        print(f"\nValidating {len(broll_paths)} clips...")
        valid_paths = [p for p in broll_paths if validate_clip(p)]
        print(f"[ASSEMBLY] Clips passed validation: {len(valid_paths)}/{len(broll_paths)}")
        gc.collect()   # free validation overhead

        if not valid_paths:
            print(
                f"[ASSEMBLY FAILED] No valid clips.\n"
                f"  Received: {len(broll_paths)} | Passed: 0\n"
                f"  Duration: {total_duration:.1f}s"
            )
            return None

        if len(valid_paths) < 5:
            print(f"[WARNING] Only {len(valid_paths)} valid clips — video may be short.")

        # ── 3. FIX 2: Safe clip loading ────────────────────────────────────
        print(f"\nLoading {len(valid_paths)} validated clips...")
        for path in valid_paths:
            loaded_clips.append(safe_load_clip(path, target_size, target_ratio))

        # FIX 3: filter out None
        valid_clips = [c for c in loaded_clips if c is not None]
        print(f"[ASSEMBLY] Clips successfully loaded: {len(valid_clips)}/{len(loaded_clips)}")
        gc.collect()

        if not valid_clips:
            print("[ASSEMBLY FAILED] All clips failed during loading.")
            return None

        # ── 4. Trim clips to fill target duration ──────────────────────────
        current_time = 0
        print(f"\nTrimming clips to fit {total_duration:.1f}s...")

        for clip in valid_clips:
            if current_time >= total_duration:
                clip.close(); continue
            remaining = total_duration - current_time
            try:
                if clip.duration > remaining:
                    clip = clip.subclipped(0, remaining) if MOVIEPY_V2 else clip.subclip(0, remaining)
                processed_clips.append(clip)
                current_time += clip.duration
            except Exception as te:
                print(f"[WARN] Trim failed: {te}")
                try: clip.close()
                except Exception: pass

        print(f"[ASSEMBLY] Trimmed clips ready: {len(processed_clips)} | Covered: {current_time:.1f}s / {total_duration:.1f}s")

        if not processed_clips:
            print("[CRITICAL] No clips after trimming. Aborting.")
            return None

        # ── 5. FIX 4: Safe concatenation ──────────────────────────────────
        final_video = safe_concatenate(processed_clips)
        if final_video is None:
            print(f"[ASSEMBLY FAILED] Concatenation returned nothing. Clips: {len(processed_clips)}")
            return None

        # ── 6. Render SILENT video (moviepy writes only video stream) ──────
        # This avoids the MoviePy CompositeAudioClip numpy bug entirely.
        # All audio work is done by FFmpeg in the next steps.
        print(f"[ASSEMBLY] Rendering silent video (Preset: medium, Threads: 2)...")
        print(f"[ASSEMBLY] Final video duration: {final_video.duration:.1f}s")

        final_video.write_videofile(
            silent_video_path,
            fps=24,
            codec="libx264",
            audio=False,                # NO AUDIO — FFmpeg handles it
            temp_audiofile=os.path.join(TEMP_DIR, "temp-audio.m4a"),
            remove_temp=True,
            threads=2,
            preset="medium",
            logger=None
        )

        # Release video clips from memory now that render is done
        cleanup_clips(processed_clips)
        processed_clips = []
        if final_video:
            final_video.close()
            final_video = None
        gc.collect()

        if not os.path.exists(silent_video_path) or os.path.getsize(silent_video_path) < 10000:
            print("[CRITICAL] Silent video render produced no output.")
            return None
        print(f"[ASSEMBLY] Silent video rendered: {silent_video_path}")

        # ── 7. Mix audio entirely with FFmpeg ─────────────────────────────
        # Completely bypasses MoviePy audio — no more CompositeAudioClip crashes
        if bg_music_path and os.path.exists(bg_music_path):
            print(f"[ASSEMBLY] Mixing audio with FFmpeg (voice 100% + music 15%)...")
            mix_ok = _mix_audio_ffmpeg(audio_path, bg_music_path, mixed_audio_path, total_duration)
            final_audio_path = mixed_audio_path if mix_ok else audio_path
            if not mix_ok:
                print("[WARN] Audio mix failed — using voiceover only.")
        else:
            final_audio_path = audio_path
            print("[ASSEMBLY] No BG music — using voiceover only.")

        # ── 8. Mux video + audio via FFmpeg ───────────────────────────────
        mux_target = temp_no_sub if srt_path else output_path
        print(f"[ASSEMBLY] Muxing video + audio...")
        mux_ok = _mux_video_audio_ffmpeg(silent_video_path, final_audio_path, mux_target)

        if not mux_ok:
            print("[CRITICAL] FFmpeg mux failed. Aborting.")
            return None

        # ── 9. Optional Subtitles (FFmpeg burn-in) ─────────────────────────
        if srt_path and os.path.exists(srt_path):
            print("Burning subtitles with FFmpeg...")
            srt_abs = os.path.abspath(srt_path).replace('\\', '/')
            if ":" in srt_abs:
                srt_abs = srt_abs.replace(":", "\\:")

            style = (
                "FontName=Arial,FontSize=28,PrimaryColour=&HFFFFFF&,"
                "OutlineColour=&H000000&,Outline=2,Alignment=10,Bold=1"
            )
            cmd = [
                _ffmpeg(), "-y", "-i", temp_no_sub,
                "-vf", f"subtitles='{srt_abs}':force_style='{style}'",
                "-c:a", "copy", output_path
            ]
            subprocess.run(cmd, check=True)
            if os.path.exists(temp_no_sub):
                os.remove(temp_no_sub)

        # Clean up temp files
        for tmp in (silent_video_path, mixed_audio_path):
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass

        print(f"[ASSEMBLY] Video assembly complete: {output_path}")
        return output_path

    except Exception as e:
        print(f"CRITICAL ERROR in assembly: {e}")
        print(f"[DEBUG] broll_paths count: {len(broll_paths)}")
        print(f"[DEBUG] loaded_clips count: {len(loaded_clips)}")
        print(f"[DEBUG] processed_clips count: {len(processed_clips)}")
        return None

    finally:
        # MASTER CLEANUP — prevents memory leaks and OOM kills on GitHub Actions
        print("Releasing media handles...")
        try:
            cleanup_clips(processed_clips)
            if final_video:
                final_video.close()
        except Exception as ce:
            print(f"Cleanup warning: {ce}")
        gc.collect()
