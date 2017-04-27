"""
Description:
Selects relevant alignments to build html info pages. It takes a connected
components list, analizes all the alignments with esl-stat and selects one
alignment per group. Returns a tsv file with the stats and group membership,
makes a folder with the selected alignments.

Use:
pick_repali.py <esl-alistat> <in_pickle_file> <in_alipath> <out_eslgroups> \
               <out_selalipath>
<esl-alistat> path to esl-alistat software
<picklelist> pickle list file with connected components (from cluster_ali.py)
<in_alipath> path to clean_alignments/ folder (from clean_ali.py)
<out_eslgroups> output .tsv file with alignments with easel stats and group
<out_selalipath> output folder to put selected alignments
"""

import os
import pandas as pd
import pickle
import shutil
import sys

# .............................FUNCTIONS...................................


def read_picklelist(pickle_file):
    """
    Reads pickle file list to python list
    """
    with open(pickle_file, 'rb') as handle:
        components_l = pickle.load(handle)

    return components_l


def easel_stats(eslalistat, ali_path):
    """
    Calculates alignments statistics with esl-alistat for all the
    alignments in a given path. Makes pandas dataframe with results.
    
    eslalistat: path to esl-alistat software
    ali_path: folder with alignemnts

    return: 
    """
    alistat_df = pd.DataFrame()
    alistat_df["file"] = os.listdir(ali_path)
    alistat_df["name"] = alistat_df["file"].str.replace(r"[.].*", "")

    for i in range(0, len(alistat_df)):
        cmd = eslalistat + " --rna %s%s" % (ali_path, alistat_df["file"][i])
        result = os.popen(cmd).readlines()
        values = []

        for line in result:
            values.append(line.split()[-1])

        num_seq = int(values[2])
        alen = int(values[3])
        diff = int(values[6]) - float(values[5])
        avlen = float(values[7])
        lenalen_ratio = avlen / alen
        avid = int(values[8].strip("%"))
        alistat_df.set_value(i, "num_seq", num_seq)
        alistat_df.set_value(i, "alen", alen)
        alistat_df.set_value(i, "diff", diff)
        alistat_df.set_value(i, "avlen", avlen)
        alistat_df.set_value(i, "lenalen_ratio", lenalen_ratio)
        alistat_df.set_value(i, "avid", avid)

    alistat_df["num_seq"] = alistat_df["num_seq"].astype(int)
    alistat_df["alen"] = alistat_df["alen"].astype(int)
    alistat_df["diff"] = alistat_df["diff"].astype(int)
    alistat_df["lenalen_ratio"] = alistat_df["lenalen_ratio"].round(2)
    alistat_df["avid"] = alistat_df["avid"].astype(int)
    
    return alistat_df


def mark_w_groups(components_l, alistat_df):
    """
    Appends group membership from list to alignment stats.
    """
    groups_df = alistat_df.copy()

    for i in range(0, len(groups_df)):

        for sublist in components_l:
            if groups_df["name"][i] in sublist:
                groups_df.set_value(i, "group", components_l.index(sublist))
    groups_df["group"] = groups_df["group"].astype(int)
    groups_df = groups_df[["group",
                           "name",
                           "num_seq",
                           "alen",
                           "diff",
                           "avlen",
                           "lenalen_ratio",
                           "avid",
                           "file"]]
    del groups_df["name"]
    groups_df = groups_df[["group",
                           "file",
                           "num_seq",
                           "alen",
                           "diff",
                           "avlen",
                           "lenalen_ratio",
                           "avid"]]

    groups_df = groups_df.sort_values(["group", "num_seq", "lenalen_ratio"],
                                      ascending=[1, 0, 0])
    groups_df = groups_df.reset_index(drop=True)
    return groups_df


def select_ali(groups_df):
    """
    Selects best alignment of group, returns pandas df.
    """
    selected_df = groups_df.sort_values(["group", "num_seq", "lenalen_ratio"],
                                        ascending=[1, 0, 0])
    # only alignments with less than 40% gaps
    selected_df = selected_df[selected_df["lenalen_ratio"] > 0.40]
    # .. only alignments with less than 100% id
    selected_df = selected_df[selected_df["avid"] < 100]
    # .. keep top 3
    selected_df = selected_df.groupby("group").head(3)
    # .. reorder based on lenalen_ratio
    selected_df = selected_df.sort_values(["group", "lenalen_ratio"],
                                          ascending=[1, 0])
    # .. keep top one
    selected_df = selected_df.drop_duplicates(["group"])
    # .. clean
    selected_df = selected_df[["group", "file"]]
    selected_df = selected_df.reset_index(drop=True)
    return selected_df


def fetch_selected(ali_path, selected_df, selali_path):
    """
    Takes the df of selected alignments, makes new folders and makes
    copies of them into a folder.

    """
    os.mkdir(selali_path)
    for i in selected_df["file"]:
        aliname = i.split(os.extsep, 1)[0]
        selfdir = os.path.join(selali_path, aliname)
        os.mkdir(selfdir)
        move_from = os.path.join(ali_path, i)
        move_to = os.path.join(selfdir, i)
        shutil.copy(move_from, move_to)

# .........................................................................

if __name__ == '__main__':
    # .....input.....
    EASELALISTAT = sys.argv[1]
    IN_PICKLE_FILE = sys.argv[2]
    IN_ALIPATH = sys.argv[3]
    OUT_ESLGROUPS = sys.argv[4]
    OUT_SELALIPATH = sys.argv[5]
    # .....process.....
    COMPONENTS_L = read_picklelist(IN_PICKLE_FILE)
    ALISTAT_DF = easel_stats(EASELALISTAT, IN_ALIPATH)
    GROUPS_DF = mark_w_groups(COMPONENTS_L, ALISTAT_DF)
    SELECTED_DF = select_ali(GROUPS_DF)
    # .....output....
    GROUPS_DF.to_csv(OUT_ESLGROUPS,
                     sep='\t',
                     index=False)
    fetch_selected(IN_ALIPATH, SELECTED_DF, OUT_SELALIPATH)
