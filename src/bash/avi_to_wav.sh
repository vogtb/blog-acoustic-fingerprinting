#!/bin/bash

#####
# Extracts audio channels from .avi files to .wav files.
#
#
#####

DIRECTORY=/mnt/src/data/the_drew_carey_show/avi
OUTPUT=/mnt/src/data/the_drew_carey_show/wav

# Ensure directory exists
mkdir -p ${OUTPUT}

# For each file, extract audio
for file in $(ls $DIRECTORY)
do
  ffmpeg -i $DIRECTORY/$file -acodec pcm_s16le -ac 2 $OUTPUT/$file.wav
done
