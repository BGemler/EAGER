#!/usr/bin/env python3

import csv
import logging
import os
import sys
from utils import get_sample_r1r2_sra

# initalize logging
log = logging.getLogger('sra-download')
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))


def download_sra_fastqs(sample_sra_dict, SRA_TOOLKIT, FASTQ_LOC):
	"""
	utilizes sra toolkit to download FASTQs to 
	working directory 
	"""
	for sample_id in sample_sra_dict:
		r1_sra, r2_sra = sample_sra_dict[sample_id]

		# execute sra toolkit to download each FASTQ
		counter = 0
		for sra_id in [r1_sra, r2_sra]:
			counter += 1
			command = SRA_TOOLKIT + 'fastq-dump ' + sra_id + \
									' -O ' + FASTQ_LOC
			os.system(command)

			# rename the FASTQ to something more intelligent
			new_name = sample_id + "_R" + str(counter) + ".fastq"
			os.system("mv " + FASTQ_LOC + "/" + sra_id + ".fastq" + " " + FASTQ_LOC + "/" + new_name)

			# compress the FASTQ
			command = "gzip " + FASTQ_LOC + "/" + new_name
			os.system(command)

			log.info('Downloaded {} SRA FASTQ file'.format(sra_id))

	return


_, sample_sra_dict, _ = get_sample_r1r2_sra(sys.argv[1])
download_sra_fastqs(sample_sra_dict, sys.argv[2], sys.argv[3])