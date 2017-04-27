"""
DESCRIPTION:
Runs R-scape and puts output in rscape/ folder.
USE:
run_rscape.py <rscape_path> <dir_path>
<rscape_path> path to R-scape software
<dir_path> path to directory of directories with one alignment per folder.

Designed to run on a tree like:

dir/
|-- URSxxxxxxxxxx
|   |__ URSxxxxxxxxxx.sto
|__ ...

Producing:

dir/
|-- URSxxxxxxxxxx
|   |-- URSxxxxxxxxxx.sto
|   |__ rscape/
|       |-- *.cyk.svg
|       |-- *.out
|       |__ and many more (...)
|__ ...

TODO:
Ex if there's no alignment in folder
Ex if there's more than one
Ex if there's already a rscape folder
"""

import glob
import os
import subprocess
import sys
# .............................FUNCTIONS...................................


def run_rscape(rscape, alnali):
    """
    Runs RNAcode software, makes dir rnacode/ with results
    in the same dir than the input alignment
    """
    rscape_template = rscape + " --outdir %s"\
                               " --cyk"\
                               " %s"
    rscapedir = os.path.join(os.path.dirname(alnali), "rscape")
    os.mkdir(rscapedir)
    cmd = rscape_template % (rscapedir,
                             alnali)
    subprocess.call(cmd, shell=True)


def iterdir(dir_path):
    """
    Makes iteration of main function in a directory containing
    directories with an alignment inside.
    """
    for folder in glob.glob(os.path.join(dir_path, '*')):
        alignments = glob.glob(os.path.join(dir_path, folder, "*.sto"))
        for stoali in alignments:
            run_rscape(RSCAPE_PATH, stoali)

# .........................................................................

if __name__ == '__main__':
    RSCAPE_PATH = sys.argv[1]
    DIR_PATH = sys.argv[2]
    iterdir(DIR_PATH)
