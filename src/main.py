from downloader import download_audio
from looper import loop
from pathlib import Path
from utils import ensure_dirs,sanitize_filename, PROJECT_ROOT, TMP_DIR, DOWNLOADS_DIR
import inquirer

def main():
    ensure_dirs()

    link = input("Insert URL: ").strip()
    if not link:
        print("Empty URL.")
        return

    questions = [
        inquirer.List(
            "minutes",
            message="How long should the loop be (minutes)?",
            choices=["30", "60", "90", "180"],
        )
    ]
    answers = inquirer.prompt(questions)
    if not answers:
        print("Cancelled.")
        return

    minutes = int(answers["minutes"])

    raw_path = download_audio(link)
    if not raw_path:
        return

    output = loop(raw_path, minutes)
    if output:
        print("Saved:", output)

if __name__ == "__main__":
    main()

