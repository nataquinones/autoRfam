import sys
import pandas as pd


def read_csv(tbl_file):
    # read tsv table into pandas df
    df_tbl = pd.read_csv(tbl_file, sep="\t")
    return df_tbl


def add_len(df_tbl):
    """
    MODIFIES dataframe f to add "name" column which is made of the
    target name, alifrom and alito. Adds empty "selected" column.
    """
    seqalen = abs(df_tbl["alifrom"] - df_tbl["alito"])
    df_tbl["seqalen"] = seqalen
    df_tbl["seq_name"] = df_tbl["target"] + "/" + df_tbl["alifrom"].map(str) + "-" + df_tbl["alito"].map(str)
    df_tbl["selected"] = None
    return df_tbl


def markbest_perquery(df_tbl, tbl_out):
    """
    MODIFIES dataframe to mark with * the sequence to keep.
    -Uncomment lines to make file reporting progress
    """
    # m = 1
    for i in set(df_tbl["query"]):
        allseqs = df_tbl[df_tbl["query"] == i]["target"]
        if len(allseqs) == len(set(allseqs)):
            df_tbl.set_value((allseqs.index.tolist()), "selected", "*")
        else:
            for j in set(df_tbl[df_tbl["query"] == i]["target"]):
                repeats = df_tbl[(df_tbl["query"] == i) & (df_tbl["target"] == j)]
                nonred = repeats.nlargest(1, "seqalen")
                df_tbl.set_value((nonred.index.tolist()[0]), "selected", "*")
        # report = "query %d of %d \n" % (m, len(set(df_tbl["query"])))
        # f = open("./aliclean_prog.txt", 'a')
        # f.write(out)
        # f.close()
        # m = m + 1
    df_bestmark = df_tbl[["query", "seq_name", "selected"]]
    df_bestmark.to_csv(tbl_out, sep='\t', index=False)


def main(tbl_file, tbl_out):
        df_tbl = read_csv(tbl_file)
        df_tbl = add_len(df_tbl)
        markbest_perquery(df_tbl, tbl_out)

# .........................................................................

if __name__ == '__main__':
    TBL_FILE = sys.argv[1]
    TBL_OUT = sys.argv[2]
    main(TBL_FILE, TBL_OUT)
