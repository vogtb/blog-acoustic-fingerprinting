import warnings
warnings.filterwarnings("ignore")
from fingerprinter.reader import read
from fingerprinter.fingerprint import fingerprint
from database.fingerprint_db import FingerprintDatabase
from etc.util import get_args_for_input_file

DESCRIPTION = """
This script will load a single wav file (-f), fingerprint it, and plot it.
"""
PLOT_FINGERPRINT = True


if __name__ == "__main__":
  args = get_args_for_input_file(DESCRIPTION)
  print("Loading, fingerprinting, and plotting wav file {}".format(args.file))
  db = FingerprintDatabase()
  channels, frame_rate = read(args.file)
  for _, channel in enumerate(channels):
    hash_tuples = fingerprint(channel, frame_rate, PLOT_FINGERPRINT)
