def reverse_complement(seq):
  base_rev_comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
  rc_seq = ''
  for base in seq:
    rc_seq += base_rev_comp[base]
  return rc_seq[::-1]

def gc_content(seq):
  gc_content = (seq.count('G') + seq.count('C')) / len(seq) * 100
  return '%.2f' % gc_content
