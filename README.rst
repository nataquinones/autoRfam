autoRfam README
===============
Description
-----------
TO_DO

Requirements
------------
- ``python 2.7.9``

  - The ``python`` dependencies are specified in `requirements.txt <https://github.com/nataquinones/autoRfam/blob/master/requirements.txt>`_ and can be installed in a virtual environment as previously described.
 
- From ``HMMER-3.1b2`` [`download <http://hmmer.org>`_]

  - ``nhmmer``
  - ``esl-alistat`` and ``esl-reformat`` from the Easel library
 
- ``R-scape v0.3.3`` [`download <http://eddylab.org/R-scape/>`_]

- ``RNAcode-0.3`` [`download <https://wash.github.io/rnacode/>`_]


Use
---

To run locally
^^^^^^^^^^^^^^
.. code:: bash

  # 1. Clone or download repository
  cd path/to/
  git clone https://github.com/nataquinones/autoRfam.git

  # 2. Modify config/paths_local.py with appropriate paths
  nhmmerpath = "local/path/to/nhmmer"
  eslalistat = "local/path/to/esl-alistat"
  eslref = "local/path/to/esl-reformat"
  rscapepath = "local/path/to/R-scape"
  rnacodepath = "local/path/to/RNAcode"

  # 3. Create a new virtual environment
  virtualenv /path/to/new/autorfam-venv/

  # 4. Activate virtual environment
  source /path/to/new/autorfam-venv/bin/activate

  # 5. Install python dependencies
  cd /path/to/autoRfam/
  pip install -r requirements.txt

  # 6. Run
  python /path/to/autoRfam/autoRfam.py /path/to/URS_list.txt

  # For options check:
  pyhton /path/to/autoRfam/autoRfam.py -h


To run in LSF cluster
^^^^^^^^^^^^^^^^^^^^^
.. code:: bash

  # 1. Get an interactive node
  bsub -Is $SHELL

  # 2. Update config/luigi.cfg with appropriate information

  # 3. Start central scheduler
  luigid

  # 4. ssh to the interactive node

  # 5. Run the luigi script


To run with Docker
^^^^^^^^^^^^^^^^^^
.. code:: bash

  # TO_DO

  # 1. Clone or download repository
  cd /path/to/autorfam/code
  git clone https://github.com/nataquinones/autoRfam.git

  # 2. Run the build
  export AUTORFAM_VOL=/path/to/autorfam/code
  cd $AUTORFAM_VOL
  docker-compose up --build

  # 3. To run interactive session on builded image
  # (where <autorfam_pipeline> is the <image>)
  docker run -it -v ${AUTORFAM_VOL}:/autorfam/autorfam-code <autorfam_pipeline>
  source /autorfam/local/venv-autorfam/bin/activate
  /autorfam/autorfam-code/autoRfam.py -e docker <URS_list.txt>
  # for help
  /autorfam/autorfam-code/autoRfam.py -h



Individual scripts
------------------

