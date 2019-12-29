import pickle
import argparse
import re
import numpy as np

mm_scores_path = './src/mismatch_score.pkl'
pam_scores_path = './src/pam_scores.pkl'

def reverse_complement(seq):
  base_rev_comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A','U':'A'}
  rc_seq = ''
  for base in seq:
    rc_seq += base_rev_comp[base]
  return rc_seq[::-1]

def get_mm_pam_scores():
  try:
    mm_scores = pickle.load(open(mm_scores_path, 'rb'))
    pam_scores = pickle.load(open(pam_scores_path,'rb'))
    return (mm_scores,pam_scores)
  except: 
    raise Exception("Could not find file with mismatch scores or PAM scores")

def calc_cfd(wt,sg,pam):
  mm_scores,pam_scores = get_mm_pam_scores()
  score = 1
  sg = sg.replace('T','U')
  wt = wt.replace('T','U')
  s_list = list(sg)
  wt_list = list(wt)
  for i,sl in enumerate(s_list):
    if wt_list[i] == sl:
      score *= 1
    else:
      key = 'r' + wt_list[i] + ':d' + reverse_complement(sl) + ',' + str(i+1)
      score *= mm_scores[key]
  score *= pam_scores[pam]
  return (100 * score)
