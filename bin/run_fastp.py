#!/usr/bin/env python3

import os
import sys
import logging
from utils import get_sample_r1r2_sra

# initalize logging
log = logging.getLogger('fastp')
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))


def run_fastp(sample_ids, FASTQ_LOC, FASTP, NUM_THREADS):
	"""
	"""
	for sample_id in sample_ids:
		raw_r1_loc = FASTQ_LOC + "/" + sample_id + "_R1.fastq.gz"
		raw_r2_loc = FASTQ_LOC + "/" + sample_id + "_R2.fastq.gz"

		clean_r1_loc = FASTQ_LOC + "/" + sample_id + "_R1-clean.fastq.gz"
		clean_r2_loc = FASTQ_LOC + "/" + sample_id + "_R2-clean.fastq.gz"

		command = FASTP + \
								" -i " + raw_r1_loc + \
								" -I " + raw_r2_loc + \
								" -o " + clean_r1_loc + \
								" -O " + clean_r2_loc + \
								" --json /dev/null --html /dev/null" + \
								" --thread " + str(NUM_THREADS)
		os.system(command)

	return


def merge_files(sample_ids, FASTQ_LOC, CONCAT_FASTQ_LOC):
	"""
	create a concatenated R1/R2 for SPAdes co-assembly
	"""
	r1_locs, r2_locs = [], []
	for sample_id in sample_ids:
		clean_r1_loc = FASTQ_LOC + "/" + sample_id + "_R1-clean.fastq.gz"
		clean_r2_loc = FASTQ_LOC + "/" + sample_id + "_R2-clean.fastq.gz"

		r1_locs.append(clean_r1_loc)
		r2_locs.append(clean_r2_loc)

	# build concat call for each of R1/R2
	command = "cat "
	for fastq in r1_locs:
		command = command + fastq + " "
	command = command + "> " + CONCAT_FASTQ_LOC + "/overall-R1.fastq.gz"
	os.system(command)

	command = "cat "
	for fastq in r2_locs:
		command = command + fastq + " "
	command = command + "> " + CONCAT_FASTQ_LOC + "/overall-R2.fastq.gz"
	os.system(command)

	return


sample_ids, _, _ = get_sample_r1r2_sra(sys.argv[1])

run_fastp(sample_ids, sys.argv[2], sys.argv[3], sys.argv[4])
merge_files(sample_ids, sys.argv[2], sys.argv[5])