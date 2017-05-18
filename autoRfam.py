# ........................IMPORT GENERAL MODULES..............................
import argparse
import luigi
import os
import shutil
import sys
# ........................IMPORT PROJECT MODULES..............................
from scripts import setup_check
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

# ......................ARGUMENT PARSER AND SETUP............................


def main_argparser():
    """
    Main argument parser. Defines the variables: input_urs, outdir and env.
    """
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

    return parser.parse_args()


def import_config(args):
    """
    Conditonally import paths, depending on option specified in -e option
    from main_argparser function.
    """
    args = main_argparser()
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

    return paths


# ...........................LUIGI PIPELINE.................................


class SetUp(luigi.Task):
    """
    """
    arguments = main_argparser()
    out_dir = setup_check.check_outdir(arguments)
    paths = setup_check.check_config_paths(import_config(arguments))
    data_dir = os.path.join(out_dir, "gen_data")
    ali_dir = os.path.join(out_dir, "alignments")
    nav_dir = os.path.join(out_dir, "autoRfamNAV")
    nhmmer_dir = os.path.join(data_dir, "nhmmer_results")
    allali_dir = os.path.join(ali_dir, "all_alignments")
    cleanali_dir = os.path.join(ali_dir, "clean_alignments")
    selali_dir = os.path.join(ali_dir, "selected_alignments")
    indpag_dir = os.path.join(nav_dir, "indiv_pages")
    template_dir = os.path.dirname(os.path.abspath(templates.__file__))

    def output(self):
        return luigi.LocalTarget(self.out_dir)

    def run(self):
        os.mkdir(self.out_dir)
        os.mkdir(self.data_dir)
        os.mkdir(self.ali_dir)


class GetFasta(luigi.Task):
    """
    """
    _in = SetUp.arguments.input_urs
    _out = os.path.join(SetUp.data_dir,
                        "all_seqs.fasta")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return SetUp()

    def run(self):
        get_fasta.fasta_seq(self._in, self._out)


class NhmmerAll(luigi.Task):
    """
    """
    outdir = SetUp.nhmmer_dir
    outname = "nhmmer"

    def output(self):
        return {"tbl": luigi.LocalTarget(os.path.join(self.outdir,
                                                      self.outname +
                                                      ".tbl")),
                "sto": luigi.LocalTarget(os.path.join(self.outdir,
                                                      self.outname +
                                                      ".sto"))}

    def requires(self):
        return GetFasta()

    def run(self):
        nhmmer_allvsall.main(SetUp.paths.nhmmerpath,
                             self.input().path,
                             self.outdir,
                             self.outname)


class StoSlice(luigi.Task):
    """
    """
    outdir = SetUp.allali_dir

    def output(self):
        return luigi.LocalTarget(self.outdir)

    def requires(self):
        return NhmmerAll()

    def run(self):
        sto_slicer.slice_sto(self.input()["sto"].path,
                             self.outdir)


class NhmmerTblParse(luigi.Task):
    """
    """
    _out = os.path.join(SetUp.data_dir,
                        "clean_hits.tsv")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerAll()

    def run(self):
        nhmmertbl_parse.clean_selfhits(self.input()["tbl"].path,
                                       self._out)


class MarkToClean(luigi.Task):
    """
    """
    _out = os.path.join(SetUp.data_dir,
                        "seqs_keep.tsv")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerTblParse()

    def run(self):
        marktoclean.main(self.input().path,
                         self._out)


class ClusterAli(luigi.Task):
    """
    """
    _out = os.path.join(SetUp.data_dir,
                        "comp.list")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerTblParse()

    def run(self):
        cluster_ali.main(self.input().path,
                         self._out)


class CleanAli(luigi.Task):
    """
    """
    _out = SetUp.cleanali_dir

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return {"stosliced": StoSlice(),
                "toclean": MarkToClean()}

    def run(self):
        clean_ali.main(self.input()["toclean"].path,
                       self.input()["stosliced"].path,
                       self._out)


class PickRepAli(luigi.Task):
    """
    """
    _tsvout = os.path.join(SetUp.data_dir, "groups.tsv")
    outdir = SetUp.selali_dir
    outdir2 = SetUp.indpag_dir

    def output(self):
        return luigi.LocalTarget(os.path.join(self.outdir2))

    def requires(self):
        return {"cleanali": CleanAli(),
                "complist": ClusterAli()}

    def run(self):
        pick_repali.main(SetUp.paths.eslalistat,
                         self.input()["complist"].path,
                         self.input()["cleanali"].path,
                         self._tsvout,
                         self.outdir)
        shutil.copytree(self.outdir,
                        SetUp.indpag_dir)


class RunRscape(luigi.Task):
    """
    """
    _out = os.path.join(PickRepAli.outdir2,
                        "rscape.log")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return PickRepAli()

    def run(self):
        run_rscape.iterdir(SetUp.paths.rscapepath,
                           self.input().path)


class RunRNAcode(luigi.Task):
    """
    """
    _out = os.path.join(PickRepAli.outdir2,
                        "rnacode.log")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return PickRepAli()

    def run(self):
        run_rnacode.iterdir(SetUp.paths.eslref,
                            SetUp.paths.rnacodepath,
                            self.input().path)


class AllHtml(luigi.Task):
    """
    """
    _homepath = os.path.join(SetUp.nav_dir,
                             "HOME.html")
    _hometsv = os.path.join(SetUp.data_dir,
                            "home.tsv")

    def requires(self):
        return {"selali": PickRepAli(),
                "rscape": RunRscape(),
                "rnacode": RunRNAcode()}

    def run(self):
        all_html.main(SetUp.paths.eslalistat,
                      self.input()["selali"].path,
                      self._homepath,
                      self._hometsv)
        for filex in os.listdir(SetUp.template_dir):
            if not filex.startswith('__init__'):
                shutil.copy(os.path.join(SetUp.template_dir, filex),
                            os.path.join(SetUp.nav_dir, filex))

# ..........................................................................

if __name__ == '__main__':
    luigi.run(["--local-scheduler"], main_task_cls=AllHtml)
