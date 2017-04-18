"""
USE:
python nhmmerall.py <fasta>

Description:
Takes fasta file, searches all vs. all with nhmmer.
Does several things with the outputs:
.tbl: Parses output to pandas table
.tbl: Removes queries with only self-hits.
.sto: Slices file into individual stockholm files
"""

import os
import pandas as pd
import re
import subprocess
import sys

# .............................FUNCTIONS...................................


def nhmmer_allvsall(nhmmer_path, fasta, out_dir, name):
    """
    Runs NHMMER as a subprocess. With options:
    -o: save output file
    -A: generate alignment of significant hits
    --tblout: output in tbl format
    --noali: remove alignments from general output
    --rna: for RNA sequences
    --tformat: Target format in FASTA
    --qformat: Query format in FASTA
    Uses same file as target and query, so it's all vs. all.
    ---
    nhmmer_path: path to nhmmer software
    fasta: fasta file with sequences to be used as query and target
    out_dir: directory where all the output goes
    name: name of the output files
    """
    nhmmer_template = nhmmer_path + " -o %s.out -A %s.sto --tblout %s.tbl --noali --rna --tformat fasta --qformat fasta %s %s"
    os.mkdir(out_dir)
    out_file = os.path.join(out_dir, name)
    cmd = nhmmer_template % (out_file, out_file, out_file, fasta, fasta)
    subprocess.call(cmd, shell=True)
    return "%s.tbl" % out_file, "%s.sto" % out_file


def parsetbl(tbl):
    """
    Takes NHMMER table output (option --tblout) and makes
    parsed tsv table.
    ---
    tbl: nhmmer output *.tbl file
    """
    df_tbl = pd.read_table(
        tbl,
        comment="#",
        engine="python",
        sep=r"\s*|-\n",
        index_col=False,
        header=None,
        usecols=range(14)
        )
    # select relevant columns only
    df_tbl = df_tbl[[2, 0, 6, 7, 12, 13]]
    df_tbl.columns = ['query', 'target', 'alifrom', 'alito', 'e_value', 'score']
    # leave only rows with sig values
    df_tbl = df_tbl[df_tbl["e_value"] < 0.01]
    # save tsv file
    pars_tbl = os.path.splitext(tbl)[0] + ".p" + os.path.splitext(tbl)[1]
    df_tbl.to_csv(pars_tbl, sep='\t', index=False)
    return pars_tbl, df_tbl


def clean_selfhits(par_tbl, out):
    """
    Takes pandas dataframe from parsed NHMMER table (*.p.tbl)
    and removes lines of queries that only have self-hits.
    ---
    par_tbl: pandas dataframe with parsed table
    out: output .tsv file
    """
    # make output file
    f = open(out, 'w')
    f.write("query\ttarget\talifrom\talito\te_value\tscore\n")
    f.close()
    # write
    for urs in set(par_tbl["query"]):
        if len(par_tbl[par_tbl["query"] == urs]) != 1:
            if set([urs]) != set((par_tbl[par_tbl["query"] == urs])["target"]):
                f = open(out, 'a')
                targtbl = str(par_tbl[par_tbl["query"] == urs].to_string(header=False, index=False))
                targtbl = re.sub("\n", "#n", targtbl)
                targtbl = re.sub("\s+", "\t", targtbl)
                targtbl = re.sub("#n", "\n", targtbl)
                targtbl = targtbl + "\n"
                f.write(targtbl)
                f.close()


def slice_sto(stofile, out_dir):
    """
    Takes concatenated stockholm file and slices it
    into individual .sto files named after the first sequence
    in the alignment
    ---
    stofile: concatenated stockholm file
    out_dir: firectory were individual files will be saved
    """
    # open and read alignment
    os.mkdir(out_dir)
    ali = open(stofile)
    alicontent = ali.read()
    commpatt = re.compile(r"#=GR.*\n")
    alicontent = commpatt.sub("", alicontent)
    commpatt2 = re.compile(r"#=GC PP_cons.*\n")
    alicontent = commpatt2.sub("", alicontent)
    commpatt3 = re.compile(r"#=GC RF.*\n")
    alicontent = commpatt3.sub("", alicontent)
    # pattern to identify end of alignment, split
    endpatt = re.compile("\/\/\n")
    filelist = endpatt.split(alicontent)
    # pattern to get first sequence aka query, list names
    namepatt = re.compile(r'\n\nURS.{10}')
    names = []
    for i in range(0, len(filelist) - 1):
        eachname = namepatt.findall(filelist[i])
        names.append(eachname[0])
    # clean name
    bad = re.compile("\n\n")
    for i in range(0, len(names)):
        names[i] = bad.sub("", names[i])
    # add extension
    names = [s + ".sto" for s in names]
    # write files
    for i in range(0, len(filelist) - 1):
        seqInfoFile = open(os.path.join(out_dir, names[i]), 'w')
        seqInfoFile.write(filelist[i])
        seqInfoFile.write("//")
        seqInfoFile.close()


def main(nhmmer_path, fasta, out_dir, name, parsedclean, ali_dir):
    """
    Integrates nhmmer scan, parsing, cleanup and stockholm file slicing.
    """
    nhmmer = nhmmer_allvsall(nhmmer_path, fasta, out_dir, name)
    tbl_file = nhmmer[0]
    sto_file = nhmmer[1]
    pars_tbl = parsetbl(tbl_file)
    clean_selfhits(pars_tbl[1], parsedclean)
    slice_sto(sto_file, ali_dir)

# .........................................................................

if __name__ == '__main__':
    NHMMER_PATH = "/Users/nquinones/Documents/hmmer-3.1b2/binaries/nhmmer"
    FASTA_FILE = sys.argv[1]
    NHMMER_OUT_FOLDER = os.path.join(os.path.dirname(FASTA_FILE), "nhmmer_results")
    NHMMER_OUT_FILESNAMES = "nhmmer"
    NHMMER_PARSEDNCLEAN = os.path.join(NHMMER_OUT_FOLDER, "clean_hits.tsv")
    ALI_DIR = os.path.join(NHMMER_OUT_FOLDER, "all_ali/")
    main(NHMMER_PATH, FASTA_FILE, NHMMER_OUT_FOLDER, NHMMER_OUT_FILESNAMES, NHMMER_PARSEDNCLEAN, ALI_DIR)
