"""
Description:
Uses RNAcentral URSs to fetch sequences in FASTA format from RNAcentral API.

Use:
get_fasta.py <in> <out>
<in> input .txt with (non-species specific) RNAcentral URS, one per line
<out> output .fasta file with sequences
"""

import requests
import sys

# .............................FUNCTIONS...................................


def fasta_seq(txtfile, fastafile):
    """
    Fetches FASTA format sequences from txt file of RNAcentral URSs.
    txtfile: input .txt with RNAcentral URS, one per line
    fastafile: output .fasta file with sequences
    """
    urs_list = open(txtfile).read().splitlines()
    handle = open(fastafile, "w")
    for i in urs_list:
        url = ("http://rnacentral.org/api/v1/rna/%s?format=fasta") % i
        req = requests.get(url, timeout=60)
        handle.write(req.content)
    handle.close()

# .........................................................................

if __name__ == '__main__':
    IN_TXT = sys.argv[1]
    OUT_FASTA = sys.argv[2]
    fasta_seq(IN_TXT, OUT_FASTA)
