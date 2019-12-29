# crispr-offtarget-predictor (CROP)
Predicts off-target propensity of CRISPR guide sequences

CRISPR Off-target Predictor (CROP) is a program which predicts the off-target propensity of a CRISPR guide sequence (guide) by creating combinations of substitutions, deletions and insertions for up to four positions along the guide 20 nucleotides. All of these combinations will then be mapped into the genome by using Bowtie (ref). The resulting mapped guide variants are counted to give the respective guide's off-target propensity. Two off-target scoring systems, namely Hsu (ref) and CFD (ref) are also used to calculate the off-target score of each guide. This program takes an input of a folder containing gene sequences if (multi)-fasta formatted file and a reference genome for mapping purpose. It can take multiple genes at once but be aware that the number of input fasta files corresponds to the number of computer cores used.

# Before using CROP
Make sure that the reference genome `your-genome.fasta` has already been indexed using Bowtie (ref). To make an index:
1. place the genome file `your-genome.fasta` in `genome/` directory
2. open bash and install bowtie: `sudo apt install bowtie`
3. navigate into `genome/` directory and type: `bowtie-build your-genome.fasta`
4. the indexing will take several minutes depending on your computer. This process will gives you six files, namely: `your-genome.1.ebwt`, `your-genome.2.ebwt`, `your-genome.3.ebwt`, `your-genome.4.ebwt`, `your-genome.rev.1.ebwt` and `your-genome.rev.1.ebwt`.

# Using CROP
1.
