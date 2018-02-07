import warnings
import glob
warnings.filterwarnings("ignore")
from fingerprinter.reader import read
from fingerprinter.fingerprint import Fingerprinter
from fingerprinter.fingerprint_record import FingerprintRecord
from database.fingerprint_db import FingerprintDatabase
from etc.util import get_file_name, get_args_for_input_directory

DESCRIPTION = """
This script will load all .wav files in a given directory (-d) and fingerprint them, persisting the fingerprints to
a MySQL database. All .wav files should be in standard season-episode format, e.g. "s01e01".
"""
PLOT_FINGERPRINT = False


if __name__ == "__main__":
  args = get_args_for_input_directory(DESCRIPTION)
  print("Loading and fingerprinting .wav files from directory {}".format(args.directory))
  db = FingerprintDatabase()
  f = Fingerprinter(plot_fingerprint=PLOT_FINGERPRINT)
  for filename in glob.glob(args.directory + "*.wav"):
    print("Fingerprinting file: {}".format(filename))
    episode_name = get_file_name(filename)
    channels, frame_rate = read(filename)
    for _, channel in enumerate(channels):
      hash_tuples = [x for x in f.fingerprint(channel, frame_rate)]
      print("hash count: {}".format(len(hash_tuples)))
      for hash_tuple in hash_tuples:
        hash_id = hash_tuple[1]
        playhead = hash_tuple[0]
        print("Inserting fingerprint: {}:{}:{}".format(hash_id, episode_name, playhead))
        db.insert(FingerprintRecord(hash_id, episode_name, playhead))
