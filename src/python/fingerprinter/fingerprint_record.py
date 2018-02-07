class FingerprintRecord(object):
  """
  Represents a single hash of a fingerprint record from the database
  """

  def __init__(self, hash_id, episode, play_head):
    self.hash_id = hash_id
    self.episode = episode
    self.play_head = play_head

  def __str__(self):
    return "hash:{} episode:{} playhead:{}".format(self.hash_id, self.episode, self.play_head)

MATCH_RATIO_THRESHOLD = 0.1

def determine_match(records):
  """
  Determines a match based on frequency of episode in records.
  :param records: FingerprintRecords
  :return: episode match string, or None, if no match found.
  """
  histogram = {}
  for record in records:
    if record.episode in histogram:
      histogram[record.episode] += 1
    else:
      histogram[record.episode] = 1
  s = sorted(histogram.iteritems(), key=lambda (k, v): v)
  match = s[-1]
  if match[1] > int(MATCH_RATIO_THRESHOLD * len(records)):
    return match[0]
  else:
    return None