"""
Description:
Takes nhmmer --tblout and process it into .tsv file to be used for
networkx processing.

Use:
nhmmertbl_parse.py <in> <out>
<in> input NHMMER --tbl output
<out> output .tsv file
"""

import re
import sys
import pandas as pd

# .............................FUNCTIONS...................................


def parse_nhmmer(nhmmertbl):
    """
    Takes NHMMER table output (option --tblout) and parses
    it into pandas df.
    ---
    nhmmertbl: nhmmer output --tblout file
    """
    df_tbl = pd.read_table(
        nhmmertbl,
        comment="#",
        engine="python",
        sep=r"\s*|-\n",
        index_col=False,
        header=None,
        usecols=range(14)
        )
    columns_dict = {0: "target",
                    1: "t_accession",
                    2: "query",
                    3: "q_accession",
                    4: "hmmfrom",
                    5: "hmmto",
                    6: "alifrom",
                    7: "alito",
                    8: "envfrom",
                    9: "envto",
                    10: "sqlen",
                    11: "strand",
                    12: "e_value",
                    13: "score",
                    14: "bias"}
    df_tbl = df_tbl.rename(columns=columns_dict)
    return df_tbl


def clean_selfhits(nhmmertbl, tsvout):
    """
    Takes nhmmer --tblout, keeps only significant hits, removes
    lines of queries that only have self-hits. Saves relevant
    columns in .tsv file.
    ---
    nhmmertbl: nhmmer --tblout
    tsvout: output .tsv file
    """
    df_tbl = parse_nhmmer(nhmmertbl)
    # clean
    df_tbl = df_tbl[df_tbl["e_value"] < 0.01]
    df_tbl = df_tbl[["query", "target", "alifrom", "alito"]]
    # make output file
    handlew = open(tsvout, 'w')
    handlew.write("query\ttarget\talifrom\talito\n")
    handlew.close()
    # remove queries with only self-hits
    for urs in set(df_tbl["query"]):
        if len(df_tbl[df_tbl["query"] == urs]) != 1:
            if set([urs]) != set((df_tbl[df_tbl["query"] == urs])["target"]):
                handlea = open(tsvout, 'a')
                targtbl = str(df_tbl[df_tbl["query"] == urs].to_string(header=False, index=False))
                # bad trick to re-format string
                targtbl = re.sub("\n", "#n", targtbl)
                targtbl = re.sub("\s+", "\t", targtbl)
                targtbl = re.sub("#n", "\n", targtbl)
                targtbl = targtbl + "\n"
                handlea.write(targtbl)
                handlea.close()

# .........................................................................

if __name__ == '__main__':
    IN_NHMMMERTBL = sys.argv[1]
    OUT_TSV = sys.argv[2]
    clean_selfhits(IN_NHMMMERTBL, OUT_TSV)
