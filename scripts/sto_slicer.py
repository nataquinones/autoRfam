"""
Description:
Takes a concatenated .sto file and slices it into all the individual
alignments, names them in based on the first sequence of alignment.

Use:
sto_slicer.py <in> <out_dir>

<in>: Input concatenated .sto file
<out_dir>: Directory where all the sliced .sto files will be saved
"""

import os
import re
import sys

# .............................FUNCTIONS...................................


def slice_sto(stofile, dirpath):
    """
    Takes a concatenated .sto file and slices it into all the individual
    alignments, names them in based on the first sequence of alignment.

    stofile: concatenated .sto file
    out_dir: directory where all the sliced .sto files will be saved
    """

    # make directory if it doesn't exist already
    if not os.path.exists(dirpath):
        os.mkdir(dirpath, 0777)
    # open stockholm file and read
    ali = open(stofile)
    alicontent = ali.read()

    # regex patterns:
    # Lines with #=GR or #=GC
    grgc_pattern = re.compile(r"#=G[RC].*\n")
    # Special digit and bar that nhmmer might append, #|
    digbar_pattern = re.compile(r"\d\|")
    # End of alignment, //
    end_pattern = re.compile(r"\/\/\n")
    # First sequence of each alignment
    name_pattern = re.compile(r'\n\nURS.{10}')

    # Use regex to clean lines
    alicontent = grgc_pattern.sub("", alicontent)
    alicontent = digbar_pattern.sub("", alicontent)

    # Use regex to split into indiv. alignments
    filelist = end_pattern.split(alicontent)
    # Remove last element because it splits into " "
    filelist.pop()
    # Add stockholm file end, //, at the end of each alignment
    filelist = [s + "//" for s in filelist]

    # Make 'names' list out of the first sequence of each alignment
    names = []
    for i in range(0, len(filelist)):
        eachname = name_pattern.findall(filelist[i])
        try:
            names.append(eachname[0])
        # it wont work if the name is not in URS format, use other name
        except IndexError:
            names.append("noURS_%s" % i)
    # clean the name to remove line breaks
    badnameprefix_pattern = re.compile("\n\n")
    for i in range(0, len(names)):
        names[i] = badnameprefix_pattern.sub("", names[i])
    # add extension to names
    names = [s + ".sto" for s in names]

    # write files
    for i in range(0, len(filelist)):
        handle = open(os.path.join(dirpath, names[i]), 'w')
        handle.write(filelist[i])
        handle.close()

# .........................................................................

if __name__ == '__main__':
    slice_sto(sys.argv[1], sys.argv[2])
