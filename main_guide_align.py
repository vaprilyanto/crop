import sys
import codecs
import csv
from src import *

#use: python main_guide_align.py INIT_SEQ.fasta MAP_NUMBER

INIT_SEQ = sys.argv[1] # _out_var_guide.fasta file
MAP_NUMBER = int(sys.argv[2]) # total number of map_s files

# path
outfile_path = str(INIT_SEQ.rsplit('/',1)[0] + '/')
map_path = str(INIT_SEQ.rsplit('/',1)[0].rsplit('_',1)[0] + '_ot_maps/')
stat_path = str(INIT_SEQ.rsplit('_',3)[0])
align_path = str(INIT_SEQ.rsplit('/',1)[0].rsplit('_',1)[0] + '_align/')

# calculate CFD, HSU and count; write each score to separate files
with open(INIT_SEQ, 'r') as init_seq:
  for (name, seq), map_file in zip(read_fasta(init_seq), range(1, MAP_NUMBER+1)):
    query_seq = codecs.open('%smap_s%d.txt' % (map_path, map_file), 'r')
    align_sfile = codecs.open(align_path + name[1:] + '_align.csv', 'w')
    align_sfile.write('GUIDE TO VARIANT ALIGN FILE FOR: %s\n\nName,Guide,Variant,MM_Guide,MM_PAM,Alignment,Hsu,CFD\n' % INIT_SEQ.rsplit('/',1)[1])

    # reading map file row-wise
    rows = csv.reader(query_seq, delimiter = '\t')

    #containers
    guide_vars = []
    mm_guides = []
    mm_pams = []
    aligns = []
    hsu_list = []
    cfd_list = []

    for row in rows:
      if 'subs' in row[0]:
        if row[1] == '-':
          row[4] = reverse_complement(row[4])

        guide_vars.append(row[4])
        aligns.append(''.join(['.' if i == j else '|' for i, j in zip(seq,row[4])]))
        mm_guides.append(sum(seq != var for seq, var in zip(seq[:20], row[4][:20]))) # count mismatch between 20-nt seqs
        mm_pams.append(sum(seq != var for seq, var in zip(seq[20:], row[4][20:]))) # count mismatch between PAMs
        hsu_list.append(float(calc_hsu_score(seq[:20], row[4][:20])))
        cfd_list.append(float(calc_cfd(seq[:20], row[4][:20], row[4][-2:])))

    for guide_var, mm_guide, mm_pam, align, hsu, cfd in zip(guide_vars, mm_guides, mm_pams, aligns, hsu_list, cfd_list):      
      align_sfile.write('%s,%s,%s,%d,%d,%s,%s,%s\n' % (name[1:], seq, guide_var, mm_guide, mm_pam, align, str(hsu), str(cfd)))
    align_sfile.close()
