Analyzing CVRs in a batch
=========================

In the case where you have a set of elections, you can analyze them as a batch. Doing so requires organizing your contest information into a couple of files:

* ``contest_set.csv``: A **csv file** listing the elections, their parsers, tabulation methods, rules, and CVR file path locations.
* ``run_config.json``: A **json file** listing which output statistics and tables to produce.

Both files are explained further below. With both files in the same directory, the batch of elections can be analyzed with ``rcv-cruncher <directory>``. Examples of both files can be downloaded `here <https://github.com/fairvotereform/rcv_cruncher/tree/master/src/rcv_cruncher/example/contest_sets/example>`_.

Contest Set File
^^^^^^^^^^^^^^^^^^

The contest set csv file can contain the following columns:

.. include:: _options_contest_set.rst

Example: candidate + rank column CVRs (Clear Ballot)
----------------------------------------------------

Clear Ballot systems (used by Portland, OR and Fort Collins, CO) export one column per candidate per rank, e.x. ``Smith Rank 1``, ``Smith Rank 2``, ``Doe Rank 1``. These files are read with the ``candidate_rank_column_csv`` parser, which turns two marked candidates at the same rank into an overvote. The Portland export contains every ballot in the city, so the ballot style holding the contest is selected with ``filter_column`` and ``filter_values``. Portland's three write-in lines are separate candidates in the file and are combined by the ``combine_writein_marks`` rule; the ``ignore_candidates`` argument reproduces the city's official rank CVR, which records lone marks on those lines as skipped.

.. code-block:: text

   parser_func: candidate_rank_column_csv
   cvr_path: Oregon/Portland/2024/PortlandOR_CD1_2024_CandidateRankColumn.csv
   extra_parser_args: filter_column=BallotStyleID;filter_values=2;ignore_candidates=Write-in-120,Write-in-121,Write-in-122

See :func:`parsers.candidate_rank_column_csv` for the recognized header formats and the ``contest`` argument used when a file holds several contests.


Run Config
^^^^^^^^^^

The run config file can include the following fields:

.. include:: _options_run_config.rst
