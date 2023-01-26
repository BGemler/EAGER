#!/usr/bin/env python3

import os
import sys


def run_spades(SPADES, CONCAT_FASTQ_LOC, NUM_THREADS, SPADES_LOC):
	"""
	run RNA spades on concatenated R1 and R2
	"""
	command = SPADES + \
							" -1 " + CONCAT_FASTQ_LOC + "/overall-R1.fastq.gz" + \
							" -2 " + CONCAT_FASTQ_LOC + "/overall-R2.fastq.gz" + \
							" -t " + str(NUM_THREADS) + \
							" -o " + SPADES_LOC + \
							" --rna"
	os.system(command)

	return


def run_quast(CONCAT_FASTQ_LOC, SPADES_LOC, NUM_THREADS, QUAST, QUAST_LOC):
	"""
	run quast, using read mapping functionality for coverage stats
	"""
	contig_loc = SPADES_LOC + "/transcripts.fasta"

	command = QUAST + "./quast.py" + \
							" " + contig_loc + \
							" -1 " + CONCAT_FASTQ_LOC + "/overall-R1.fastq.gz" + \
							" -2 " + CONCAT_FASTQ_LOC + "/overall-R2.fastq.gz" + \
							" -o " + QUAST_LOC + \
							" -t " + str(NUM_THREADS) + \
							" --silent"
	os.system(command)
	

	return


#run_spades(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
run_quast(sys.argv[2], sys.argv[4], sys.argv[3], sys.argv[5], sys.argv[6])
