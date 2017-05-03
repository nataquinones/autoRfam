"""
Description:
Takes .tsv file with columns "query" and "target"
(made for nhmmertbl_parse.py output) and gives a .tsv file of the of the
sequences to remove from alignments
Use:
marktoclean.py <in> <out>
<in> .tsv file with columns "query" and "target"
<out> .tsv file with sequences marked for deletion
"""

import sys
import pandas as pd

# .............................FUNCTIONS...................................


def read_tsv(tsvin):
    """
    Read tsv file into pandas df
    """
    df_tbl = pd.read_csv(tsvin, sep="\t", index_col=False)
    return df_tbl


def add_len(df_tbl):
    """
    MODIFIES dataframe f to add "name" column which is made of the
    target name, alifrom and alito. Adds empty "selected" column.
    """
    df_tbl["seqalen"] = abs(df_tbl["alifrom"] - df_tbl["alito"])
    df_tbl["seq_name"] = df_tbl["target"] + \
                         "/" + \
                         df_tbl["alifrom"].map(str) + \
                         "-" + \
                         df_tbl["alito"].map(str)
    df_tbl["selected"] = None
    return df_tbl


def markbest_perquery(df_tbl, report=False):
    """
    Makes df with * mark on the sequence to keep.
    If you want to write a file checking the progress of this process
    add the path as a second argument like:
    markbest_perquery(df_tbl, "./marktoclean_progress.txt")
    """
    df_bestmark = df_tbl.copy()
    count = 1
    for i in set(df_bestmark["query"]):
        allseqs = df_bestmark[df_bestmark["query"] == i]["target"]
        if len(allseqs) == len(set(allseqs)):
            df_bestmark.set_value((allseqs.index.tolist()), "selected", "*")
        else:
            for j in set(df_bestmark[df_bestmark["query"] == i]["target"]):
                repeats = df_bestmark[(df_bestmark["query"] == i) & (df_bestmark["target"] == j)]
                nonred = repeats.nlargest(1, "seqalen")
                df_bestmark.set_value((nonred.index.tolist()[0]), "selected", "*")
        if report != False:
            out = "query %d of %d \n" % (count, len(set(df_bestmark["query"])))
            handle = open(report, 'a')
            handle.write(out)
            handle.close()
            count = count + 1
    df_bestmark = df_bestmark[["query", "seq_name", "selected"]]
    df_bestmark.columns = (["alignment", "sequence", "keep"])
    return df_bestmark


def main(tsvin, tsvout):
        df_tbl = read_tsv(tsvin)
        add_len(df_tbl)
        df_bestmark = markbest_perquery(df_tbl)
        df_bestmark.to_csv(tsvout, sep='\t', index=False)
        return df_bestmark

# .........................................................................

if __name__ == '__main__':
    IN_TSV = sys.argv[1]
    OUT_TSV = sys.argv[2]
    OUT_DF = main(IN_TSV, OUT_TSV)