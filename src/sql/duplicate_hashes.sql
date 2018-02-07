-- Duplicate hashes, should be pretty low.
SELECT hash, COUNT(DISTINCT episode) AS e FROM fingerprints
GROUP BY hash HAVING e > 1 ORDER BY e DESC;