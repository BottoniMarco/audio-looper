from pathlib import Path
import unicodedata
import re
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TMP_DIR = PROJECT_ROOT / "tmp"
DOWNLOADS_DIR = PROJECT_ROOT / "downloads"

def ensure_dirs():
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_tmp_files():
    shutil.rmtree(TMP_DIR)

def sanitize_filename(name: str, max_length: int = 120) -> str:

    # 1. Normalize unicode (é → e, emojis removed)
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")

    # 2. Remove path separators explicitly
    name = name.replace("/", "_").replace("\\", "_")

    # 3. Replace whitespace with underscore
    name = re.sub(r"\s+", "_", name)

    # 4. Remove everything except safe characters
    name = re.sub(r"[^a-zA-Z0-9._-]", "", name)

    # 5. Collapse multiple underscores or dots
    name = re.sub(r"[_\.]{2,}", "_", name)

    # 6. Trim leading/trailing separators
    name = name.strip("._-")

    # 7. Enforce length limit
    if len(name) > max_length:
        name = name[:max_length].rstrip("._-")

    # 8. Fallback if empty
    if not name:
        name = "audio"

    return name