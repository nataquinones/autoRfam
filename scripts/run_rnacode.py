"""
DESCRIPTION:
Runs RNAcode software for a batch of stockholm files.
(Uses esl-reformat to convert .sto to clustal alignment)
Designed to run on a tree like:

dir/
|-- URSxxxxxxxxxx
|   |__ URSxxxxxxxxxx.sto
|__ ...

Producing:

dir/
|-- URSxxxxxxxxxx
|   |-- URSxxxxxxxxxx.sto
|   |-- URSxxxxxxxxxx.aln
|   |__ rnacode/
|       |-- rnacode.out
|       |__ hss-0.eps (...)
|__ ...
"""
import glob
import os
import subprocess
import sys
# .............................FUNCTIONS...................................


def convert_stotoclustal(eslreformat, stoali):
    """
    Takes .sto format alignment and writes clustal .aln
    alignment with same basename in same dir
    """
    eslreformat_template = eslreformat + " --replace .:-"\
                                         " --informat stockholm"\
                                         " -d"\
                                         " -o"\
                                         " %s.aln"\
                                         " clustal" \
                                         " %s"
    basename = os.path.splitext(stoali)[0]
    cmd = eslreformat_template % (basename, stoali)
    subprocess.call(cmd, shell=True)
    return "%s.aln" % (basename)


def run_rnacode(rnacode, alnali):
    """
    Runs RNAcode software, makes dir rnacode/ with results
    in the same dir than the input alignment
    """
    rnacode_template = rnacode + " --eps-dir %s"\
                                 " --outfile %s"\
                                 " --eps"\
                                 " %s"
    rnacodedir = os.path.join(os.path.dirname(alnali), "rnacode")
    os.mkdir(rnacodedir)
    cmd = rnacode_template % (rnacodedir,
                              os.path.join(rnacodedir, "rnacode.out"),
                              alnali)
    subprocess.call(cmd, shell=True)


def main(eslreformat, rnacode, stoali):
    """
    Integrates both functions
    """
    alnali = convert_stotoclustal(eslreformat, stoali)
    run_rnacode(rnacode, alnali)


def iterdir(eslreformat, rnacode, dir_path):
    """
    Makes iteration of main function in a directory containing
    directories with an alignment inside.
    """
    for folder in glob.glob(os.path.join(dir_path, '*')):
        alignments = glob.glob(os.path.join(dir_path, folder, "*.sto"))
        for stoali in alignments:
            main(eslreformat, rnacode, stoali)
            with open(os.path.join(dir_path, "rnacode.log"), "a") as logfile:
                logfile.write(stoali+"\n")

# .........................................................................

if __name__ == '__main__':
    ESLREF_PATH = sys.argv[1]
    RNACODE_PATH = sys.argv[2]
    DIR_PATH = sys.argv[3]
    iterdir(ESLREF_PATH, RNACODE_PATH, DIR_PATH)
