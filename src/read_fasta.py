def read_fasta(file):
  name, seq = None, []
  for line in file:
    line = line.rstrip()
    if line.startswith('>'):
      if name: yield (name, ''.join(seq))
      name, seq = line, []
    else:
      seq.append(line)
  if name: yield (name, ''.join(seq))
