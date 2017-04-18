"""
Description:
Takes a single column .txt file with one non-species specific RNAcentral URS
per line and write a fasta file with the sequences.
"""

import requests
import pandas as pd
import sys

# .............................FUNCTIONS...................................


def tabletolist(tsvtbl):
    """
    Takes single column txt file and
    makes it a python list
    """
    urs_df = pd.read_table(
        tsvtbl,
        header=None)
    urs_list = urs_df[0].tolist()
    return urs_list


def fasta_seq(urs_list, outfile):
    """
    Fetches FASTA format sequences
    from a python list of RNAcentral URSs
    """
    out_file = open(outfile, "w")
    for i in urs_list:
        url = ("http://rnacentral.org/api/v1/rna/" +
               i +
               "?format=fasta")
        req = requests.get(url, timeout=30)
        out_file.write(req.content)
    out_file.close()


def main(urs_file, fasta_file):
    lista = tabletolist(urs_file)
    fasta_seq(lista, fasta_file)

# .........................................................................

if __name__ == '__main__':
    URS_FILE = sys.argv[1]
    FASTA_FILE = sys.argv[2]
    main(URS_FILE, FASTA_FILE)
