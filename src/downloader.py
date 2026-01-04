import yt_dlp
import os
import ffmpeg

output_folder = "./../downloads"
tmp_file = "raw_audio.mp3"


def download_audio(link):
  with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': output_folder + "/" + tmp_file}) as video:
    info_dict = video.extract_info(link, download = True)
    file_name = info_dict["title"]
    path = output_folder + "/" + tmp_file
    if os.path.isfile(path) and os.path.getsize(path) > 0:
      os.rename(path, output_folder + "/" + file_name + ".mp3")
      print("Successfully Downloaded - see local download folder", output_folder + "/" + file_name)
      loop(output_folder + "/" + file_name + ".mp3")
    else:
      return "Something went wrong during the download"    
    
     
def loop(input):

  OUTPUT = "./../downloads/loop_30m.mp3"

  TARGET_SECONDS = 30 * 60
  FADE_IN = 0.2          # seconds
  FADE_OUT = 0.4         # seconds

  (
      ffmpeg
      .input(input, stream_loop=-1)
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

download_audio('https://youtu.be/HsUjBw_auZw')
