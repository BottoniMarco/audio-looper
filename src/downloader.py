import yt_dlp
import os
from pathlib import Path
from looper import loop
from utils import ensure_dirs,sanitize_filename,cleanup_tmp_files,PROJECT_ROOT, TMP_DIR, DOWNLOADS_DIR

def download_audio(link: str) -> str | None:
  ensure_dirs()

  tmp_base = TMP_DIR / "raw_audio"
  tmp_part = TMP_DIR / "raw_audio.part"
  tmp_final = TMP_DIR / "raw_audio.download" 

  if tmp_part.exists():
    tmp_part.unlink()

  ydl_opts = {
    "format": "bestaudio",
    "outtmpl": str(tmp_final), 
    "noplaylist": True,
}

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as video:
      cleanup_tmp_files()
      info_dict = video.extract_info(link, download = True)
  except KeyboardInterrupt:
    print("Download cancelled by the user")
    cleanup_tmp_files()
    return None
  except Exception as e:
    print("Error during download:")
    print(e)
    cleanup_tmp_files()
    return None
 
  if not tmp_final.exists() or tmp_final.stat().st_size == 0:
    print("Downloaded file missing or empty.")
    cleanup_tmp_files()
    return None

  title = sanitize_filename(info_dict.get("title", "audio"))
  final_path = TMP_DIR / f"{title}.download" 


  if final_path.exists():
      final_path.unlink()

  tmp_final.rename(final_path)

  print("Downloaded to:", final_path)
  return str(final_path)
    
     


