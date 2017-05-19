autoRfam README
===============
Description
-----------
**autoRfam** is a pipeline that allows to cluster RNAcentral sequences into potential new families. It starts with a list of RNAcentral URSs, aligns them, selects the most relevant alignments, recollects important information about them (alignment statistics, annotations, publications, secondary structure prediction, coding potential, etc.) and makes this information browsable through ``html`` pages.

+--------+-------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+
|**IN**  | List of RNAcentral URSs                         |see: URStest1.txt_                                                                                                           |
+--------+-------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+
|**OUT** | Directory with results, browsable through the   | see: `Detailed output directory structure <https://github.com/nataquinones/autoRfam#detailed-output-directory-structure>`_  |
|        | generated file ``/autoRfamNAV/HOME.html``       |                                                                                                                             |
+--------+-------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+

.. _URStest1.txt: https://github.com/nataquinones/autoRfam/blob/master/files/URStest1.txt
.. _URStest2.txt: https://github.com/nataquinones/autoRfam/blob/master/files/URStest2.txt


The **main script** is ``autoRfam.py``, which launches a `Luigi <http://luigi.readthedocs.io/en/stable/index.html>`_ pipeline (see: `autoRfam Luigi pipeline <https://github.com/nataquinones/autoRfam#autorfam-luigi-pipeline>`_). Usage:

.. code::

  autoRfam.py [-h] [-e <s>] [-o <dir>] <ursfile>
  
  positional arguments:
    <ursfile>             File with RNAcentral URSs
  
  optional arguments:
    -h, --help            show this help message and exit
    -e <s>, --env <s>     <s> can be <local>, <docker> or <lsf>. Select to
                          import paths from appropriate file in config/. Default
                          setting is <local>.
    -o <dir>, --outdir <dir>
                          <dir> is the path to the directory which will be
                          created in which the whole pipeline output will be
                          saved. If argument not specified, it will create it in
                          the /path/to/<ursfile>/autoRfam_<ursfile>

Requirements
------------
- ``python 2.7.9``

  - The ``python`` dependencies are specified in `requirements.txt <https://github.com/nataquinones/autoRfam/blob/master/requirements.txt>`_
 
- From ``HMMER-3.1b2`` [`download <http://hmmer.org>`_]

  - ``nhmmer``
  - ``esl-alistat`` and ``esl-reformat`` from the ``Easel`` library
 
- ``R-scape v0.3.3`` [`download <http://eddylab.org/R-scape/>`_]

- ``RNAcode-0.3`` [`download <https://wash.github.io/rnacode/>`_]


Use
---
To run with Docker
^^^^^^^^^^^^^^^^^^
.. code:: bash

  # 1. Clone or download repository
  cd /path/to/autorfam/code
  git clone https://github.com/nataquinones/autoRfam.git
  export AUTORFAM_VOL=/path/to/autorfam/code/autoRfam
  
  # 2. Build image
  cd $AUTORFAM_VOL
  docker-compose build

  # 3. Run service, bin/bash is the entrypoint
  docker-compose run pipeline

  # 4. Once inside, to run autoRfam:
  source $LOC/venv-autorfam/bin/activate
  cd /autorfam/autorfam-code
  python autoRfam.py -e docker [-o <dir>] <ursfile>
  
  
  # Example 1
  python autoRfam.py -e docker ./files/URStest2.txt
  # browse results from: $AUTORFAM_VOL/files/autoRfam_URStest2/autoRfamNAV/HOME.html
  
  # Example 2, using -o option
  python autoRfam.py -e docker -o ./files/example2 ./files/URStest1.txt
  # browse results from: $AUTORFAM_VOL/files/example2/autoRfamNAV/HOME.html
  
  # For help
  python autoRfam.py -h


To run locally
^^^^^^^^^^^^^^
You must have the `requirements <https://github.com/nataquinones/autoRfam#requirements>`_ installed.

.. code:: bash

  # 1. Clone or download repository
  cd /path/to/autorfam/code
  git clone https://github.com/nataquinones/autoRfam.git

  # 2. Modify config/paths_local.py with appropriate paths
  nhmmerpath = "local/path/to/nhmmer"
  eslalistat = "local/path/to/esl-alistat"
  eslref = "local/path/to/esl-reformat"
  rscapepath = "local/path/to/R-scape"
  rnacodepath = "local/path/to/RNAcode"

  # 3. Create a new virtual environment
  virtualenv /path/to/new/autorfam-venv/
  source /path/to/new/autorfam-venv/bin/activate
  cd /path/to/autorfam/code/autoRfam/
  pip install -r requirements.txt

  # 4. Run autoRfam
  # source /path/to/new/autorfam-venv/bin/activate
  cd /path/to/autorfam/code/autoRfam/
  python autoRfam.py -e local [-o <dir>] <ursfile>
  
  
  # Example 1
  python autoRfam.py -e local ./files/URStest2.txt
  # browse results from: /path/to/autorfam/code/files/autoRfam_URStest2/autoRfamNAV/HOME.html
  
  # Example 2, using -o option
  python autoRfam.py -e local -o ./files/example2 ./files/URStest1.txt
  # browse results from: /path/to/autorfam/code/files/example2/autoRfamNAV/HOME.html
  
  # For help
  python autoRfam.py -h


To run in LSF cluster
^^^^^^^^^^^^^^^^^^^^^
.. code:: bash

  # 1. Get an interactive node
  bsub -Is $SHELL

  # 2. Update config/luigi.cfg with appropriate information

  # 3. Start central scheduler
  luigid

  # 4. ssh to the interactive node

  # 5. Run the luigi script with '-e lsf'


Detailed output directory structure 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IN: ``URStest.txt``

OUT:

.. code::

      autoRfam_URStest/
      │
      ├── alignments/
      │   ├── all_alignments/
      │   │   ├── *.sto
      │   │   └── ...
      │   ├── clean_alignments/
      │   │   ├── *.sto
      │   │   ├── *.cl.sto
      │   │   └── ...
      │   └── selected_alignments/
      │       ├── URSxxxxxxxxxx/
      │       │   └── URSxxxxxxxxxx.sto
      │       └── ...
      │           └── ...
      │   
      ├── autoRfamNAV/
      │   ├── help.html
      │   ├── HOME.html
      │   ├── indiv_pages/
      │   │   ├── rnacode.log
      │   │   ├── rscape.log
      │   │   ├── URSxxxxxxxxxx/
      │   │   │   ├── rnacode/
      │   │   │   │   ├── (hss-0.eps)
      │   │   │   │   └── rnacode.out
      │   │   │   ├── rscape/
      │   │   │   │   ├── URSxxxxxxxxxx.R2R.cyk.svg
      │   │   │   │   └── ...
      │   │   │   ├── URSxxxxxxxxxx.aln
      │   │   │   ├── URSxxxxxxxxxx.sto
      │   │   │   ├── URSxxxxxxxxxx.sto.html
      │   │   │   └── URSxxxxxxxxxx.sto.txt
      │   │   └── URS.../
      │   │       └──...
      │   └── sorttable.js
      │
      └── gen_data
          ├── all_seqs.fasta
          ├── clean_hits.tsv
          ├── comp.list
          ├── groups.tsv
          ├── home.tsv
          ├── nhmmer_results/
          │    ├── nhmmer.out
          │    ├── nhmmer.sto
          │    └── nhmmer.tbl
          └── seqs_keep.tsv

autoRfam Luigi pipeline
-----------------------
.. image::  https://github.com/nataquinones/autoRfam/blob/master/docs/pipeline_diagram.png 
