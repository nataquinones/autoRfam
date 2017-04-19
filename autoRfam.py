import sys
import os
from scripts import get_fasta
from scripts import nhmmerall
from scripts import cluster_ali

# .............................PATHS...................................
# ..........software..........
NHMMER_PATH = "/Users/nquinones/Documents/hmmer-3.1b2/binaries/nhmmer"
# ..........files..........
# step 1
URS_FILE = sys.argv[1]
FASTA_FILE = os.path.join(os.path.dirname(URS_FILE), "all_sequences.fasta")
# step 2
NHMMER_OUT_FOLDER = os.path.join(os.path.dirname(URS_FILE), "nhmmer_results/")
NHMMER_OUT_FILESNAMES = "nhmmer"
NHMMER_PARSEDNCLEAN = os.path.join(NHMMER_OUT_FOLDER, "clean_hits.tsv")
# step 3
COMPONENTS_OUT = os.path.splitext(NHMMER_PARSEDNCLEAN)[0] + ".comp.list"
ALI_DIR = os.path.join(NHMMER_OUT_FOLDER, "all_ali/")


# .............................FUNCTIONS...................................


def main():
    # step 1
    get_fasta.main(URS_FILE, FASTA_FILE)
    # step 2
    nhmmerall.main(NHMMER_PATH, FASTA_FILE, NHMMER_OUT_FOLDER, NHMMER_OUT_FILESNAMES, NHMMER_PARSEDNCLEAN, ALI_DIR)
    # step 3
    comp_list = cluster_ali.main(NHMMER_PARSEDNCLEAN)
    print comp_list

# .........................................................................
if __name__ == '__main__':
    main()
