import warnings
import glob
warnings.filterwarnings("ignore")
from fingerprinter.reader import read_single
from etc.util import get_args_for_input_output_directories, get_file_name
from random import randint
from scipy.io.wavfile import write


DESCRIPTION = """
Pull random 1-second clips from every .wav file in a given directory (-d), and output them to another directory (-o).
All filenames will be in the format "{episode}.{play_head}.wav", e.g. "s01e01.555.wav"
"""
CLIP_LENGTH_SECONDS = 16


if __name__ == "__main__":
  args = get_args_for_input_output_directories(DESCRIPTION)
  print("Loading cutting clips from .wav files in directory {}".format(args.directory))
  working_directory = args.directory
  output_directory = args.output
  for filename in glob.glob(working_directory + "*.wav"):
    print("Cutting clip for {}".format(filename))
    episode_name = get_file_name(filename)
    channel, frame_rate = read_single(filename)
    index_of_clip = randint(0, len(channel) - frame_rate)
    one_second_clip = channel[index_of_clip:index_of_clip + (CLIP_LENGTH_SECONDS * frame_rate)]
    output_file_path = "{}/{}.{}.wav".format(output_directory, episode_name, (index_of_clip / frame_rate))
    write(output_file_path, frame_rate, one_second_clip)
