#!/bin/bash

echo "=== STEP 1: LISTING GUIDE SEQUENCES ==="
echo ""
python3 main_guide_finder.py $1
echo "=== STEP 1 done! ==="
echo ""

#Bowtie must be installed to run this step
echo "=== STEP 2: CREATING GUIDE VARIANTS & MAPPING TO GENOME ==="
echo ""
genome=./genome/$2
path0='./'`dirname $1`'_out/'$(cut -d. -f1 <<<`basename $1`)_result/
path1='./'`dirname $1`'_out/'$(cut -d. -f1 <<<`basename $1`)_result/$(cut -d. -f1 <<<`basename $1`)_ot_maps
path2='./'`dirname $1`'_out/'$(cut -d. -f1 <<<`basename $1`)_result/$(cut -d. -f1 <<<`basename $1`)_outfiles
path3='./'`dirname $1`'_out/'$(cut -d. -f1 <<<`basename $1`)_result/$(cut -d. -f1 <<<`basename $1`)_single_guides
guide_file_num=$(ls $path1 -1q | wc -l 2>&1)

for (( num=1; num <=$guide_file_num; num++));
do
echo 'creating variants for s'$num'.fasta'
python3 main_guide_variant.py $path1/'s'$num'.fasta'
echo 'done creating variants for s'$num'.fasta'
rm $path1/'s'$num'.fasta'
echo 'mapping s'$num'_var.fasta' to genome
bowtie $genome -v 0 -f $path1/'s'$num'_var.fasta' > $path1/'map_s'$num'.txt'
echo 'done mapping variants s'$num'_var.fasta' to genome
rm $path1/'s'$num'_var.fasta'
echo ""
done
echo "all guide variants have been mapped"
echo "=== STEP 2 done! ==="
echo ""

echo "=== STEP 3: SCORING MAPPED VARIANTS ==="
echo "calculate scores for "$guide_file_num" guides..."
python3 main_guide_score.py $path2/$(cut -d. -f1 <<<`basename $1`)_out_guide_list.fasta $guide_file_num $path2/$(cut -d. -f1 <<<`basename $1`)_out_doench.txt
echo "Done scoring" $(cut -d. -f1 <<<`basename $1`)
echo "=== STEP 3 done! ==="
echo ""

echo "=== STEP 4: ALIGN MAPPED VARIANTS ==="
python3 main_guide_align.py $path2/$(cut -d. -f1 <<<`basename $1`)_out_guide_list.fasta $guide_file_num
echo "Done aligning" $(cut -d. -f1 <<<`basename $1`)
echo "=== STEP 4 done! ==="
echo ""
echo "This analysis was run using cas_191219"