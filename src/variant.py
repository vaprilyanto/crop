import itertools as it

def base_combination(pos):
  for i in list(it.product('ATGC', repeat=pos)):
    yield i

def pams():
  pams = ['AGG', 'TGG', 'GGG', 'CGG', 'AAG', 'TAG', 'GAG', 'CAG']
  return pams

# substitute every 4-position combinations in seq with 'u-x'
def base_substitute(seq):
  for i in range(0, len(seq)-3):
    for j in range(1, len(seq)-2):
      for k in range(2, len(seq)-1):
        for l in range(3, len(seq)):
          yield seq[:i] + 'u' + seq[i+1:i+j] + 'v' + seq[i+j+1:i+j+k-1] + \
              'w' + seq[i+j+k:i+j+k+l-3] + 'x' + seq[i+j+k+l-2:]

# substitute every combination of base positions to '-'
def base_delete(seq):
  for i in range(0, len(seq)-1):
    yield seq[:i+1] + '-' + seq[i+2:]
    
  for i in range(0, len(seq)-2):
    for j in range(1, len(seq)-1):
      yield seq[:i+1] + '-' + seq[i+2:i+j+1] + '-' + seq[i+j+2:]

  for i in range(0, len(seq)-3):
    for j in range(1, len(seq)-2):
      for k in range(2, len(seq)-1):
        yield seq[:i+1] + '-' + seq[i+2:i+j+1] + '-' + seq[i+j+2:i+j+k] +\
              '-' + seq[i+j+k+1:]

  for i in range(0, len(seq)-4):
    for j in range(1, len(seq)-3):
      for k in range(2, len(seq)-2):
        for l in range(3, len(seq)-1):
          yield seq[:i+1] + '-' + seq[i+2:i+j+1] + '-' + seq[i+j+2:i+j+k] +\
              '-' + seq[i+j+k+1:i+j+k+l-2] + '-' + seq[i+j+k+l-1:]

# insert each position in seq with 'u-x'
def base_insert_1(seq):
  for i in range(0, len(seq)):
    yield seq[:i+1] + 'u' + seq[i+1:]

def base_insert_2(seq):
  for i in range(0, len(seq)):
    for j in range(1, len(seq)+1):
      yield seq[:i+1] + 'u' + seq[i+1:i+j] + 'v' + seq[i+j:]

def base_insert_3(seq):
  for i in range(0, len(seq)):
    for j in range(1, len(seq)+1):
      for k in range(2, len(seq)+2):
        yield seq[:i+1] + 'u' + seq[i+1:i+j] + 'v' + seq[i+j:i+j+k-2] +\
              'w' + seq[i+j+k-2:]

def base_insert_4(seq):
  for i in range(0, len(seq)):
    for j in range(1, len(seq)+1):
      for k in range(2, len(seq)+2):
        for l in range(3, len(seq)+3):
          yield seq[:i+1] + 'u' + seq[i+1:i+j] + 'v' + seq[i+j:i+j+k-2] +\
              'w' + seq[i+j+k-2:i+j+k+l-5] + 'x' + seq[i+j+k+l-5:]

# filtering duplicates from base_substitute(seq)
def filter_substitute(seq):
  for guide in base_substitute(seq):
    for base in base_combination(4):
      if len(guide) == len(seq):
        yield guide.replace('u', base[0]).replace('v', base[1])\
            .replace('w', base[2]).replace('x', base[3])

# filtering duplicates from base_delete(seq)
def filter_delete(seq):
  for guide in base_delete(seq):
    if guide[-1] == '-' or guide[-2:] == '--'\
       or guide[-3:] == '---' or guide[-4:] == '----':
      pass
    else: yield guide.replace('-', '')

# filtering duplicates from base_insert(seq)
def filter_insert(seq):
  for guide in base_insert_1(seq):
    for base in base_combination(1):
      yield guide.replace('u', base[0])

  for guide in base_insert_2(seq):
    for base in base_combination(2):
      yield guide.replace('u', base[0]).replace('v', base[1])

  for guide in base_insert_3(seq):
    for base in base_combination(3):
      yield guide.replace('u', base[0]).replace('v', base[1])\
            .replace('w', base[2])

  for guide in base_insert_4(seq):
    for base in base_combination(4):
      yield guide.replace('u', base[0]).replace('v', base[1])\
            .replace('w', base[2]).replace('x', base[3])

# adding NRG at the 3' end of each seq
def addpam_substitute(seq):
  for guide_subs in set(filter_substitute(seq)):
    for pam in pams():
      yield guide_subs + pam

def addpam_delete(seq):
  for guide_dels in set(filter_delete(seq)):
    for pam in pams():
      yield guide_dels + pam

def addpam_insert(seq):
  for guide_ins in set(filter_insert(seq)):
    for pam in pams():
      yield guide_ins + pam
