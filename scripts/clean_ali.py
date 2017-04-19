import os
import pandas as pd
import shutil
import sys


def read_csv(tbl_file):
    # read tsv table into pandas df
    df_tbl = pd.read_csv(tbl_file, sep="\t")
    return df_tbl


def cleanup(df_tbl, ali_path, selali_path):
    """
    """
    os.mkdir(selali_path)
    # select unmarked sequences to delete
    df_todel = df_tbl[df_tbl["selected"] != "*"]
    # select seq_names to delete lines, in and out file names
    for urs in set(df_todel["query"]):
        bad_seqs = df_todel[df_todel["query"] == urs]["seq_name"].tolist()
        ali_file = ali_path + urs + ".sto"
        clean_ali_file = selali_path + urs + ".cl.sto"
        # process to delete lines with bad seqs
        with open(ali_file) as oldfile, open(clean_ali_file, 'w') as newfile:
            for line in oldfile:
                if not any(seq in line for seq in bad_seqs):
                    newfile.write(line)

    # select files that need no modifications to copy
    to_move = set(df_tbl["query"]) - set(df_todel["query"])
    for urs in to_move:
        move_from = ali_path + urs + ".sto"
        move_to = selali_path + urs + ".sto"
        shutil.copy(move_from, move_to)


def main(tbl_file, ali_path, selali_path):
        df_tbl = read_csv(tbl_file)
        cleanup(df_tbl, ali_path, selali_path)


# .........................................................................

if __name__ == '__main__':
    TBL_FILE = sys.argv[1]
    ALI_PATH = sys.argv[2]
    SEL_ALI_PATH = sys.argv[3]
    main(TBL_FILE, ALI_PATH, SEL_ALI_PATH)
