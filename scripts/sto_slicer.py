"""
Description:
Takes concatenated stockholm file and slices it into individual .sto
files named after the first sequence in the alignment. Tested on
NHMMER's -A output.

Use:
sto_slicer.py <in>
<in> input concatenated .sto file
"""

import os
import re
import sys

# .............................FUNCTIONS...................................


def slice_sto(stofile):
    """
    Takes concatenated stockholm file and slices it
    into individual .sto files named after the first sequence
    in the alignment
    ---
    stofile: concatenated stockholm file from NHMMER -A
    out_dir: directory were individual files will be saved
    """
    # open and read alignment
    out_dir = "all_alignments"
    os.mkdir(out_dir)
    ali = open(stofile)
    alicontent = ali.read()
    commpatt = re.compile(r"#=GR.*\n")
    alicontent = commpatt.sub("", alicontent)
    commpatt2 = re.compile(r"#=GC PP_cons.*\n")
    alicontent = commpatt2.sub("", alicontent)
    commpatt3 = re.compile(r"#=GC RF.*\n")
    alicontent = commpatt3.sub("", alicontent)
    # pattern to identify end of alignment, split
    endpatt = re.compile("\/\/\n")
    filelist = endpatt.split(alicontent)
    # pattern to get first sequence aka query, list names
    namepatt = re.compile(r'\n\nURS.{10}')
    names = []
    for i in range(0, len(filelist) - 1):
        eachname = namepatt.findall(filelist[i])
        names.append(eachname[0])
    # clean name
    bad = re.compile("\n\n")
    for i in range(0, len(names)):
        names[i] = bad.sub("", names[i])
    # add extension
    names = [s + ".sto" for s in names]
    # write files
    for i in range(0, len(filelist) - 1):
        seqinfofile = open(os.path.join(out_dir, names[i]), 'w')
        seqinfofile.write(filelist[i])
        seqinfofile.write("//")
        seqinfofile.close()

# .........................................................................

if __name__ == '__main__':
    STOFILE = sys.argv[1]
    slice_sto(STOFILE)
