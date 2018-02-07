CREATE DATABASE fingerprints;
USE fingerprints;
CREATE TABLE Fingerprints (
  hash BIGINT NOT NULL,
  episode VARCHAR(20) NOT NULL,
  playhead BIGINT NOT NULL,
  INDEX(hash),
  UNIQUE(hash, playhead, episode)
);
