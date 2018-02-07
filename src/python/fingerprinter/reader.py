import numpy as np
from pydub import AudioSegment


def read(filename):
  audiofile = AudioSegment.from_file(filename)
  # Setting to single channel, mono, so we don't have to process to signals which are likely to be very similar.
  audiofile = audiofile.set_channels(1)
  data = np.fromstring(audiofile._data, np.int16)
  channels = []
  for chn in xrange(audiofile.channels):
    channels.append(data[chn::audiofile.channels])
  fs = audiofile.frame_rate
  return channels, fs

def read_single(filename):
  audiofile = AudioSegment.from_file(filename)
  # Setting to single channel, mono, so we don't have to process to signals which are likely to be very similar.
  audiofile = audiofile.set_channels(1)
  data = np.fromstring(audiofile._data, np.int16)
  channels = []
  for chn in xrange(audiofile.channels):
    channels.append(data[chn::audiofile.channels])
  fs = audiofile.frame_rate
  return channels[0], fs