import re

'''def crispr_guide(seq, length, pam):
  seq = seq.upper()
  pattern = r'(?=(' + (r'\w'*int(length)) + pam + r'))'
  guide = re.findall(pattern, seq)
  guide_list = []
  for i in guide:
    guide_list.append(i)
  return guide_list'''

def crispr_guide(seq, length, pam):
  seq = seq.upper()
  pattern = r'(?=(' + (r'\w'*(int(length)+4)) + pam + (r'\w'*3) + r'))'
  guide = re.findall(pattern, seq)
  guide_list = []
  for i in guide:
    guide_list.append(i)
  return guide_list
