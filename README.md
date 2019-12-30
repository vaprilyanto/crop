# CRISPR Off-Target-Predictor (CROP)
Predicts off-target propensity of CRISPR guide sequences

CRISPR Off-target Predictor (CROP) is a program which predicts the off-target propensity of a CRISPR guide sequence (guide) by creating combinations of substitutions, deletions and insertions for up to four positions along the guide 20 nucleotides. All of these combinations will then be mapped into the genome by using Bowtie (Langmead et al, 2009). The resulting mapped guide variants are counted to give the respective guide's off-target propensity. Two off-target scoring systems, namely Hsu (Hsu et al, 2013) and CFD (Doench et al, 2014; Doench et al, 2016) are also used to calculate the off-target score of each guide. This program takes an input of a folder containing gene sequences if (multi)-fasta formatted file and a reference genome for mapping purpose. It can take multiple genes at once but be aware that the number of input fasta files corresponds to the number of computer cores used.

# Before using CROP
Make sure that the reference genome `your-genome.fasta` has already been indexed using Bowtie (ref). To make an index:
1. place the genome file `your-genome.fasta` in `genome/` directory
2. open bash and install bowtie: `sudo apt install bowtie`
3. navigate into `genome/` directory and type: `bowtie-build your-genome.fasta`
4. the indexing will take several minutes depending on your computer. This process will gives you six files, namely: `your-genome.1.ebwt`, `your-genome.2.ebwt`, `your-genome.3.ebwt`, `your-genome.4.ebwt`, `your-genome.rev.1.ebwt` and `your-genome.rev.1.ebwt`.

# Using CROP
1. Place all the fasta-formatted DNA sequences into one directory. Name this dirctory without using underscore character (e.g. `input-folder/`)
2. Open bash and navigate to `crop/` directory. There are two `.sh` files, `core.sh` and `crop.sh`. Make both files into executables using `chmod +x core.sh` and `chmod +x crop.sh`, respectively
3. Run`./crop.sh` followed by entering `input folder` and `your-genome`
4. CROP is now running. Depending on your computer, it takes aroung 100 seconds to process one guide sequence. The total duration will follow the input sequence with most guides 

# CROP Result
CROP outputs the result named `input-folder_out/`. Each fasta file inside the `input-folder/` were reported in `input-folder_out/` as separate folders. Each folder contains:
1. `_align/` containing `align_map_s*.csv`, a table containing all mapped variants aligned to the original guide sequence, comparing mismatch positions
2. `_ot_maps/` containing `map_s*.txt`, a sam-formatted file listing mapped guide variants
3. `_outfiles/` containing `<seq>_out_doench.txt`, a raw 30nt-guide sequence (N4-guide-NGG-N3) file as input for Azimuth score calculation at https://crispr.ml website; `<seq>_out_guide_list.fasta`, a fasta file containing all guide sequences extracted from `<seq>`; `<seq>_score.csv`, a table containing multiple informations for each guide, including GC content, Doench on-target score, map count, Hsu & CFD off-target score, and number of on target count
4. `_single_guides/` containing `<seq>.fasta`, single-fasta files containing 20nt guide sequence concatenated with 78nt tracrRNA sequence. Both sequences are in RNA form (T > U)
5. `<seq>_log.txt`, a log file recording all the process taken to give the result and the time needed to finish the process

# Troubleshoot
Problem | Troubleshoot
------- | ------------
ERROR: input directory `<directory>` does not exist. Check it!! | Make sure that you type the correct input folder
ERROR: genome `<genome>` does not exist. Check it!! | Make sure you type the correct genome name or the genome is already in genome/ folder
`rm` cannot remove: <file> Permission denied | Close all files in the previous `*_out/` folder. File/folder overwrite proceeds if only all the files are closed
`mkdir` cannot create directory <directory>: File exists | Close all files in the previous `*_out/ folder`. File/folder overwrite proceeds if only all the files are closed

# Licenses
Included software:
Bowtie: Artistic License 2.0

# References
1. Langmead, B., Trapnell, C., Pop, M. & Salzberg, S. L. Ultrafast and memory-efficient alignment of short DNA sequences to the human genome. Genome Biol. 10, (2009).
2. Hsu, P. D. et al. DNA targeting specificity of RNA-guided Cas9 nucleases. Nat. Biotechnol. 31, 827–832 (2013).
3. Doench, J. G. et al. Rational design of highly active sgRNAs for CRISPR-Cas9-mediated gene inactivation. Nat. Biotechnol. 32, 1262–1267 (2014).
4. Doench, J. G. et al. Optimized sgRNA design to maximize activity and minimize off-target effects of CRISPR-Cas9. Nat. Biotechnol. 34, 184–191 (2016).
