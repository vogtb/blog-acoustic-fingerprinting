import warnings
import glob
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
warnings.filterwarnings("ignore")
from fingerprinter.reader import read_single
from fingerprinter.fingerprint import Fingerprinter
from fingerprinter.fingerprint_record import determine_match
from database.fingerprint_db import FingerprintDatabase
from etc.util import get_args_for_input_output_directories, get_file_name

DESCRIPTION = """
This script will load all clips in a given directory (-d), fingerprint them, and lookup the corresponding episode in
the fingerprint database. It will then plot the positive, negative, false-positive, and false-negative matches to rate
the effectiveness of the current parameters of the algorithm. These plots will be saved as .png files in a given
output directory.

Files in the input directory should be in the format "{episode}.{play_head}.{noise_class}.wav", as written in the
clips.py script.
"""
PLOT_FINGERPRINTS = False
MAX_HASH_LOOKUP = 512


def pull_metadata_from_file_path(file_path):
  filename = file_path.split("/")[-1:][0]
  sp = filename.split('.')
  episode_name = sp[0]
  t = sp[1]
  wav_class = "NORMAL"
  if "HN" in filename:
    wav_class = "HN"
  elif "MN" in filename:
    wav_class = "MN"
  elif "LN" in filename:
    wav_class = "LN"
  return (wav_class, episode_name, t)


if __name__ == "__main__":
  args = get_args_for_input_output_directories(DESCRIPTION)
  print("Loading .wav files for analysis from {}".format(args.directory))
  db = FingerprintDatabase()
  results = {
    "NORMAL": {
      "tp": 0,
      "tn": 0,
      "fp": 0,
      "fn": 0
    },
    "LN": {
      "tp": 0,
      "tn": 0,
      "fp": 0,
      "fn": 0
    },
    "MN": {
      "tp": 0,
      "tn": 0,
      "fp": 0,
      "fn": 0
    },
    "HN": {
      "tp": 0,
      "tn": 0,
      "fp": 0,
      "fn": 0
    }
  }
  f = Fingerprinter(plot_fingerprint=PLOT_FINGERPRINTS)
  for filename in glob.glob(args.directory + "positive/*.wav"):
    print("Current working positive clip: {}".format(filename))
    wav_class, episode_name, tstamp = pull_metadata_from_file_path(filename)
    print("Positive Clip: {} {} {}".format(wav_class, episode_name, tstamp))
    channel, frame_rate = read_single(filename)
    hashes = [x for x in f.fingerprint(channel, frame_rate)]
    hash_numbers = [hash_pair[1] for hash_pair in hashes[0:MAX_HASH_LOOKUP]]
    fingerprint_records = db.find_records_by_hashes(hash_numbers)
    actual_match_name = determine_match(fingerprint_records)
    print("expected {}, actual {}".format(episode_name, actual_match_name))
    results[wav_class]["tp" if actual_match_name == episode_name else "fn"] += 1
  for filename in glob.glob(args.directory + "negative/*.wav"):
    print("Current working negative clip: {}".format(filename))
    wav_class, episode_name, tstamp = pull_metadata_from_file_path(filename)
    print("Negative Clip: {} {} {}".format(wav_class, episode_name, tstamp))
    channel, frame_rate = read_single(filename)
    hashes = [x for x in f.fingerprint(channel, frame_rate)]
    hash_numbers = [hash_pair[1] for hash_pair in hashes[0:MAX_HASH_LOOKUP]]
    fingerprint_records = db.find_records_by_hashes(hash_numbers)
    should_be_none = determine_match(fingerprint_records)
    print("expected None, actual {}".format(should_be_none))
    results[wav_class]["tn" if should_be_none is None else "fp"] += 1
  print(results)
  graphing_dict = {
    "LN": {
      "label": "LN",
      "color": "blue"
    },
    "MN": {
      "label": "MN",
      "color": "orange"
    },
    "HN": {
      "label": "HN",
      "color": "red"
    },
    "NORMAL": {
      "label": "NORMAL",
      "color": "green"
    }
  }
  for classification in ["NORMAL", "LN", "MN", "HN"]:
    tp = float(results[classification]["tp"])
    fp = float(results[classification]["fp"])
    tn = float(results[classification]["tn"])
    fn = float(results[classification]["fn"])
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    specificity = tn / (tn + fp)
    accuracy = (tp + tn) / (fp + tp + fn + tn)
    ppcr = (tp + fp) / (fp + tp + fn + tn)
    print(classification, "precision", precision)
    print(classification, "recall", recall)
    print(classification, "specificity", specificity)
    print(classification, "accuracy", accuracy)
    print(classification, "ppcr", ppcr)
    print("")
    plt.scatter([recall], [precision], marker="o", facecolors="None", color=graphing_dict[classification]["color"], s=40, linewidths=2, label=graphing_dict[classification]["label"])
  plt.title("Recall vs Precision")
  plt.ylabel("Precision")
  plt.xlabel("Recall")
  plt.xlim(-1, 1)
  plt.ylim(-1, 1)
  plt.legend(scatterpoints=1, loc='lower right')
  plt.axvline(x=0, color='b', linestyle=':')
  plt.axhline(y=0, color='b', linestyle=':')
  plt.tight_layout()
  plt.show()

  # grouping specificity, accuracy, ppcr
  rows = []
  for classification in ["NORMAL", "LN", "MN", "HN"]:
    tp = float(results[classification]["tp"])
    fp = float(results[classification]["fp"])
    tn = float(results[classification]["tn"])
    fn = float(results[classification]["fn"])
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    specificity = tn / (tn + fp)
    accuracy = (tp + tn) / (fp + tp + fn + tn)
    ppcr = (tp + fp) / (fp + tp + fn + tn)
    rows.append([classification, "specificity", specificity])
    rows.append([classification, "accuracy", accuracy])
    rows.append([classification, "ppcr", ppcr])
  dpoints = np.array(rows)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  space = 0.3
  conditions = np.unique(dpoints[:, 0])
  categories = np.unique(dpoints[:, 1])
  n = len(conditions)
  width = (1 - space) / (len(conditions))
  for i, cond in enumerate(conditions):
    indeces = range(1, len(categories) + 1)
    vals = dpoints[dpoints[:, 0] == cond][:, 2].astype(np.float)
    pos = [j - (1 - space) / 2. + i * width for j in range(1, len(categories) + 1)]
    ax.bar(pos, vals, width=width, label=cond, color=cm.Accent(float(i) / n))
    ax.set_xticks(indeces)
  ax.set_xticklabels(categories)
  handles, labels = ax.get_legend_handles_labels()
  ax.legend(handles[::-1], labels[::-1])
  plt.setp(plt.xticks()[1])
  ax.set_ylabel("Rate")
  ax.set_xlabel("Sample Class")
  plt.show()