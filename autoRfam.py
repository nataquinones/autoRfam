import luigi
import os
import shutil
import sys
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

NHMMERPATH = "/Users/nquinones/Documents/hmmer-3.1b2/binaries/nhmmer"
ESLALISTAT = "/Users/nquinones/Documents/hmmer-3.1b2/easel/miniapps/esl-alistat"
ESLREF_PATH = "/Users/nquinones/Documents/hmmer-3.1b2/easel/miniapps/esl-reformat"
RSCAPEPATH = "/Users/nquinones/Documents/rscape_v0.3.3/bin/R-scape"
RNACODE_PATH = "/Users/nquinones/Documents/RNAcode-0.3/src/RNAcode"
DATA_PATH = "/Users/nquinones/Dropbox/EMBL-EBI/autoRfam/data"

INPUT_URS = sys.argv[1]
INPUT_ABS = os.path.abspath(INPUT_URS)
NAME = os.path.splitext(os.path.basename(INPUT_ABS))[0]
DESTDIR = os.path.join(os.path.dirname(INPUT_ABS), "autoRfam_%s" % NAME)
ALIDIR = os.path.join(DESTDIR, "alignments")
DATADIR = os.path.join(DESTDIR, "gen_data")
NAVDIR = os.path.join(DESTDIR, "autoRfamNAV")


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
        os.symlink(self._homepath, os.path.join(DESTDIR, "HOME.html"))
        for file in os.listdir(DATA_PATH):
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
