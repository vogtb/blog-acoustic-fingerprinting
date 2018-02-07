import numpy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)
from mmh3 import hash
from operator import itemgetter


MINIMUM_TIME_BETWEEN_PEAKS = 0
MAX_TIME_BETWEEN_PEAKS = 200
PEAK_NEIGHBOR_COUNT = 20
HASH_PEAK_FAN_OUT = 4

FFT_WINDOW_SIZE = 4096
OVERLAP_RATIO = 0.5
MINIMUM_AMPLITUDE = 20
PLOT_FINGERPRINT = False


class Fingerprinter(object):
  def __init__(self, plot_fingerprint=PLOT_FINGERPRINT,
      min_between_peaks=MINIMUM_TIME_BETWEEN_PEAKS,
      max_between_peaks=MAX_TIME_BETWEEN_PEAKS,
      peak_neighbor_count=PEAK_NEIGHBOR_COUNT,
      hash_peak_fan_out=HASH_PEAK_FAN_OUT):
    self.plot_fingerprint = plot_fingerprint
    self.max_between_peaks = max_between_peaks
    self.min_between_peaks = min_between_peaks
    self.peak_neighbor_count = peak_neighbor_count
    self.hash_peak_fan_out = hash_peak_fan_out


  def fingerprint(self, channel_samples, sample_rate):
    frequency_bins = mlab.specgram(channel_samples,
         NFFT=FFT_WINDOW_SIZE,
         Fs=sample_rate,
         window=mlab.window_hanning,
         noverlap=int(FFT_WINDOW_SIZE * OVERLAP_RATIO))[0]
    # specgram gives us a frequency break down that is linear, when frequencies are logarithmic
    frequency_bins = 10 * numpy.log10(frequency_bins)
    frequency_bins[frequency_bins == -numpy.inf] = 0
    binary_structure = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(binary_structure, PEAK_NEIGHBOR_COUNT)
    local_max = maximum_filter(frequency_bins, footprint=neighborhood) == frequency_bins
    background = (frequency_bins == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    detected_peaks = local_max ^ eroded_background
    amps = frequency_bins[detected_peaks]
    j, i = numpy.where(detected_peaks)
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    filtered_peaks = [x for x in peaks if x[2] > MINIMUM_AMPLITUDE]
    frequency_component = [x[1] for x in filtered_peaks]
    time_component = [x[0] for x in filtered_peaks]
    if self.plot_fingerprint:
      fig, ax = plt.subplots()
      ax.imshow(frequency_bins)
      ax.scatter(time_component, frequency_component)
      ax.set_xlabel('Time')
      ax.set_ylabel('Frequency')
      ax.set_title("Spectrogram")
      plt.gca().invert_yaxis()
      plt.show()
    peaks = zip(frequency_component, time_component)
    print("peak count: {}".format(len(peaks)))
    return self.generate_hashes(peaks)


  @staticmethod
  def generate_hashes(peaks):
    peaks.sort(key=itemgetter(1))
    for i in range(len(peaks)):
      for j in range(1, HASH_PEAK_FAN_OUT):
        if (i + j) < len(peaks):
          freq1 = peaks[i][0]
          freq2 = peaks[i + j][0]
          t1 = peaks[i][1]
          t2 = peaks[i + j][1]
          t_delta = t2 - t1
          if t_delta >= MINIMUM_TIME_BETWEEN_PEAKS and t_delta <= MAX_TIME_BETWEEN_PEAKS:
            h = hash("{}:{}:{}".format(str(freq1), str(freq2), str(t_delta)))
            yield (t1, h)