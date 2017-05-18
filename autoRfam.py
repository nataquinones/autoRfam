# ........................IMPORT GENERAL MODULES..............................
import argparse
import luigi
import os
import shutil
import sys
# ........................IMPORT PROJECT MODULES..............................
from scripts import get_fasta
from scripts import nhmmer_allvsall
from scripts import sto_slicer
from scripts import nhmmertbl_parse
from scripts import marktoclean
from scripts import cluster_ali
from scripts import clean_ali
from scripts import pick_repali
from scripts import run_rscape
from scripts import run_rnacode
from scripts import all_html
import templates

# ......................SETUP AND ARGUMENT PARSER............................

# .......... main argument parser
parser = argparse.ArgumentParser()
parser.add_argument("input_urs",
                    metavar='<ursfile>',
                    help="")
parser.add_argument("-e", "--env",
                    metavar='<s>',
                    help="""<s> can be <local>, <docker> or <lsf>. \
                          Select to import paths from appropriate \
                          file in config/. Default setting is <local>.""",
                    type=str,
                    default="local")
parser.add_argument("-o", "--outdir",
                    metavar='<dir>',
                    help="""<dir> is the path to the directory which will be created
                            in which the whole pipeline output will be saved. \
                            If argument not specified, it will create it in the
                            /path/to/<ursfile>/autoRfam_<ursfile>""",
                    default="default_dir",
                    type=str)

args = parser.parse_args()


# .......... conditional import of config/paths_*.py file
if args.env == "local":
    from config import paths_local as paths
elif args.env == "docker":
    from config import paths_docker as paths
elif args.env == "lsf":
    from config import paths_lsf as paths
else:
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# autoRfam"
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# Invalid -e: Please select a valid option."
    print "# Must be: local, docker or lsf."
    print "#"
    print "# For help: autoRfam.py -h"
    print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    sys.exit(1)


# .......... import and check of config paths
# nhmmer
if os.path.exists(paths.nhmmerpath) & (os.path.basename(paths.nhmmerpath) == "nhmmer"):
    NHMMERPATH = paths.nhmmerpath
else:
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# autoRfam"
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# Can't find: nhmmer"
    print "# I'm looking for '%s' as indicated in '%s'" % (paths.nhmmerpath, paths.__file__)
    if (os.path.basename(paths.nhmmerpath) != "nhmmer"):
        print "# The basename is '%s', but I expect it to be 'nhmmer'." % os.path.basename(paths.nhmmerpath)
    else:
        print "# Try selecting the correct -e option or ammending this config file."
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    sys.exit(1)

# esl-alistat
if os.path.exists(paths.eslalistat) & (os.path.basename(paths.eslalistat) == "esl-alistat"):
    ESLALISTAT = paths.eslalistat
else:
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# autoRfam"
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# Can't find: esl-alistat"
    print "# I'm looking for '%s' as indicated in '%s'" % (paths.eslalistat, paths.__file__)
    if (os.path.basename(paths.eslalistat) != "esl-alistat"):
        print "# The basename is '%s', but I expect it to be 'esl-alistat'." % os.path.basename(paths.eslalistat)
    else:
        print "# Try selecting the correct -e option or ammending this config file."
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    sys.exit(1)

# esl-reformat
if os.path.exists(paths.eslref) & (os.path.basename(paths.eslref) == "esl-reformat"):
    ESLREF_PATH = paths.eslref
else:
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# autoRfam"
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# Can't find: esl-reformat"
    print "# I'm looking for '%s' as indicated in '%s'" % (paths.eslref, paths.__file__)
    if (os.path.basename(paths.eslref) != "esl-reformat"):
        print "# The basename is '%s', but I expect it to be 'esl-reformat'." % os.path.basename(paths.eslref)
    else:
        print "# Try selecting the correct -e option or ammending this config file."
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    sys.exit(1)

