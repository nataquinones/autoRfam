import luigi
import os
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

INPUT = sys.argv[1]
DESTDIR = os.path.join(os.path.dirname(INPUT), "autoRfam")
ALIDIR = os.path.join(DESTDIR, "alignments")


class GetFasta(luigi.Task):
    """
    """
    _in = INPUT
    _out = os.path.join(DESTDIR, "all_seqs.fasta")

    def output(self):
        return luigi.LocalTarget(self._out)

    def run(self):
        get_fasta.fasta_seq(self._in, self._out)


class NhmmerAll(luigi.Task):
    """
    """
    outdir = os.path.join(DESTDIR, "nhmmer_results")

    def output(self):
        return {"tbl": luigi.LocalTarget(os.path.join(self.outdir,
                                                      "nhmmer.tbl")),
                "sto": luigi.LocalTarget(os.path.join(self.outdir,
                                                      "nhmmer.sto"))}

    def requires(self):
        return GetFasta()

    def run(self):
        nhmmer_allvsall.main(NHMMERPATH, self.input().path, self.outdir)


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
    _out = os.path.join(DESTDIR, "clean_hits.tsv")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerAll()

    def run(self):
        nhmmertbl_parse.clean_selfhits(self.input()["tbl"].path, self._out)


class MarkToClean(luigi.Task):
    """
    """
    _out = os.path.join(DESTDIR, "seqs_keep.tsv")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return NhmmerTblParse()

    def run(self):
        marktoclean.main(self.input().path, self._out)


class ClusterAli(luigi.Task):
    """
    """
    _out = os.path.join(DESTDIR, "comp.list")

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
    _tsvout = os.path.join(DESTDIR, "groups.tsv")
    outdir = os.path.join(ALIDIR, "selected_alignments")

    def output(self):
        return luigi.LocalTarget(self.outdir)

    def requires(self):
        return {"cleanali": CleanAli(),
                "complist": ClusterAli()}

    def run(self):
        pick_repali.main(ESLALISTAT, self.input()["complist"].path, self.input()["cleanali"].path, self._tsvout, self.outdir)


class RunRscape(luigi.Task):
    """
    """
    _out = os.path.join(PickRepAli.outdir, "rscape.log")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return PickRepAli()

    def run(self):
        run_rscape.iterdir(RSCAPEPATH, self.input().path)


class RunRNAcode(luigi.Task):
    """
    """
    _out = os.path.join(PickRepAli.outdir, "rnacode.log")

    def output(self):
        return luigi.LocalTarget(self._out)

    def requires(self):
        return PickRepAli()

    def run(self):
        run_rnacode.iterdir(ESLREF_PATH, RNACODE_PATH, self.input().path)


class AllHtml(luigi.Task):
    """
    """
    _homepath = os.path.join(DESTDIR, "HOME.html")
    _hometsv = os.path.join(DESTDIR, "home.tsv")

    def requires(self):
        return {"selali": PickRepAli(),
                "rscape": RunRscape(),
                "rnacode": RunRNAcode()}

    def run(self):
        all_html.main(ESLALISTAT, self.input()["selali"].path, self._homepath, self._hometsv)

if __name__ == '__main__':
    if not os.path.exists(DESTDIR):
        os.mkdir(DESTDIR, 0777)
    if not os.path.exists(ALIDIR):
        os.mkdir(ALIDIR, 0777)
    luigi.run(["--local-scheduler"], main_task_cls=AllHtml)
