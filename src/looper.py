import ffmpeg
import os
from pathlib import Path
from utils import ensure_dirs,sanitize_filename,cleanup_tmp_files, PROJECT_ROOT, TMP_DIR, DOWNLOADS_DIR

def loop(input_path: str, minutes: int) -> str | None:

    ensure_dirs()
    input_path = str(input_path)
    name = Path(input_path).stem
    TARGET_SECONDS = minutes * 60

    
    final_out = DOWNLOADS_DIR / f"{name}_{minutes}m.mp3"
    part_out = DOWNLOADS_DIR / f"{name}_{minutes}m.part.mp3"

    if part_out.exists():
        part_out.unlink()

    FADE_IN = 0.1
    FADE_OUT = 0.1

    try:
        (
            ffmpeg
            .input(input_path, stream_loop=-1)
            .output(
                str(part_out),
                t=TARGET_SECONDS,
                af=(
                    f"afade=t=in:st=0:d={FADE_IN},"
                    f"afade=t=out:st={TARGET_SECONDS - FADE_OUT}:d={FADE_OUT}"
                ),
                acodec="libmp3lame",
                audio_bitrate="192k"
            )
            .overwrite_output()
            .run()
        )
    except KeyboardInterrupt:
        cleanup_tmp_files()
        if part_out.exists():
            part_out.unlink()
        return None
    except ffmpeg.Error as e:
        print("FFmpeg failed:")
        print(e.stderr.decode() if e.stderr else e)
        if part_out.exists():
            part_out.unlink()
        return None

    if not part_out.exists() or part_out.stat().st_size == 0:
        print("FFmpeg finished but output is invalid.")
        if part_out.exists():
            part_out.unlink()
        return None

    if final_out.exists():
        final_out.unlink()

    part_out.rename(final_out)

    # Only delete input after success
    Path(input_path).unlink(missing_ok=True)

    print("Saved:", final_out)
    return str(final_out)