# r-scape
if os.path.exists(paths.rscapepath) & (os.path.basename(paths.rscapepath) == "R-scape"):
    RSCAPEPATH = paths.rscapepath
else:
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# autoRfam"
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# Can't find: R-scape"
    print "# I'm looking for '%s' as indicated in '%s'" % (paths.rscapepath, paths.__file__)
    if (os.path.basename(paths.rscapepath) != "R-scape"):
        print "# The basename is '%s', but I expect it to be 'R-scape'." % os.path.basename(paths.rscapepath)
    else:
        print "# Try selecting the correct -e option or ammending this config file."
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    sys.exit(1)

# RNAcode
if os.path.exists(paths.rnacodepath) & (os.path.basename(paths.rnacodepath) == "RNAcode"):
    RNACODE_PATH = paths.rnacodepath
else:
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# autoRfam"
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    print "# Can't find: RNAcode"
    print "# I'm looking for '%s' as indicated in '%s'" % (paths.rnacodepath, paths.__file__)
    if (os.path.basename(paths.rnacodepath) != "RNAcode"):
        print "# The basename is '%s', but I expect it to be 'RNAcode'." % os.path.basename(paths.rnacodepath)
    else:
        print "# Try selecting the correct -e option or ammending this config file."
    print "# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    sys.exit(1)

DATA_PATH = os.path.dirname(os.path.abspath(templates.__file__))

# .......... setup path variables
# read input
INPUT_URS = args.input_urs
INPUT_ABS = os.path.abspath(INPUT_URS)

# check if output path is valid
if args.outdir == "default_dir":
    NAME = os.path.splitext(os.path.basename(INPUT_ABS))[0]
    DESTDIR = os.path.join(os.path.dirname(INPUT_ABS), "autoRfam_%s" % NAME)
else:
    if os.path.exists(os.path.abspath(args.outdir)):
        if os.path.isfile(os.path.abspath(args.outdir)):
            print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            print "# autoRfam"
            print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            print "# Invalid -o: Please select a valid path."
            print "# Problem:"
            print "# '%s'" % os.path.abspath(args.outdir)
            print "# is not a directory."
            print "#"
            print "# For help: autoRfam.py -h"
            print "- - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            sys.exit(1)

        else:
            print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            print "# autoRfam"
            print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            print "# Invalid -o: Please select a valid path."
            print "# Problem:"
            print "# '%s'" % os.path.abspath(args.outdir)
            print "# already exists."
            print "# It needs to be a new directory."
            print "#"
            print "# For help: autoRfam.py -h"
            print "- - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            sys.exit(1)

    else:
        absdir_path = os.path.abspath(os.path.dirname(args.outdir))
        if os.path.exists(absdir_path):
            DESTDIR = os.path.abspath(args.outdir)
        else:
            print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            print "# autoRfam"
            print "# - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            print "# Invalid -o: Please select a valid path."
            print "# Problem:"
            print "# Can't create '%s', because" % args.outdir
            print "# '%s' doesn't exist." % absdir_path
            print "#"
            print "# For help: autoRfam.py -h"
            print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
            sys.exit(1)

# define global paths
ALIDIR = os.path.join(DESTDIR, "alignments")
DATADIR = os.path.join(DESTDIR, "gen_data")
NAVDIR = os.path.join(DESTDIR, "autoRfamNAV")

# ...........................LUIGI PIPELINE.................................
class GetFasta(luigi.Task):
    """
    """
    _in = INPUT_ABS
    _out = os.path.join(DATADIR, "all_seqs.fasta")

    def output(self):
        return luigi.LocalTarget(self._out)

    def run(self):
        get_fasta.fasta_seq(self._in, self._out)


class NhmmerAll(luigi.Task):
    """
    """
    outdir = os.path.join(DATADIR, "nhmmer_results")
    outname = "nhmmer"

    def output(self):
        return {"tbl": luigi.LocalTarget(os.path.join(self.outdir,
                                                      self.outname + ".tbl")),
                "sto": luigi.LocalTarget(os.path.join(self.outdir,
                                                      self.outname + ".sto"))}

    def requires(self):
        return GetFasta()

    def run(self):
        nhmmer_allvsall.main(NHMMERPATH, self.input().path, self.outdir, self.outname)


