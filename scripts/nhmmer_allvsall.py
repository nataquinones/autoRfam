"""
DESCRIPTION:
Runs NHMMER all vs. all from .fasta file.
USE:
nhmmer_allvsall.py <nhmmerpath> <in>
<nhhmerpath> path to nhmmer software
<in> input .fasta file
"""

import os
import subprocess
import sys

# .............................FUNCTIONS...................................


def main(nhmmer_path, fastafile, results_path, results_name):
    """
    Runs NHMMER with fasta file vs. itself, with options:
    -o: save output file
    -A: generate alignment of significant hits
    --tblout: output in tbl format
    --noali: remove alignments from general output
    --rna: for RNA sequences
    --tformat: Target format in FASTA
    --qformat: Query format in FASTA
    ..........
    nhmmer_path: path to nhmmer software
    fasta: fasta file with sequences to be used as query and target
    """
    # output dir and files
    os.mkdir(results_path)
    out_file = os.path.join(results_path, results_name + ".out")
    sto_file = os.path.join(results_path, results_name + ".sto")
    tbl_file = os.path.join(results_path, results_name + ".tbl")
    # process
    nhmmer_template = nhmmer_path + " -o %s"\
                                    " -A %s"\
                                    " --tblout %s"\
                                    " --noali"\
                                    " --rna"\
                                    " --tformat fasta"\
                                    " --qformat fasta"\
                                    " %s"\
                                    " %s"
    cmd = nhmmer_template % (out_file,
                             sto_file,
                             tbl_file,
                             fastafile,
                             fastafile)
    subprocess.call(cmd, shell=True)

# .........................................................................

if __name__ == '__main__':
    NHMMER_PATH = sys.argv[1]
    FASTA_FILE = sys.argv[2]
    RESULTS_PATH = sys.argv[3]
    RESULTS_NAME = sys.argv[4]
    main(NHMMER_PATH, FASTA_FILE, RESULTS_PATH, RESULTS_NAME)
