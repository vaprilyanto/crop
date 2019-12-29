import sys
import codecs
import os
from src import *

# use: python main_guide_variant.py INFILE

INFILE = sys.argv[1]

# creating folder for single-fasta files
main_folder = str(INFILE.rsplit('/',1)[0] + '/')
save_path = str('./' + main_folder)

with open(INFILE, 'r') as infile:
  lines = infile.readlines()
  seq_number = ((len(lines)) // 2)
  infile.seek(0)
  
  for name, seq in read_fasta(infile):
    outfile = codecs.open(save_path + name[1:] + '_var.fasta', 'w')
    counter = 1

    print ('Writing guide variant for %s ...' % name[1:])

    
    # writing substitution variants in outfile
    for subs_variant in addpam_substitute(seq):
      outfile.write('%s_subs_%s\n%s\n' % (name, str(counter), subs_variant))
      counter += 1

    # writing deletion variants in outfile
    for dels_variant in addpam_delete(seq):
      if len(dels_variant) == len(seq)+3-1:
        outfile.write('%s_1del_%s\n%s\n' % (name, str(counter), dels_variant))
        counter += 1
      elif len(dels_variant) == len(seq)+3-2:
        outfile.write('%s_2del_%s\n%s\n' % (name, str(counter), dels_variant))
        counter += 1
      elif len(dels_variant) == len(seq)+3-3:
        outfile.write('%s_3del_%s\n%s\n' % (name, str(counter), dels_variant))
        counter += 1
      else:
        outfile.write('%s_4del_%s\n%s\n' % (name, str(counter), dels_variant))
        counter += 1
    
    # writing insertion variants in outfile
    for ins_variant in addpam_insert(seq):
      if len(ins_variant) == len(seq)+3+1:
        outfile.write('%s_1ins_%s\n%s\n' % (name, str(counter), ins_variant))
        counter += 1
      elif len(ins_variant) == len(seq)+3+2:
        outfile.write('%s_2ins_%s\n%s\n' % (name, str(counter), ins_variant))
        counter += 1
      elif len(ins_variant) == len(seq)+3+3:
        outfile.write('%s_3ins_%s\n%s\n' % (name, str(counter), ins_variant))
        counter += 1
      else:
        outfile.write('%s_4ins_%s\n%s\n' % (name, str(counter), ins_variant))
        counter += 1
        
  outfile.close()