class StoSlice(luigi.Task):
    """
    """
    outdir = os.path.join(ALIDIR, "all_alignments")

    def output(self):
        return luigi.LocalTarget(self.outdir)

    def requires(self):
        return NhmmerAll()

    def run(self):
        sto_slicer.slice_sto(self.input()["sto"].path, self.outdir)


class NhmmerTblParse(luigi.Task):
    """
    """
    _out = os.path.join(DATADIR, "clean_hits.tsv")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerAll()

    def run(self):
        nhmmertbl_parse.clean_selfhits(self.input()["tbl"].path, self._out)


class MarkToClean(luigi.Task):
    """
    """
    _out = os.path.join(DATADIR, "seqs_keep.tsv")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerTblParse()

    def run(self):
        marktoclean.main(self.input().path, self._out)

class ClusterAli(luigi.Task):
    """
    """
    _out = os.path.join(DATADIR, "comp.list")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerTblParse()

    def run(self):
        cluster_ali.main(self.input().path, self._out)


class CleanAli(luigi.Task):
    """
    """
    _out = os.path.join(ALIDIR, "clean_alignments/")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return {"stosliced": StoSlice(),
                "toclean": MarkToClean()}

    def run(self):
        clean_ali.main(self.input()["toclean"].path, self.input()["stosliced"].path, self._out)


class PickRepAli(luigi.Task):
    """
    """
    _tsvout = os.path.join(DATADIR, "groups.tsv")
    outdir = os.path.join(ALIDIR, "selected_alignments")
    outdir2 = os.path.join(NAVDIR, "indiv_pages")

    def output(self):
        return luigi.LocalTarget(os.path.join(self.outdir2))

    def requires(self):
        return {"cleanali": CleanAli(),
                "complist": ClusterAli()}

    def run(self):
        pick_repali.main(ESLALISTAT, self.input()["complist"].path, self.input()["cleanali"].path, self._tsvout, self.outdir)
        shutil.copytree(self.outdir, os.path.join(NAVDIR, "indiv_pages"))


class RunRscape(luigi.Task):
    """
    """
    _out = os.path.join(PickRepAli.outdir2, "rscape.log")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return PickRepAli()

    def run(self):
        run_rscape.iterdir(RSCAPEPATH, self.input().path)


class RunRNAcode(luigi.Task):
    """
    """
    _out = os.path.join(PickRepAli.outdir2, "rnacode.log")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return PickRepAli()

    def run(self):
        run_rnacode.iterdir(ESLREF_PATH, RNACODE_PATH, self.input().path)


class AllHtml(luigi.Task):
    """
    """
    _homepath = os.path.join(NAVDIR, "HOME.html")
    _hometsv = os.path.join(DATADIR, "home.tsv")

    def requires(self):
        return {"selali": PickRepAli(),
                "rscape": RunRscape(),
                "rnacode": RunRNAcode()}

    def run(self):
        all_html.main(ESLALISTAT, self.input()["selali"].path, self._homepath, self._hometsv)
        for file in os.listdir(DATA_PATH):
            if not file.startswith('__init__'):
                shutil.copy(os.path.join(DATA_PATH, file), os.path.join(NAVDIR, file))


if __name__ == '__main__':
    if not os.path.exists(DESTDIR):
        os.mkdir(DESTDIR, 0777)
    if not os.path.exists(ALIDIR):
        os.mkdir(ALIDIR, 0777)
    if not os.path.exists(DATADIR):
        os.mkdir(DATADIR, 0777)
    if not os.path.exists(NAVDIR):
        os.mkdir(NAVDIR, 0777)
    luigi.run(["--local-scheduler"], main_task_cls=AllHtml)
