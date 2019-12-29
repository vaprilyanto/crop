#!/bin/bash

read -p 'Select your input folder: ' directory
if [ ! -d ./$directory/ ]; then
	echo 'ERROR: input directory' $directory 'does not exist. Check it!!'
	exit
else
	read -p 'Type reference genome for mapping: ' genome
	if [ ! -f ./genome/$genome'.1.ebwt' ]; then
		echo 'ERROR: genome' $genome 'does not exist. Check it!!'
		exit
	else
		for f in ./$directory/*fasta; do
		if [[ $f == *[_]* ]]; then
			echo 'ERROR:' $f 'must not contain underscore (_) character. Rename it!!'
			exit
		else
			echo 'This run will delete all previous files in the './$directory'_out/ and write new files during its process...'
			read -p 'Do you want to proceed? [y/n]:' ans
			if [ $ans != 'y' ]; then
				echo Run cancelled by user...
				exit
			else
				rm -r './'$directory'_out/'
				mkdir './'$directory'_out/'
				for f in ./$directory/*.fasta; do
				mkdir './'$directory'_out/'$(cut -d. -f1 <<<`basename $f`)_result/
				((time ./core.sh $f $genome) 2>&1 | tee -a './'$directory'_out/'$(cut -d. -f1 <<<`basename $f`)_result/$(cut -d. -f1 <<<`basename $f`)_log.txt) &
				done
			fi
			wait
			exit
		fi
		done
	fi
fi