#!/bin/bash -e

function fail {
	echo "$@" >&2
	exit 1
}

# add bin directory to path
BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. >/dev/null 2>&1 && pwd )"
export PATH="$BASE/bin:$PATH"

# user-system specifications 
NUM_THREADS="8"

# specify tool paths (note - this could be done better in a dockerized implementation)
# hard-coded for now
SRA_TOOLKIT="/home/fung/Documents/sratoolkit.2.11.0-ubuntu64/bin/"
FASTQC="/home/fung/Documents/FastQC/fastqc"
MULTIQC="multiqc"
FASTP="/home/fung/Documents/fastp"
SPADES="/home/fung/Documents/SPAdes-3.15.2-Linux/bin/spades.py"
QUAST="/home/fung/Documents/quast-5.0.2/"

# specify user-defined files
SAMPLE_SRA_FILE="$BASE/sources/sample_sra_map.csv" # note - working data has 2 SRA IDs for each sample. Must manually define
# NOTE - this format is antiquated... and isn't modern. Replace post project so 1 SRA per sample (with --split flag)
PIPELINE_WORK_DIR="$BASE/salmonella"

# check for existence of necessary files for pipeline to run
[ -z "$SRA_TOOLKIT" ] && fail "SRA_TOOLKIT must be provided"
[ -z "$FASTQC" ] && fail "FASTQC must be provided"
[ -z "$MULTIQC" ] && fail "MULTIQC must be provided"
[ -z "$FASTP" ] && fail "FASTP must be provided"
[ -z "$SPADES" ] && fail "SPADES must be provided"
[ -z "$QUAST" ] && fail "QUAST must be provided"
[ -z "$NUM_THREADS" ] && fail "NUM_THREADS must be provided"
[ ! -f "$SAMPLE_SRA_FILE" ] && fail "SAMPLE_SRA_FILE $SAMPLE_SRA_FILE does not exist"

# ensure necessary tools are in path
which python3 >/dev/null || fail "python3 must be on the PATH"

# initialize working folders
FASTQ_LOC=${FASTQ_LOC:-"$PIPELINE_WORK_DIR/fastqs"}
RAW_FASTQC_LOC=${RAW_FASTQC_LOC:-"$PIPELINE_WORK_DIR/raw_fastqc"}
CLEAN_FASTQC_LOC=${CLEAN_FASTQC_LOC:-"$PIPELINE_WORK_DIR/clean_fastqc"}
SPADES_LOC=${SPADES_LOC:-"$PIPELINE_WORK_DIR/spades"}
QUAST_LOC=${QUAST_LOC:-"$PIPELINE_WORK_DIR/quast"}

mkdir -p "$PIPELINE_WORK_DIR"
mkdir -p "$FASTQ_LOC"
mkdir -p "$RAW_FASTQC_LOC"
mkdir -p "$CLEAN_FASTQC_LOC"
mkdir -p "$SPADES_LOC"
mkdir -p "$QUAST_LOC"

export PIPELINE_WORK_DIR
export FASTQ_LOC
export RAW_FASTQC_LOC
export CLEAN_FASTQC_LOC
export SPADES_LOC
export QUAST_LOC

# Download SRA accessions
#$BASE/bin/download_ncbi_sra.py "$SAMPLE_SRA_FILE" "$SRA_TOOLKIT" "$FASTQ_LOC"

# Run FASTQC/MultiQC over raw FASTQs
#$BASE/bin/run_fastqc.py "$SAMPLE_SRA_FILE" "$FASTQ_LOC" "$RAW_FASTQC_LOC" "$FASTQC" "$MULTIQC" "$NUM_THREADS" "raw"

# Run FASTQ cleaning protocol (FASTP). Merge cleaned files into a single pair of R1/R2 for co-assembly
#$BASE/bin/run_fastp.py "$SAMPLE_SRA_FILE" "$FASTQ_LOC" "$FASTP" "$NUM_THREADS" "$PIPELINE_WORK_DIR"

# Run FASTQC/MultiQC over clean FASTQs
#$BASE/bin/run_fastqc.py "$SAMPLE_SRA_FILE" "$FASTQ_LOC" "$CLEAN_FASTQC_LOC" "$FASTQC" "$MULTIQC" "$NUM_THREADS" "clean"

# Run SPAdes, QUAST assembly evaluation
$BASE/bin/run_spades.py "$SPADES" "$PIPELINE_WORK_DIR" "$NUM_THREADS" "$SPADES_LOC" "$QUAST" "$QUAST_LOC"
