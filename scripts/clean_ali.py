"""
Description:
Takes .tsv file with sequences marked for deletion (from marktoclean.py) and
alignments directory. It deletes the specific sequences and makes a copy of
the alignments in a new directory called "clean_alignments".

Use:
clean_ali.py <in> <aligmentsdir>
<in> .tsv file with sequences marked for deletion
<aligmentsdir> directory with alignments to clean
"""

import os
import pandas as pd
import shutil
import sys


def read_tsv(tsvin):
    """
    Read tsv file into pandas df
    """
    df_tbl = pd.read_csv(tsvin, sep="\t")
    return df_tbl


def cleanup(df_tbl, allali_path, selali_path):
    """
    Takes df with sequences marked for deletion, cleans the alignment
    and makes a copy in directory "clean_alignments/"
    """
    os.mkdir(selali_path)
    # select unmarked sequences to delete
    df_todel = df_tbl[df_tbl["keep"] != "*"]
    # select sequence to delete lines, in and out file names
    for urs in set(df_todel["alignment"]):
        bad_seqs = df_todel[df_todel["alignment"] == urs]["sequence"].tolist()
        ali_file = os.path.join(allali_path, urs + ".sto")
        clean_ali_file = os.path.join(selali_path, urs + ".cl.sto")
        # process to delete lines with bad seqs
        with open(ali_file) as oldfile, open(clean_ali_file, 'w') as newfile:
            for line in oldfile:
                if not any(seq in line for seq in bad_seqs):
                    newfile.write(line)

    # select files that need no modifications to copy
    to_move = set(df_tbl["alignment"]) - set(df_todel["alignment"])
    for urs in to_move:
        move_from = os.path.join(allali_path, urs + ".sto")
        move_to = os.path.join(selali_path, urs + ".sto")
        shutil.copy(move_from, move_to)


def main(tsvin, allali_path, selali_path):
    df_tbl = read_tsv(tsvin)
    cleanup(df_tbl, allali_path, selali_path)

# .........................................................................

if __name__ == '__main__':
    IN_TSV = sys.argv[1]
    IN_ALLALIPATH = sys.argv[2]
    OUT_SELALIPATH = os.path.join(os.path.dirname(
                               os.path.dirname(IN_ALLALIPATH)),
                               "clean_alignments")
    main(IN_TSV, IN_ALLALIPATH, OUT_SELALIPATH)
