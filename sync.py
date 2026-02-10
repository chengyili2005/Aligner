"""
Description: This is a quick script I made to align 2 media files by padding the lacking one.
Credits: The repository KnurpsBram/shign does most of the heavy lifting here, I've just added extra steps to handle videos.
"""

import argparse
import shign
import librosa
import os
from moviepy import AudioClip, VideoClip, TextClip, VideoFileClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips
import numpy as np

VIDEO_EXTENSIONS = [".mp4", ".mov"]
AUDIO_EXTENSIONS = [".mp3", ".wav"]

def parse_args():
  parser = argparse.ArgumentParser(
    description=
    "Sync up two media files"
  )
  parser.add_argument('--in1', type=str)
  parser.add_argument('--in2', type=str)
  parser.add_argument('--pad', type=bool, default=False, help="If argument is here it will create new files with respective pads. Leave blank if you don't want new media files")
  args = parser.parse_args()
  return args

def what_media(file):
  # Determins what type of file the path is based off a list of supported extensions
  __, extension = os.path.splitext(file)
  if extension in VIDEO_EXTENSIONS:
    return 'video'
  elif extension in AUDIO_EXTENSIONS:
    return 'audio'
  else:
    return None

def load_files(file1, file2):
  # Determine if file is an audio or video file path, then load it as a moviepy object
  files = {file1: None, file2: None}
  for file in files.keys():
    media_type = what_media(file)
    if media_type=='video':
      files[file] = VideoFileClip(file)
    elif media_type=='audio':
      files[file] = AudioFileClip(file)
    else:
      print(f"Unable to load this audio file {file}")
      print(f"Supported file formats: {", ".join(VIDEO_EXTENSIONS)}, {", ".join(AUDIO_EXTENSIONS)}")
  return files[file1], files[file2]

def write_files(out1, out2, path1, path2):
  # Write the moviepy files into memory
  paths = {path1: out1, path2: out2}
  for path in paths.keys():
    out = paths[path]
    if isinstance(out, VideoFileClip) or isinstance(out, VideoClip):
      out.write_videofile(path, codec='libx264', audio_codec='aac')
    elif isinstance(out, AudioFileClip) or isinstance(out, AudioClip):
      out.write_audiofile(path)

def pad_files(file1, file2, delta_b):

  # Load in the files as moviepy objects (to handle both video and audio files)
  moviepy1, moviepy2 = load_files(file1, file2)

  # Create padding
  padding_seconds = abs(delta_b / 1000.0)
  padding_audio = AudioClip(lambda t: np.zeros(2), duration=padding_seconds, fps=44100)

  # 2nd file needs to be padded
  if delta_b > 0:

    if isinstance(moviepy2, VideoFileClip):
      padding_video = TextClip(text=f"Shign: This part of the video was padded so that it would line up with the audio file\n Video starts at: {padding_seconds // 60} mins & {padding_seconds % 60} seconds:", color='white', size=moviepy2.size, bg_color='black')
      padding_video = padding_video.with_duration(padding_seconds).with_position("Center")
      moviepy2 = concatenate_videoclips([padding_video, moviepy2])
    elif isinstance(moviepy2, AudioFileClip):
      padding_audio = AudioClip(lambda t: np.zeros(2), duration=padding_seconds, fps=44100)
      moviepy2 = concatenate_audioclips([padding_audio, moviepy2])
    print(f"{file2} will be padded")

  # 1st file needs to be padded
  elif delta_b < 0:

    if isinstance(moviepy1, VideoFileClip):
      padding_video = TextClip(text=f"Shign: This part of the video was padded so that it would line up with the audio file", color='white', size=moviepy1.size, bg_color='black')
      padding_video = padding_video.with_duration(padding_seconds).with_position("Center")
      moviepy1 = concatenate_videoclips([padding_video, moviepy1])
    elif isinstance(moviepy1, AudioFileClip):
      padding_audio = AudioClip(lambda t: np.zeros(2), duration=padding_seconds, fps=44100)
      moviepy1 = concatenate_audioclips([padding_audio, moviepy1])
    print(f"{file1} will be padded")

  # Files are already perfect
  else:
    pass

  out1, out2 = moviepy1, moviepy2

  return out1, out2

if __name__ == '__main__':

  # Grab argumentsb,
  args = parse_args()
  inputfile1 = args.in1
  inputfile2 = args.in2
  pad = args.pad

  # Load files into audio files
  audio_1, sr_1 = librosa.load(inputfile1, sr=None)
  audio_2, sr_2 = librosa.load(inputfile2, sr=None)

  # Get milliseconds needed to shift
  delta_b = shign.get_shift_ms(audio_a=audio_1, audio_b=audio_2, sr_a=sr_1, sr_b=sr_2)
  if delta_b > 0:
    print(delta_b, "milliseconds needs to be added to the beginning of", inputfile2)
  elif delta_b < 0:
    print(abs(delta_b), "milliseconds needs to be added to the beginning of", inputfile1)
  else:
    print("files are already lined up")

  # Pad the files respectively
  if pad:
    print("Padding files accordingly...")
    out1, out2 = pad_files(inputfile1, inputfile2, delta_b)

    # Append "shigned_" before the basename and write the files into memory
    dir1 = os.path.dirname(inputfile1)
    dir2 = os.path.dirname(inputfile2)
    base1 = os.path.basename(inputfile1)
    base2 = os.path.basename(inputfile2)
    path1 = os.path.join(dir1, f"shigned_{base1}")
    path2 = os.path.join(dir2, f"shigned_{base2}")
    write_files(out1, out2, path1, path2)
  else:
    pass
