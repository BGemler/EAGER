#!/usr/bin/env python3

import logging
import csv
import os

log = logging.getLogger('utils')
logging.basicConfig(level=os.environ.get('LOGLEVEL', 'INFO'))


def get_sample_r1r2_sra(SAMPLE_SRA_FILE):
	"""
	returns python dict of sample id: [R1 SRA, R2 SRA]
	"""
	sample_sra_dict, classification_sample_dict = {}, {}
	with open(SAMPLE_SRA_FILE, "r") as f:
		reader = csv.reader(f)
		next(reader, None)

		for row in reader:
			classification, sample_id, r1_sra, r2_sra = row

			sample_sra_dict[sample_id] = [r1_sra, r2_sra]

			if classification not in classification_sample_dict:
				classification_sample_dict[classification] = []
			classification_sample_dict[classification].append(sample_id)
	f.close()

	log.info('Parsed {} entries from SAMPLE_SRA_FILE'.format(len(sample_sra_dict)))

	return list(sample_sra_dict.keys()), sample_sra_dict, classification_sample_dict

