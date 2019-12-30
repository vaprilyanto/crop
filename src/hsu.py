# This code was adopted based on source code by Hari Jay 
# "https://snipt.net/harijay/fz-score-d1324dab/"

import functools
import operator

def product(iterable):
  return functools.reduce(operator.mul, iterable, 1)

def calc_hsu_score(seq1, seq2, seqlen=20):
  M = [0,0,0.014,0,0,0.395,0.317,0,0.389,0.079,0.445,0.508,0.613,0.851,0.732,0.828,0.615,0.804,0.685,0.583]
  if len(seq1) != len(seq2):
    raise ValueError('Sequences need to be the same length')
  mm_pos = [index+1 for index, elem in enumerate(zip(seq1.strip(), seq2.strip()))\
            if elem[0] != elem[1] if index <20]
  mm_num = len(mm_pos)
  min_d, max_d = None, None
  if mm_num >= 1:
    min_d, max_d = min(mm_pos), max(mm_pos)

  d = None
  if seq1 == seq2:
    d = 19
  else:
    try:
      d = (max_d - min_d)/(mm_num-1.0)
    except ZeroDivisionError:
      d = 19

  pi_term = None
  if mm_pos != []:
    pi_term = product([1-M[i-1] for i in mm_pos])
  else:
    pi_term = 1

  second_term = None
  if d:
    second_term = 1/((((19.0-d)/19.0)*4.0)+1)
  else:
    second_term = 1

  score = None
  if mm_num > 0:
    score = second_term * pi_term * (1.0/(mm_num)**2)*100
  else:
    score = 100
  return '%.3f' % score
