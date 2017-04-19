import os
import pandas as pd
import pickle
import sys

# .............................FUNCTIONS...................................


def read_picklelist(pickle_file):
    """
    """
    with open(pickle_file, 'rb') as f:
        comp = pickle.load(f)
    return comp


def easel_stats(comp, easelalistat, ali_path):
    """
    """
    info_table = pd.DataFrame()
    info_table["file"] = os.listdir(ali_path)
    info_table["name"] = info_table["file"].str.replace(r"[.].*", "")
    for i in range(0, len(info_table)):
        ex_string = "%s --rna %s%s" % (easelalistat, ali_path, info_table["file"][i])
        b = os.popen(ex_string).readlines()
        values = []
        for line in b:
            values.append(line.split()[-1])
        num_seq = int(values[2])
        alen = int(values[3])
        diff = int(values[6]) - float(values[5])
        avlen = float(values[7])
        lenalen_ratio = avlen / alen
        avid = int(values[8].strip("%"))
        info_table.set_value(i, "num_seq", num_seq)
        info_table.set_value(i, "alen", alen)
        info_table.set_value(i, "diff", diff)
        info_table.set_value(i, "avlen", avlen)
        info_table.set_value(i, "lenalen_ratio", lenalen_ratio)
        info_table.set_value(i, "avid", avid)

    for i in range(0, len(info_table)):
        for sublist in comp:
            if info_table["name"][i] in sublist:
                info_table.set_value(i, "group", comp.index(sublist))

    info_table["num_seq"] = info_table["num_seq"].astype(int)
    info_table["alen"] = info_table["alen"].astype(int)
    info_table["diff"] = info_table["diff"].astype(int)
    info_table["group"] = info_table["group"].astype(int)

    info_table = info_table[["group", "name", "num_seq", "alen", "diff", "avlen", "lenalen_ratio", "avid", "file"]]
    info_table = info_table.sort_values(["num_seq", "lenalen_ratio"], ascending=[0, 0])
    return info_table


def make_summary(df_tbl):
    sorted_df = df_tbl.sort_values(["group", "num_seq", "lenalen_ratio"], ascending=[1, 0, 0])
    # make summary
    summary_df = pd.DataFrame()
    for group in set(sorted_df["group"]):
        sub = sorted_df[sorted_df["group"] == group]
        mems = len(sub)
        mean = sub.num_seq.mean()
        maxi = sub.num_seq.max()
        mini = sub.num_seq.min()
        rat = sub.lenalen_ratio.mean()
        line = [[group, mems, mean, maxi, mini, rat]]
        summary_df = summary_df.append(line)
    summary_df.columns = ["group", "members", "avg_numseq", "max_numseq", "min_numseq", "alenrat"]
    summary_df = summary_df.set_index(["group"], drop=True)
    return summary_df


def select_ali(df_tbl):
    selected = df_tbl.sort_values(["group", "num_seq", "lenalen_ratio"], ascending=[1, 0, 0])
    # .. only alignments with less than 40% gaps
    selected = selected[selected["lenalen_ratio"] > 0.40]
    # .. only alignments with less than 100% id
    selected = selected[selected["avid"] < 100]
    # .. keep top 3
    selected = selected.groupby("group").head(3)
    # .. reorder based on lenalen_ratio
    selected = selected.sort_values(["group", "lenalen_ratio"], ascending=[1, 0])
    # .. keep top one
    selected = selected.drop_duplicates(["group"])
    selected = selected.set_index(["group"], drop=True)
    return selected


def join_summsel(summary_df, selected_df, info_table):
    joined = pd.concat([selected_df, summary_df], axis=1, join='inner')
    joined["lenalen_ratio"] = joined["lenalen_ratio"].round(2)
    joined["avg_numseq"] = joined["avg_numseq"].round(2)
    joined["alenrat"] = joined["alenrat"].round(2)
    # full table
    sel_ali_tbl = joined[["file", "num_seq", "alen", "avlen", "lenalen_ratio", "avid"]]
    sel_ali_tbl.reset_index(level=0, inplace=True)
    sel_ali_tbl.to_csv("./selali.tsv", sep="\t", index=False)
    sel_ali_tbl["file"].to_csv("./selali.txt", sep="\t", index=False)
    # group relation table
    groups_tbl = info_table[["group", "file"]].sort_values(["group"])
    groups_tbl.to_csv("./groups_info.tsv", sep="\t", index=False)


def main():
    """
    """
    comp = read_picklelist(PICKLE_FILE)
    info_tbl = easel_stats(comp, EASELALISTAT, ALIPATH)
    summary_df = make_summary(info_tbl)
    selected = select_ali(info_tbl)
    join_summsel(summary_df, selected, info_tbl)
# .........................................................................

if __name__ == '__main__':
    PICKLE_FILE = sys.argv[1]
    EASELALISTAT = sys.argv[2]
    ALIPATH = sys.argv[3]
    main()
