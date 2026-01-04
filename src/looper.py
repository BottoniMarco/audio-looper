import ffmpeg
import inquirer
import os
from pathlib import Path

def loop(input_path: str):

    name = Path(input_path).stem

    questions = [
    inquirer.List('loop',
        message="How long the loop should be (minutes) ",
        choices=['30', '60', '90', '180'],
        ),
    ]
    user_input = inquirer.prompt(questions)
    minutes = int(user_input["loop"])
    TARGET_SECONDS = minutes * 60

    OUTPUT = str(Path("../downloads") / f"{name}_{minutes}m.mp3")

    FADE_IN = 0.1
    FADE_OUT = 0.1

    try:
        (
            ffmpeg
            .input(input_path, stream_loop=-1)
            .output(
                OUTPUT,
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
    except ffmpeg.Error as e:
        print("FFmpeg failed:")
        print(e.stderr.decode() if e.stderr else e)
        return None

    # success path ONLY
    if os.path.isfile(OUTPUT) and os.path.getsize(OUTPUT) > 0:
        os.remove(input_path)
        return OUTPUT
    else:
        print("FFmpeg finished but output file is invalid.")
        return None
