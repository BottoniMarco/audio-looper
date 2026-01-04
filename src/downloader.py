import yt_dlp
import os
from pathlib import Path
import re
import unicodedata
from looper import loop

tmp_output_folder = "./../tmp"
tmp_file = "raw_audio.mp3"



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

def download_audio(link):
  try:
    with yt_dlp.YoutubeDL({
      'extract_audio': True, 'format': 'bestaudio', 
      'outtmpl': tmp_output_folder + "/" + tmp_file}) as video:
      info_dict = video.extract_info(link, download = True)
  except Exception as e:
      print("Error during download:")
      print(e)
      return None
  file_name = sanitize_filename(info_dict["title"])
  path = tmp_output_folder + "/" + tmp_file
  if os.path.isfile(path) and os.path.getsize(path) > 0:
    os.rename(path, tmp_output_folder + "/" + file_name + ".mp3")
    print("Successfully Downloaded - see local download folder", tmp_output_folder + "/" + file_name )
    output = loop(tmp_output_folder + "/" + file_name + ".mp3")
    return output
  else:
      print("Downloaded file missing or empty.")
      return None    
    
     


