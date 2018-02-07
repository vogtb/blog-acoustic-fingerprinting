from argparse import ArgumentParser

def get_file_name(path):
  """
  Separates a path name of the format "/whatever/dir/file.wav" into "file".
  :param path: to parse into the primary component of the file.
  :return: the separated file name.
  """
  return path.split("/")[-1:][0].split('.')[0]

def get_args_for_input_directory(description):
  """
  Simple args parser for a single input directory.
  :description: default description to output
  :return: args parsed from command line
  """
  parser = ArgumentParser(description=description)
  parser.add_argument('-d', '--directory', type=str, help='Directory of input files', required=True)
  args = parser.parse_args()
  return args

def get_args_positive_negative_out(description):
  """
  Simple args parser for a single input directory, single output directory.
  :description: default description
  :return: args parsed from command line
  """
  parser = ArgumentParser(description=description)
  parser.add_argument('-p', '--positive', type=str, help='Directory of input files, positive match', required=True)
  parser.add_argument('-n', '--negative', type=str, help='Directory of input files, negative match', required=True)
  parser.add_argument('-o', '--output', type=str, help='Directory of output files', required=True)
  args = parser.parse_args()
  return args

def get_args_for_input_output_directories(description):
  """
  Simple args parser for a single input directory, single output directory.
  :description: default description
  :return: args parsed from command line
  """
  parser = ArgumentParser(description=description)
  parser.add_argument('-d', '--directory', type=str, help='Directory of input files', required=True)
  parser.add_argument('-o', '--output', type=str, help='Directory of output files', required=True)
  args = parser.parse_args()
  return args

def get_args_for_input_file(description):
  """
  Simple args parser for a single input file.
  :description: default description to output
  :return: args parsed from command line
  """
  parser = ArgumentParser(description=description)
  parser.add_argument('-f', '--file', type=str, help='Input file', required=True)
  args = parser.parse_args()
  return args
