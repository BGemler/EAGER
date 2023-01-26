#!/usr/bin/env python3

import os
import sys
import logging
from utils import get_sample_r1r2_sra

# initalize logging
log = logging.getLogger('fastqc-multiqc')
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))


def execute_fastqc(sample_ids, FASTQ_LOC, fastqc_loc, FASTQC, NUM_THREADS, fastq_type):
	"""
	if fastq_type == "raw": fastq file endings are: sample_id + _R + {1/2} + .fastq.gz
	if fastq_type == "clean": fastq file endings are: sample_id + _R + {1/2} + -clean.fastq.gz
	"""
	for sample_id in sample_ids:
		if fastq_type == "raw":
			r1_loc = FASTQ_LOC + "/" + sample_id + "_R1.fastq.gz"
			r2_loc = FASTQ_LOC + "/" + sample_id + "_R2.fastq.gz"
		elif fastq_type == "clean":
			r1_loc = FASTQ_LOC + "/" + sample_id + "_R1-clean.fastq.gz"
			r2_loc = FASTQ_LOC + "/" + sample_id + "_R2-clean.fastq.gz"
		else:
			raise Exception("invalid fastq_type given")

		# run fastqc over each FASTQ file
		for fastq in [r1_loc, r2_loc]:
			command = FASTQC + " " + fastq + \
									" --outdir=" + fastqc_loc + \
									" -t " + str(NUM_THREADS) + \
									" --quiet"
			os.system(command)

		log.info('Finished FASTQC for {}'.format(sample_id))

	return


def execute_multiqc(fastqc_loc, MULTIQC):
	"""
	run multiqc over FASTQC files, save to FASTQC folder
	"""
	command = MULTIQC + " " + fastqc_loc + \
							" -o " + fastqc_loc + \
							" -f"
	os.system(command)

	log.info('Finished MultiQC, result located in {}'.format(fastqc_loc))

	return


sample_ids, _, _ = get_sample_r1r2_sra(sys.argv[1])

execute_fastqc(sample_ids, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[6], sys.argv[7])
execute_multiqc(sys.argv[3], sys.argv[5])