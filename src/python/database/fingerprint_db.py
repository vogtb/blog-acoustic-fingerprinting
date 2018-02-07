import MySQLdb as mdb
from fingerprinter.fingerprint_record import FingerprintRecord

MYSQL_HOST = "localhost"
MYSQL_USER = "super"
MYSQL_PASSWORD = "password"
MYSQL_DB_NAME = "fingerprints"
INSERT_SINGLE_ROW_STATEMENT = "INSERT INTO Fingerprints (hash, episode, playhead) VALUES ({:d}, '{}', {})"
SELECT_SINGLE_HASH_QUERY = "SELECT hash, episode, playhead FROM Fingerprints where hash = {:d}"
SELECT_HASH_IN_QUERY = "SELECT hash, episode, playhead FROM Fingerprints where hash in ({})"


class FingerprintDatabase(object):
  """Instance of the database that holds fingerprints. Assumes a schema specified in the schema.sql file in this repo.

  """
  def __init__(self, host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db_name=MYSQL_DB_NAME):
    self.host = host
    self.user = user
    self.password = password
    self.db_name = db_name
    self.connection = mdb.connect(host, user, password, db_name)

  def insert(self, fingerprint):
    try:
      cur = self.connection.cursor()
      cur.execute(INSERT_SINGLE_ROW_STATEMENT.format(fingerprint.hash_id, fingerprint.episode, fingerprint.play_head))
      self.connection.commit()
    except mdb.Error, e:
      print("Error %d: %s" % (e.args[0], e.args[1]))

  def lookup(self, hash_number):
    try:
      cur = self.connection.cursor()
      cur.execute(SELECT_SINGLE_HASH_QUERY.format(hash_number))
      return cur
    except mdb.Error, e:
      print("Error %d: %s" % (e.args[0], e.args[1]))

  def find_records_by_hashes(self, hash_numbers):
    """
    Selects all records that exist for any hash in hash_numbers list.
    :param hash_numbers: to select on.
    :return: list of FingerprintRecords
    """
    query = SELECT_HASH_IN_QUERY.format(", ".join(str(x) for x in hash_numbers))
    try:
      cur = self.connection.cursor()
      cur.execute(query)
      return [FingerprintRecord(hash_id, episode, play_head) for (hash_id, episode, play_head) in cur]
    except mdb.Error, e:
      print("Error %d: %s" % (e.args[0], e.args[1]))
