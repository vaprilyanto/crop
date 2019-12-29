import codecs
import sys
from os import mkdir
from os.path import basename, dirname
from src import *

# USE --> python main_guide_finder.py INFILE.fasta

# input file (in fasta format) as the first argument
INFILE = sys.argv[1] # input sequences in (multi) fasta file

# creating folder for output files
filename = basename(INFILE).rsplit('.')[0]
pathname = dirname(INFILE)

#creating output folders
main_folder = mkdir(pathname + '_out/%s_result/%s_single_guides/' % (filename, filename))
result_folder = mkdir(pathname + '_out/%s_result/%s_outfiles/' % (filename, filename))
ot_folder = mkdir(pathname + '_out/%s_result/%s_ot_maps/' % (filename, filename))
align_folder = mkdir(pathname + '_out/%s_result/%s_align/' % (filename, filename))

# output files destination
main_path = '%s_out/%s_result/' % (pathname, filename)
sguide_path = '%s%s_single_guides/' % (main_path, filename)
ot_path = '%s%s_ot_maps/' % (main_path, filename)
align_path = '%s%s_align/' % (main_path, filename)
outfile_path = '%s%s_outfiles/' % (main_path, filename)

# create output files
print('creating output files...')
guide_list_table = codecs.open(outfile_path + filename + '_out_guide_list.csv', 'w') # csv file to list guides
guide_list_fasta = codecs.open(outfile_path + filename + '_out_guide_list.fasta', 'w') # fasta file to list guides
guide_doench = codecs.open(outfile_path + filename + '_out_doench.txt','w') # standard txt file to list guides used for calculating Doench/Azimuth on-target score
print('done!')

pam = '[ATGC]GG' # change this if you want another PAM
guide_length = 20
tracr = 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUU'
print('This process uses PAM: ', pam, 'and guide length: ', guide_length)

print('processing', filename, '...')
with codecs.open(INFILE, 'r') as infile:
  # create counter which spans to all fasta sequences
  count = 1
  num = 1
  f_counts = 0
  r_counts = 0
  for name, seq in read_fasta(infile):
    seq = seq.upper()
    
    # create counter which reset while changing fasta sequence
    f_count = 1
    r_count = 1

    # check the input sequence consists of only ATGC
    if not set(seq) <= set('ATGC'):
      print(filename, name[1:], 'contains non-DNA sequences!! Check it!')
      break
    else:
      f_guides = []
      r_guides = []
      
      # searching fwd & rev 30nt-guides from a given sequence: N4-guide-PAM-N3
      f_guides_doench = crispr_guide(seq, guide_length, pam)
      r_guides_doench = crispr_guide(reverse_complement(seq), guide_length, pam)

      # searching forward guides from a given sequence
      for f_guide in f_guides_doench:
        f_guides.append(f_guide[4:27])
      
      # searching reverse guides from a given sequence
      for r_guide in r_guides_doench:
        r_guides.append(r_guide[4:27])

    if f_guides == []:
      print(filename + ' ' + name[1:] + ' ' + 'has no forward guides!')
    else:
      for f_guide in f_guides:
        # write single fasta files
        # each contains single 20nt-guide sequence in RNA bases 'AUGC' + 78nt tracr-RNA sequence
        f_single_guide = codecs.open(sguide_path + name[1:] + '_f' + str(f_count) + '.fasta', 'w')
        f_single_guide.write(name + '_f' + str(f_count) + '\n' +\
                             f_guide[:guide_length].replace('T','U') + tracr)

        # write single-fasta files, each contains single 20nt-guide sequence in fasta format
        f_single_ot = codecs.open(ot_path + 's' + str(num) + '.fasta', 'w')
        f_single_ot.write('>s' + str(num) + '\n' +\
                             f_guide[:guide_length])

        # write all f_guides in guide_list.fasta file
        guide_list_fasta.write(name + '_f' + str(f_count) + '\n' + f_guide + '\n')

        # write all f_guides in guide_list.csv file
        guide_list_table.write(name[1:] + '_' + str(f_count) + ',' + '+' + ',' + f_guide[:guide_length] +\
                       ',' + f_guide[guide_length:] + ',' + gc_content(f_guide[:20]) + '\n')

        num += 1
        f_count += 1
        f_counts += 1
        count += 1
        f_single_guide.close()

      # write plain N4-guide-PAM-N3 sequences into guide_doench file
      for f_guide_doench in f_guides_doench:
        guide_doench.write(f_guide_doench + '\n')

      print(filename + ' ' + name[1:] + ' ' + 'forward sequence done!')

    if r_guides == []:
      print(filename + ' ' + name[1:] + ' ' + 'has no reverse guides!')
    else:
      for r_guide in r_guides:
        # write single fasta files
        # each contains single 20nt-guide sequence in RNA bases 'AUGC' + 78nt tracr-RNA sequence
        r_single_guide = codecs.open(sguide_path + name[1:] + '_r' + str(r_count) + '.fasta', 'w')
        r_single_guide.write(name + '_r' + str(r_count) + '\n' +\
                             r_guide[:guide_length].replace('T','U') + tracr)

        # write single-fasta files, each contains single 20nt-guide sequence in fasta format
        r_single_ot = codecs.open(ot_path + 's' + str(num) + '.fasta', 'w')
        r_single_ot.write('>s' + str(num) + '\n' +\
                             r_guide[:guide_length])
        
        # write all r_guides in guide_list.fasta file
        guide_list_fasta.write(name + '_r' + str(r_count) + '\n' + r_guide + '\n')

        # write all r_guides in guide_list.csv file
        guide_list_table.write(name[1:] + '_' + str(r_count) + ',' + '-' + ',' + r_guide[:guide_length] +\
                       ',' + r_guide[guide_length:] + ',' + gc_content(r_guide[:20]) + '\n')

        num += 1
        r_count += 1
        r_counts += 1
        count += 1
        r_single_guide.close()

      # write plain N4-guide-PAM-N3 sequences into guide_doench file
      for r_guide_doench in r_guides_doench:
        guide_doench.write(r_guide_doench + '\n')
      
      print(filename + ' ' + name[1:] + ' ' + 'reverse sequence done!')
  
  print('\nAll the guides in', filename, 'has been printed out. Total:', count-1, 'guides')
  print('Resulted files: \n',
        '1.', filename + '_out_guide_list.csv\n',
        '2.', filename + '_out_guide_list.fasta\n',
        '3.', filename + '_out_doench.txt\n',
        '4.', f_counts, 'single-fasta files for forward guides\n',
        '5.', r_counts, 'single-fasta files for reverse guides')
        
  guide_list_table.close()
  guide_list_fasta.close()
  guide_doench.close()
  
