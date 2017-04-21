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


def nhmmer_allvsall(nhmmer_path, fastafile):
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
    os.mkdir("nhmmer_results")
    out_file = os.path.join("nhmmer_results", "nhmmer.out")
    sto_file = os.path.join("nhmmer_results", "nhmmer.sto")
    tbl_file = os.path.join("nhmmer_results", "nhmmer.tbl")
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
    nhmmer_allvsall(NHMMER_PATH, FASTA_FILE)
