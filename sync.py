"""
Description: This is a quick script I made to align 2 media files by padding the lacking one.
Credits: The repository KnurpsBram/shign does most of the heavy lifting here, I've just added extra steps to handle videos.
"""

import argparse
import shign
import librosa
import os
import moviepy

def parse_args():
  parser = argparse.ArgumentParser(
    description=
    "Sync up two audio files"
  )
  parser.add_argument('--in1', type=str)
  parser.add_argument('--in2', type=str)
  parser.add_argument('--change_files', type=str, default='False')
  args = parser.parse_args()
  return args

def load_files(file1, file2, delta_b):
  # Determine if file is an audio or video file path, then load it as a moviepy object
  # TODO
  moviepy1, moviepy2 = None, None
  return moviepy1, moviepy2

def write_files(out1, out2, path1, path2):
  # Write the moviepy files into memory
  # TODO
  return

def pad(file1, file2, delta_b):

  # Load in the files as moviepy objects (to handle both video and audio files)
  moviepy1, moviepy2 = load_files(file1, file2)

  # 2nd file needs to be padded
  if delta_b > 0:
    # TODO
    pass

  # 1st file needs to be padded
  elif delta_b < 0:
    # TODO
    pass

  # Files are already perfect
  else:
    print("Files are already lined up")
    out1, out2 = moviepy1, moviepy2

  return out1, out2

if __name__ == '__main__':

  # Grab arguments
  args = parse_args()
  inputfile1 = args.in1
  inputfile2 = args.in2
  change_files = args.change_files

  # Load files into audio files
  audio_1, sr_1 = librosa.load(inputfile1, sr=None)
  audio_2, sr_2 = librosa.load(inputfile2, sr=None)

  # Get milliseconds needed to shift
  delta_b = shign.get_shift_ms(audio_a=audio_1, audio_b=audio_2, sr_a=sr_1, sr_b=sr_2)
  print(delta_b, "milliseconds needs to be added to the second file")

  # Pad the files respectively
  out1, out2 = pad(inputfile1, inputfile2)

  # Append "shigned_" before the basename and write the files into memory
  # TODO
  path1 = ""
  path2 = ""
  write_files(out1, out2, path1, path2)