+---------------------+------------------------------------------------------------------------------------------------------+
| get_fasta.py_       | Takes file of RNAcentral URSs, fetches the sequences in ``.fasta`` format and saves them into file.  |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``get_fasta.py <in> <out>``                                                                 |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<in>`` Input list of non species-specific RNAcentral URSs, one per line                   |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out>`` Output ``.fasta`` file                                                            |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| nhmmer_allvsall.py_ | Runs ``nhmmer`` with ``.fasta`` file against itself with                                             |
|                     | options: ``-o`` ``-A`` ``--tblout`` ``--noali`` ``--rna`` ``--tformat fasta`` ``--qformat fasta``    |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``nhmmer_allvsall.py <nhmmerpath> <in> <out_path> <out_name>``                              |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<nhmmerpath>``: Path to ``nhmmer`` from ``HMMER-3.1b2``                                   |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<in>``: Input ``.fasta`` file                                                             |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out_path>``: Path where all the output files will be saved                               |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out_name>``: Name of the output files                                                    |
|                     |        |                                                                                             |
|                     |        | - ``out_name.out`` (from ``nhmmer``'s ``-o`` option)                                        |
|                     |        | - ``out_name.sto`` (from ``nhmmer`` ``-A`` option)                                          |
|                     |        | - ``out_name.tbl`` (from ``nhmmer`` ``--tblout`` option)                                    |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| sto_slicer.py_      | Takes a concatenated ``.sto`` file and slices it into all the individual alignments, names them in   |
|                     | based on the first sequence of alignment.                                                            |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``sto_slicer.py <in> <out_dir>``                                                            |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<in>``: Input concatenated ``.sto`` file                                                  |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out_dir>``: Directory where all the sliced ``.sto`` files will be saved                  |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| nhmmertbl_parse.py_ | Takes ``nhmmer --tblout``'s output and processes it into ``.tsv`` file to be used for                |
|                     | ``networkx`` processing. (Removes non significant hits, removes lines of query sequences that        |
|                     | only have self-hits, leaves only columns of query, target, and alignment from-to.)                   |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``nhmmertbl_parse.py <in> <out>``                                                           |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<in>``: Input ``nhmmer --tblout``                                                         |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out>``: Processed ``.tsv file``                                                          |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| martoclean.py_      | Takes the output of nhmmertbl_parse.py_ . If a query has repetead hits of a same target sequence,    |
|                     | it picks and marks with a ``*`` the one of greater length.                                           |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``nhmmertbl_parse.py <in> <out>``                                                           |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<in>``: Processed ``.tsv file`` obtained through nhmmertbl_parse.py_                      |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out>``: Marked ``.tsv file`` (Added column with ``*`` next to the sequence               |
|                     |        | that is to be kept.)                                                                        |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| cluster_ali.py_     | Takes ``.tsv`` file with column "query and "target" (the output of nhmmertbl_parse.py_) to compute   |
|                     | a sparse matrix and get the connected components with networkx. Gives list of lists                  |
|                     | representing groups.                                                                                 |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``cluster_ali.py <in>``                                                                     |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<in>``: Processed ``.tsv file`` obtained through nhmmertbl_parse.py_                      |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | *Output:* In the same directory of the input, it makes a file called ``comp.list`` with     |
|                     |        | a pickle file list of lists                                                                 |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| clean_ali.py_       | Takes marked ``.tsv`` file (the output of martoclean.py_) and the path to a directory with its       |
|                     | corresponding alignments. It deletes the unmarked sequences (with no ``*``) and makes a copy of      |
|                     | the alignments in a new directory called "clean_alignments". A ``.cl`` extension is added to         |
|                     | the alignments that were cleaned.                                                                    |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``clean_ali.py <in_tsv> <in_ali>``                                                          |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<in_tsv>``: The ``.tsv file`` obtained through martoclean.py_                             |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<in_ali>``: Directory with corresponding alingments                                       |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | *Output:* In the same directory of the input, it makes a directory called                   |
|                     |        | ``clean_alignments`` with copies of the processed alignments inside.                        |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| pick_reprali.py_    | Takes directory with .sto alignments and a list of connected components (from cluster_ali.py_ ) that |
|                     | groups them. With this information, it runs esl-alistat on each alignment and selects the best per   |
|                     | group and makes a new directory with the selected alignments.                                        |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``pick_reprali.py <esl-alistat> <comp.list> <in_dir> <out_tsv> <out_dir>``                  |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<esl-alistat>``: Path to ``esl-alistat``, from ``easel`` in ``HMMER-3.1b2``               |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<comp.list>``: List of lists in pickle file, from cluster_ali.py_                         |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<in_dir>``:  Directory of directories to process                                          |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out_tsv>``: Output ``.tsv`` file with alignment stats                                    |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<out_dir>``:  Path where all the selected alignments will be saved                        |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| run_rscape.py_      | For a directory of directories with ``.sto`` alignments, runs ``R-scape`` and puts the output        |
|                     | inside each, in a folder called ``rscape\``.                                                         |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``run_rscape.py <rscape> <in_dir>``                                                         |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<rscape>``: Path to ``R-scape v0.3.3``                                                    |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<in_dir>``: Directory of directories to process                                           |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| run_rnacode.py_     | For a directory of directories with ``.sto`` alignments, converts alignment into clustal format      |  
|                     | runs ``RNAcode`` and puts the output inside each, in a folder called ``rnacode\``                    |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``run_rscape.py <esl-reformat> <rscape> <in_dir>``                                          |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<esl-reformat>``: Path to ``esl-reformat``, from ``easel`` in ``HMMER-3.1b2``             |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<rscape>``: Path to ``RNAcode-0.3``                                                       |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<in_dir>``: Directory of directories to process                                           |
+---------------------+--------+---------------------------------------------------------------------------------------------+
| all_html.py_        | For a directory of directories with ``.sto`` alignments, ``rscape\`` and ``rnacode\`` results        |
|                     | it generates a tree of html files as well as a ``HOME.html`` entry point.                            |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |**Use:**| ``all_html.py <esl-alistat> <in_dir> <home_html> <home_tsv>``                               |
|                     +--------+---------------------------------------------------------------------------------------------+
|                     |        | ``<esl-alistat>``: Path to ``esl-alistat``, from ``easel`` in ``HMMER-3.1b2``               |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<in_dir>``: Directory of directories to process                                           |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<home_html>``: Entry point to html pages, (``html`` home)                                 |
|                     |        +---------------------------------------------------------------------------------------------+
|                     |        | ``<home_tsv>``: ``.tsv`` file generated from individual pages, used to make html home       |
+---------------------+--------+---------------------------------------------------------------------------------------------+

.. _get_fasta.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/get_fasta.py
.. _nhmmer_allvsall.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/nhmmer_allvsall.py
.. _sto_slicer.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/sto_slicer.py
.. _nhmmertbl_parse.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/nhmmertbl_parse.py
.. _martoclean.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/martoclean.py
.. _cluster_ali.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/cluster_ali.py
.. _clean_ali.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/clean_ali.py
.. _pick_reprali.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/pick_reprali.py
.. _run_rscape.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/run_rscape.py
.. _run_rnacode.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/run_rnacode.py
.. _all_html.py: https://github.com/nataquinones/autoRfam/blob/master/scripts/all_html.py

Luigi pipeline
--------------
.. image::  https://github.com/nataquinones/autoRfam/blob/master/docs/pipeline_diagram.png 

Directory structure 
^^^^^^^^^^^^^^^^^^^
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
