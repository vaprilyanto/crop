import sys
import codecs
import csv
from src import *

# use: python <script>.py INIT_SEQ MAP_NUMBER DOENCH_SEQ

INIT_SEQ = sys.argv[1] # _out_guide_list.fasta file
MAP_NUMBER = int(sys.argv[2]) # total number of map_s files
DOENCH_SEQ = sys.argv[3] # _out_doench.txt file

# creating folder for output files
outfile_path = str(INIT_SEQ.rsplit('/',1)[0] + '/')
map_path = str(INIT_SEQ.rsplit('/',1)[0].rsplit('_',1)[0] + '_ot_maps/')
stat_path = str(INIT_SEQ.rsplit('_',3)[0])

# calculate CFD, HSU and count; write each score to separate files
with open(INIT_SEQ, 'r') as init_seq, open(DOENCH_SEQ, 'r') as doench_seq:
  score_file = codecs.open('%s_score.csv' % stat_path, 'w')
  score_file.write('SCORING OFF-TARGET FOR: %s\nName,Seq,PAM,GC,Doench,Subs,Dels,Ins,Total,Hsu,CFD,Total On Tgt\n' % INIT_SEQ.rsplit('/',1)[1])

  for (name, seq), map_file, dseq in zip(read_fasta(init_seq), range(1, MAP_NUMBER+1), doench_seq):
    query_seq = codecs.open('%smap_s%d.txt' % (map_path, map_file), 'r')

    dscore = calc_doench_score(dseq)

    # reading map file row-wise
    rows = csv.reader(query_seq, delimiter = '\t')

    # declaring initial number of subs, dels and ins (for count_file)
    subs, dels, ins = 0, 0, 0
    
    # initial score for CFD and HSU scores
    cfd_total_score = []
    hsu_total_score = []
    
    for row in rows:
      # counting number of subs, dels and ins seq variants
      if 'subs' in row[0]:
        subs += 1
      elif 'del' in row[0]:
        dels += 1
      elif 'ins' in row[0]:
        ins += 1
      else: pass
      total = subs + dels + ins

      # calculating CFD and HSU scores
      if 'subs' in row[0]:
        if row[1] == '-':
          row[4] = reverse_complement(row[4])
                
        cfd_total_score.append(float(calc_cfd(seq[:20], row[4][:20], row[4][-2:])))
        hsu_total_score.append(float(calc_hsu_score(seq[:20], row[4][:20])))

    #writing all cfd scores
    cfd_total_score.sort()
    hsu_total_score.sort()

    agg_cfd = 100/(100 + sum(cfd_total_score[:-1])) * 100
    agg_hsu = 100/(100 + sum(hsu_total_score[:-1])) * 100
    gc = gc_content(seq[:20])

    score_file.write('%s,%s,%s,%s,%s,%d,%d,%d,%d,%.3f,%.3f,%s\n'
                     % (name[1:], seq[:20], seq[20:], gc, dscore, subs, dels, ins, total, agg_hsu, agg_cfd, str(cfd_total_score.count(100.000))))
    
    if cfd_total_score.count(100.000) > 1:
      print('%s has %d additional on-target' % (name[1:], cfd_total_score[:-1].count(100.000)))
    elif cfd_total_score.count(100.000) == 1:
      print('%s has only one on-target' % name[1:])
    else:
      print('%s has no on-target' % name[1:])

  score_file.close()
