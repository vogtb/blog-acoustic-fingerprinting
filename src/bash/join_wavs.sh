#!/bin/bash

#####
# Joins all .wav files with noise .wav files, resulting in 3 new files.
#
#
#####

POSITIVE_DIRECTORY=/mnt/src/data/samples/positive/
NEGATIVE_DIRECTORY=/mnt/src/data/samples/negative/

LN=/mnt/src/blog_repos/blog-acoustic-fingerprinting/src/wav/light_ambient_noise_10s.wav
MN=/mnt/src/blog_repos/blog-acoustic-fingerprinting/src/wav/medium_ambient_noise_10s.wav
HN=/mnt/src/blog_repos/blog-acoustic-fingerprinting/src/wav/heavy_ambient_noise_10s.wav

for file in $(ls ${POSITIVE_DIRECTORY})
do
  f=${file::-4}
  ffmpeg -i ${POSITIVE_DIRECTORY}/${file} \
    -i ${HN} \
    -filter_complex amerge -q:a 4 ${POSITIVE_DIRECTORY}/${f}.HN.wav

  ffmpeg -i ${POSITIVE_DIRECTORY}/${file} \
    -i ${MN} \
    -filter_complex amerge -q:a 4 ${POSITIVE_DIRECTORY}/${f}.MN.wav

  ffmpeg -i ${POSITIVE_DIRECTORY}/${file} \
    -i ${LN} \
    -filter_complex amerge -q:a 4 ${POSITIVE_DIRECTORY}/${f}.LN.wav
done



for file in $(ls ${NEGATIVE_DIRECTORY})
do
  f=${file::-4}
  ffmpeg -i ${NEGATIVE_DIRECTORY}/${file} \
    -i ${HN} \
    -filter_complex amerge -q:a 4 ${NEGATIVE_DIRECTORY}/${f}.HN.wav

  ffmpeg -i ${NEGATIVE_DIRECTORY}/${file} \
    -i ${MN} \
    -filter_complex amerge -q:a 4 ${NEGATIVE_DIRECTORY}/${f}.MN.wav

  ffmpeg -i ${NEGATIVE_DIRECTORY}/${file} \
    -i ${LN} \
    -filter_complex amerge -q:a 4 ${NEGATIVE_DIRECTORY}/${f}.LN.wav
done