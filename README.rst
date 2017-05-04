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

  # 2. Modify `data/paths.py <https://github.com/nataquinones/autoRfam/blob/master/data/paths.py>`_ with corresponding paths

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
TO_DO



Pipeline
---------
.. image::  https://github.com/nataquinones/autoRfam/blob/master/docs/pipeline_diagram.png 
