autoRfam README
===============
Description
-----------
TO_DO

Requirements
------------
- ``python 2.7.9``

  - The ``python`` dependencies are specified in `requirements.txt <https://github.com/nataquinones/autoRfam/blob/master/requirements.txt>`_ and can be installed in a virtual environment as previously described.
 
- From ``HMMER-3.1b2``

  - ``nhmmer``
  - ``esl-alistat`` and ``esl-reformat`` from the Easel library
 
- ``R-scape v0.3.3``

- ``RNAcode-0.3``


Use
---

.. code:: bash

  # 1. Clone or download repository
  cd path/to/
  git clone https://github.com/nataquinones/autoRfam.git

  # 2. Modify data/paths.py with corresponding paths
  nhmmerpath = "~/hmmer-3.1b2/binaries/nhmmer"
  eslalistat = "~/hmmer-3.1b2/easel/miniapps/esl-alistat"
  eslref = "~/hmmer-3.1b2/easel/miniapps/esl-reformat"
  rscapepath = "~/rscape_v0.3.3/bin/R-scape"
  rnacodepath = "~/RNAcode-0.3/src/RNAcode"

  # 3. Create a new virtual environment
  virtualenv /path/to/new/autorfam-venv/

  # 4. Activate virtual environment
  source /path/to/new/autorfam-venv/bin/activate

  # 5. Install python dependencies
  cd /path/to/autoRfam/
  pip install -r requirements.txt

  # 6. Run
  python /path/to/autoRfam/autoRfam.py /path/to/URS_list.txt 


Scripts
-------

+---------------------+------+------------------------------------------------------------------------------------+
| get_fasta.py_       | Takes file of RNAcentral URSs, fetches the sequences in ``.fasta`` format and saves file. |
|                     +------+------------------------------------------------------------------------------------+
|                     | in:  | List of non species-specific RNAcentral URSs, one per line [example]               |
|                     +------+------------------------------------------------------------------------------------+
|                     | out: | ``FASTA`` file                                                                     |
+---------------------+------+------------------------------------------------------------------------------------+



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

Pipeline
---------
.. image::  https://github.com/nataquinones/autoRfam/blob/master/docs/pipeline_diagram.png 
