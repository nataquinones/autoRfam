"""
Description:
Takes directory with .sto alignments and a list of connected components that
groups them (list of lists in pickle format). With this information, it
runs esl-alistat on each alignment and selects the best per group. It makes
a new directory with the selected alignments.

Use:
pick_repali.py <alistat> <picklelist> <in_alipath> \
               <out_eslgroups> <out_selalipath>

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
    Reads pickle list file, returns python list.

    pickle_file: path to pickle list file with list of lists
    of connected components (from cluster_ali.find_components)
    """
    with open(pickle_file, 'rb') as handle:
        components_l = pickle.load(handle)

    return components_l


def easel_stats(eslalistat, ali_path):
    """
    Calculates alignment statistics with esl-alistat for all the
    alignments in a given path. Returns dataframe with alignment stats.

    eslalistat: path to esl-alistat software
    ali_path: dir with .sto alignemnt files
    """

    # new dataframe, add column with file names ["file"] and
    # column ["name"] with file name with no extension
    alistat_df = pd.DataFrame()
    alistat_df["file"] = os.listdir(ali_path)
    alistat_df["name"] = alistat_df["file"].str.replace(r"[.].*", "")

    # Run esl-alistat on each file (taken from the dataframe), as subprocess
    for i in range(0, len(alistat_df)):
        cmd = eslalistat + " --rna %s%s" % (ali_path, alistat_df["file"][i])
        result = os.popen(cmd).readlines()
        # make list and append values from subprocess
        values = []
        for line in result:
            values.append(line.split()[-1])
        # from list, select and format relevant information
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
    # add results to dataframe
    alistat_df["num_seq"] = alistat_df["num_seq"].astype(int)
    alistat_df["alen"] = alistat_df["alen"].astype(int)
    alistat_df["diff"] = alistat_df["diff"].astype(int)
    alistat_df["lenalen_ratio"] = alistat_df["lenalen_ratio"].round(2)
    alistat_df["avid"] = alistat_df["avid"].astype(int)

    return alistat_df


def mark_w_groups(components_l, alistat_df):
    """
    Appends group membership to dataframe with alignment stats. Returns
    dataframe with new column.

    components_l: python list of lists of connected components
    (from pick_repali.read_picklelist)
    alistat_df: dataframe with alignment stats (from pick_repali.easel_stats)
    """
    # make copy of dataframe
    groups_df = alistat_df.copy()

    # iterate over each line of dataframe
    for i in range(0, len(groups_df)):

        # for each line, take the name of the alingment, check if it is in a
        # sublist of components_l, and add index of sublist on column ["group"]
        # all the alignments in a same sublist will belong to the same group
        for sublist in components_l:
            if groups_df["name"][i] in sublist:
                groups_df.set_value(i, "group", components_l.index(sublist))
    groups_df["group"] = groups_df["group"].astype(int)
    # rename rearrange columns ?
    groups_df = groups_df[["group",
                           "name",
                           "num_seq",
                           "alen",
                           "diff",
                           "avlen",
                           "lenalen_ratio",
                           "avid",
                           "file"]]
    # delete name column, since it's no longer needed
    del groups_df["name"]
    # rename rearrange columns ?
    groups_df = groups_df[["group",
                           "file",
                           "num_seq",
                           "alen",
                           "diff",
                           "avlen",
                           "lenalen_ratio",
                           "avid"]]
    # sort dataframe
    groups_df = groups_df.sort_values(["group", "num_seq", "lenalen_ratio"],
                                      ascending=[1, 0, 0])
    # remove index
    groups_df = groups_df.reset_index(drop=True)

    return groups_df


def select_ali(groups_df):
    """
    Selects best alignment of each group, returns dataframe including
    only the selected alignment.

    groups_df: Dataframe with alignment statistics and group membership
    (from pick_repali.mark_w_groups)
    """
    # sort dataframe
    selected_df = groups_df.copy()
    # only keep alignments with less than 40% gaps
    selected_df = selected_df[selected_df["lenalen_ratio"] > 0.40]
    # only keep alignments with less than 100% id
    selected_df = selected_df[selected_df["avid"] < 100]
    # sort based on group, num_seq and then lenalen_ratio
    selected_df = selected_df.sort_values(["group",
                                           "num_seq",
                                           "lenalen_ratio"],
                                          ascending=[1, 0, 0])
    # keep top 3 alignments per group with current sort
    selected_df = selected_df.groupby("group").head(3)
    # re-sort based on lenalen_ratio
    selected_df = selected_df.sort_values(["group", "lenalen_ratio"],
                                          ascending=[1, 0])
    # keep top 1
    selected_df = selected_df.drop_duplicates(["group"])
    # clean: keep only "group" and "file" columns
    selected_df = selected_df[["group", "file"]]
    selected_df = selected_df.reset_index(drop=True)

    return selected_df


def fetch_selected(ali_path, selected_df, selali_path):
    """
    Takes the dataframe of selected alignments, makes new folders and makes
    copies of them into a folder.

    ali_path: path to folder with original alignments
    selected_df: dataframe with selected alignments
    (from pick_repali.select_ali)
    selali_path: path to destination folder for selected alignments
    """
    os.mkdir(selali_path)

    for i in selected_df["file"]:
        aliname = i.split(os.extsep, 1)[0]
        selfdir = os.path.join(selali_path, aliname)
        os.mkdir(selfdir)
        move_from = os.path.join(ali_path, i)
        move_to = os.path.join(selfdir, i)
        shutil.copy(move_from, move_to)


def main(eslalistat, pickle_file, ali_path, groupstsv, selali_path):
    """
    Integrates all functions. Given a folder with stockholm files and a
    pickle list that groups them into clusters, selects the best alignment
    per group and makes a new folder with the selected alignments.

    eslalistat: path to esl-alistat software
    pickle_file: path to pickle list file with list of lists
    ali_path: dir with original .sto alignemnt files
    outgroupstsv: output tsv file with summary
    selali_path: path to destination folder for selected alignments
    """
    components_l = read_picklelist(pickle_file)
    alistat_df = easel_stats(eslalistat, ali_path)
    groups_df = mark_w_groups(components_l, alistat_df)
    selected_df = select_ali(groups_df)
    groups_df.to_csv(groupstsv,
                     sep='\t',
                     index=False)
    fetch_selected(ali_path, selected_df, selali_path)

# .........................................................................

if __name__ == '__main__':
    in_eslalistat = sys.argv[1]
    in_pickle_file = sys.argv[2]
    in_ali_path = sys.argv[3]
    out_groupstsv = sys.argv[4]
    out_selali_path = sys.argv[5]
    main(in_eslalistat, in_pickle_file, in_ali_path, out_groupstsv, out_selali_path)
