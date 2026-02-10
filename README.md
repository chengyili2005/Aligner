# Aligner

## Info
Not to be confused with forced alignment.

This script uses a pre-existing repository `KnurpsBram/shign` to "shift and align" two existing audio signals.

It does this by calculating the shifting that will maximize correlation between the two waveforms. Then, it pads one the waveform that is too early such that it aligns with the other waveform.

Effectively, it can be used to line up two media files that record the same audio (for example, a video and lapel microphone recording of the same interaction)

## Setup
Install `KnurpsBram/shign`:
```{bash}
# Clone repository
git clone https://github.com/KnurpsBram/shign
cd shign
pip install .

# Can be removed after install
cd ../
rm -rf shign
```

Install FFMPEG for your OS: https://www.ffmpeg.org/download.html
```{bash}
# If you're on Ubuntu/Debian
sudo apt update
sudo apt install
```

Install Python dependencies:
```{bash}
# Through PIP
pip install -r requirements.txt
```

## Usage
```
python align.py --in1 {file1} --in2 {file2} --pad True
```
Note: If you don't want to pad then just remove the --pad argument.

## Other notes
- This doesn't work if the two files are too far apart. If they're a under a minute off there's a good chance it'll work.
- Audio/Video quality tends to decrease after running the alignment. It's not noticeable to me but sometimes the audio will sound a little crunchy.
- Rendering the videos tends to take a bit.