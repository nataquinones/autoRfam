PIPELINE
========

STEP 1: GET FASTA
-----------------
1.1 from txt to python list ()
1.2 from urs list to FASTA ()

SCRIPT: get_fasta.py
IN: .txt URS list
OUT: .fasta sequences file


STEP 2: NHMMER
--------------
2.1 Run nhmmer, get output files ()
2.2 Parse nhmmer .tbl ()
2.3 Clean .tbl ()
2.4 Slice concat sto file ()

SCRIPT: nhmmerall.py
IN: .fasta file
OUT: all nhmmer files, parsed nhmmer tbl, sliced sto files


STEP 3: CLUSTER
---------------
3.1 Read .tsv table
3.2 Make dictonary mapping urs to integer
3.3 Make scipy_sparse_matrix
3.4 Find components
* 3.5 Find cliques

SCRIPT: clusteR_ali.py
IN: parsed nhmmer tbl
OUT: pickle list with components

STEP 4: CLEAN ALIGNMENTS
------------------------
4.1 Read table
4.2 Modify table with names
4.3 Mark best

SCRIPT: marktoclean.py
IN: tbl ???TODO
OUT: marked .tsv tbl

4.4 Read marked .tsv tbl
4.5 Clean alignments

SCRIPT: clean_ali.py
IN: marked .tsv tbl
OUT: cleaned alignments

STEP 5: PICK BEST ALIGNMENTS
----------------------------
5.1 read pickle list
5.2 make easel stats for each
5.3 make summary with group info
5.4 select the best
5.5 join and save

SCRIPT: pick_repali.py
IN: pickle list with components
OUT: list of selected alignments

STEP 6: FETCH SELECTED ALIGNMENTS
---------------------------------

SCRIPT: None
IN: list of selected alignments
OUT: folder with selected alignments

STEP 7: RUN RNAcode and Rscape
------------------------------

STEP 8: Make HTML
-----------------


