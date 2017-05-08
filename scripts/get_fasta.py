"""
Description:
Takes file of RNAcentral URSs, fetches the sequences in .fasta format from
RNAcentral API. and saves them into file.

Use:
get_fasta.py <in> <out>

<in>: Input list of non species-specific RNAcentral URSs, one per line
<out>: Output .fasta file
"""

import requests
import sys

# .............................FUNCTIONS...................................


def fasta_seq(txtfile, fastafile):
    """
    Fetches FASTA format sequences from .txt file of RNAcentral URSs.

    txtfile: input .txt with RNAcentral URS, one per line
    fastafile: output .fasta file with sequences
    """

    # read txt file as list
    urs_list = open(txtfile).read().splitlines()
    # open file to write output
    handle = open(fastafile, "w")

    # fetch each element of the list from RNAcentral API and write file
    for i in urs_list:
        url = ("http://rnacentral.org/api/v1/rna/%s?format=fasta") % i
        req = requests.get(url, timeout=60)
        handle.write(req.content)

    # close file
    handle.close()

# .........................................................................

if __name__ == '__main__':
    fasta_seq(sys.argv[1], sys.argv[2])
