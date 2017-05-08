"""
Description:
Runs nhmmer with .fasta file against itself with options:
-o -A --tblout --noali --rna --tformat fasta --qformat fasta
and returns *.out, *.sto and *.tbl output files.

Use:
nhmmer_allvsall.py <nhmmerpath> <in> <out_path> <out_name>

<nhmmerpath>: Path to nhmmer from HMMER-3.1b2
<in>: Input .fasta file
<out_path>: Path where all the output files will be saved
<out_name>: Name of the output files
"""

import os
import subprocess
import sys

# .............................FUNCTIONS...................................


def main(nhmmer_path, fastafile, results_path, results_name):
    """
    Runs nhmmer with .fasta file against itself with options:
    -o -A --tblout --noali --rna --tformat fasta --qformat fasta
    and returns *.out, *.sto and *.tbl output files.

    nhmmer_path: path to nhmmer software
    fasta: fasta file with sequences to be used as query and target
    results_path: Path where all the output files will be saved
    results_name: Name of the output files before extension
    """

    # define output dir and output file names
    os.mkdir(results_path)
    out_file = os.path.join(results_path, results_name + ".out")
    sto_file = os.path.join(results_path, results_name + ".sto")
    tbl_file = os.path.join(results_path, results_name + ".tbl")
    # subprocess template
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
    # run subprocess
    subprocess.call(cmd, shell=True)

# .........................................................................

if __name__ == '__main__':
    nhmmer_path = sys.argv[1]
    fastafile = sys.argv[2]
    results_path = sys.argv[3]
    results_name = sys.argv[4]
    main(nhmmer_path, fastafile, results_path, results_name)
