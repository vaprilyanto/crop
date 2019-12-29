def mismatch_count(seq1, seq2):
  mismatch = sum(c1!=c2 for c1, c2 in zip(seq1, seq2))
  return mismatch
