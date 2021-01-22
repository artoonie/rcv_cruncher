import decimal
import os
from statistics import median
import pandas as pd
import numpy as np
from itertools import combinations
from copy import deepcopy

# cruncher imports
from .definitions import NAN, SKIPPEDRANK, OVERVOTE, WRITEIN, index_inf, replace, remove, remove_dup
from .cache_helpers import save
from .rcv_base import RCV
from .ballots import ballots, cleaned_ballots, candidates


def convert_cvr(ctx):
    """
    convert ballots read in with parser into common csv format.
    One ballot per row, columns: ID, extra_info, rank1, rank2 ...
    """
    ballot_dict = deepcopy(ballots(ctx, combine_writeins=False))
    bs = ballot_dict['ranks']
    weight = ballot_dict['weight']
    del ballot_dict['ranks']
    del ballot_dict['weight']

    # how many ranks?
    num_ranks = max(len(i) for i in bs)

    # replace constants with strings
    bs = [replace(SKIPPEDRANK, 'skipped', b) for b in bs]
    bs = [replace(OVERVOTE, 'overvote', b) for b in bs]

    # make sure all ballots are lists of equal length, adding trailing 'skipped' if necessary
    bs = [b + (['skipped'] * (num_ranks - len(b))) for b in bs]

    # assemble output_table, start with extras
    output_df = pd.DataFrame.from_dict(ballot_dict)

    # are weights all one, then dont add to output
    if not all([i == 1 for i in weight]):
        output_df['weight'] = [float(w) for w in weight]

    # add in rank columns
    for i in range(1, num_ranks + 1):
        output_df['rank' + str(i)] = [b[i-1] for b in bs]

    return output_df

##########################
# MISC TABULATION

def cumulative_ranking_tables(ctx):
    """
    Return cumulative ranking tables. Rows are candidate names and columns are rank numbers.
    Reading across columns, the tables show the accumulating count/percentage of ballots that marked
    a candidate as more ranks are considered. The final column shows the count/percentage of ballots
    that never marked the candidate.
    """

    # get inputs
    candidate_set = sorted(candidates(ctx))

    # ballot rank limit
    ballot_length = len(ballots(ctx)['ranks'][0])

    # get cleaned ballots
    cleaned_dict = deepcopy(cleaned_ballots(ctx))
    ballot_set = [{'ranks': ranks + (['NA'] * (ballot_length - len(ranks))), 'weight': weight}
                  for ranks, weight in zip(cleaned_dict['ranks'], cleaned_dict['weight'])]

    # total ballots
    total_ballots = sum([d['weight'] for d in ballot_set])

    # create data frame that will be populated and output
    col_names = ["Rank " + str(i + 1) for i in range(ballot_length)] + ['Did Not Rank']
    cumulative_percent_df = pd.DataFrame(NAN, index=candidate_set, columns=col_names)
    cumulative_count_df = pd.DataFrame(NAN, index=candidate_set, columns=col_names)

    # tally candidate counts by rank
    rank_counts = []
    for rank in range(0, ballot_length):
        rank_cand_set = set([b['ranks'][rank] for b in ballot_set]) - {'NA'}
        current_rank_count = {cand: 0 for cand in rank_cand_set}
        for cand in rank_cand_set:
            current_rank_count[cand] = sum(b['weight'] for b in ballot_set if cand == b['ranks'][rank])
        rank_counts.append(current_rank_count)

    # accumulate ballot counts that rank candidates
    cumulative_counter = {cand: 0 for cand in candidate_set}
    for rank in range(0, ballot_length):
        for cand in candidate_set:
            # if candidate has any marks for this rank, accumulate them
            if cand in rank_counts[rank]:
                cumulative_counter[cand] += rank_counts[rank][cand]
            # update tables
            cumulative_count_df.loc[cand, 'Rank ' + str(rank + 1)] = cumulative_counter[cand]
            cumulative_percent_df.loc[cand, 'Rank ' + str(rank + 1)] = cumulative_counter[cand] * 100 / total_ballots

    # fill in Did Not Rank column
    for cand in candidate_set:
        cumulative_count_df.loc[cand, 'Did Not Rank'] = total_ballots - cumulative_counter[cand]
        cumulative_percent_df.loc[cand, 'Did Not Rank'] = (total_ballots - cumulative_counter[cand]) * 100 / total_ballots

    cumulative_count_df = cumulative_count_df.astype(float).round(3)
    cumulative_percent_df = cumulative_percent_df.astype(float).round(3)

    return cumulative_count_df, cumulative_percent_df

def condorcet_tables(ctx):
    """
    Returns a two condorcet tables as a pandas data frame with candidate names as row and column indices.
    One contains counts and the other contains percents.

    Each cell indicates the count/percentage of ballots that ranked the row-candidate over
    the column-candidate (including ballots that only ranked the row-candidate). When calculating percents,
    the denominator is each cell is the number of ballots that ranked the row-candidate OR the column-candidate.

    Symmetric cells about the diagonal should sum to 100 (for the percent table).
    """
    candidate_set = sorted(candidates(ctx))
    cleaned_dict = deepcopy(cleaned_ballots(ctx))
    ballot_set = [{'ranks': ranks, 'weight': weight}
                  for ranks, weight in zip(cleaned_dict['ranks'], cleaned_dict['weight'])]

    # create data frame that will be populated and output
    condorcet_percent_df = pd.DataFrame(NAN, index=candidate_set, columns=candidate_set)
    condorcet_count_df = pd.DataFrame(NAN, index=candidate_set, columns=candidate_set)

    # turn ballot-lists into ballot-dict with
    # key 'id' containing a unique integer id for the ballot
    # key 'ranks' containing the original ballot-list
    ballot_dicts = [{'id': ind, 'ballot': ballot} for ind, ballot in enumerate(ballot_set)]

    # make dictionary with candidate as key, and value as list of ballot-dicts
    # that contain their name in any rank
    cand_ballot_dict = {cand: [ballot for ballot in ballot_dicts if cand in ballot['ballot']['ranks']]
                        for cand in candidate_set}

    # all candidate pairs
    cand_pairs = combinations(candidate_set, 2)

    for pair in cand_pairs:
        cand1 = pair[0]
        cand2 = pair[1]

        # get the union of their ballots
        combined_ballot_list = cand_ballot_dict[cand1] + cand_ballot_dict[cand2]
        uniq_pair_ballots = list({v['id']: v['ballot'] for v in combined_ballot_list}.values())

        uniq_pair_ballots_weights = [ballot['weight'] for ballot in uniq_pair_ballots]
        sum_weighted_ballots = sum(uniq_pair_ballots_weights)

        # which ballots rank cand1 above cand2?
        cand1_vs_cand2 = [index_inf(b['ranks'], cand1) < index_inf(b['ranks'], cand2) for b in uniq_pair_ballots]
        cand1_vs_cand2_weightsum = sum(weight * flag for weight, flag
                                       in zip(uniq_pair_ballots_weights, cand1_vs_cand2))

        # the remainder then must rank cand2 over cand1
        cand2_vs_cand1 = [not i for i in cand1_vs_cand2]
        cand2_vs_cand1_weightsum = sum(weight * flag for weight, flag
                                       in zip(uniq_pair_ballots_weights, cand2_vs_cand1))

        # add counts to df
        condorcet_count_df.loc[cand1, cand2] = cand1_vs_cand2_weightsum
        condorcet_count_df.loc[cand2, cand1] = cand2_vs_cand1_weightsum

        # calculate percent
        if sum_weighted_ballots:
            cand1_percent = (cand1_vs_cand2_weightsum / sum_weighted_ballots) * 100
            cand2_percent = (cand2_vs_cand1_weightsum / sum_weighted_ballots) * 100
        else:
            cand1_percent = 0
            cand2_percent = 0

        # add to df
        condorcet_percent_df.loc[cand1, cand2] = cand1_percent
        condorcet_percent_df.loc[cand2, cand1] = cand2_percent

    # find condorcet winner and set index name to include winner
    condorcet_winner = None

    if len(candidate_set) == 1:

        condorcet_winner = candidate_set[0]
    else:

        for cand in candidate_set:

            not_cand = set(candidate_set) - {cand}
            all_winner = all(condorcet_percent_df.loc[cand, not_cand] > 50)

            if all_winner:
                if condorcet_winner is None:
                    condorcet_winner = cand
                else:
                    print("cannottt be more than one condorcet winner!!!!")
                    exit(1)

    # convert decimal to float
    condorcet_count_df = condorcet_count_df.astype(float).round(3)
    condorcet_percent_df = condorcet_percent_df.astype(float).round(3)

    return condorcet_count_df, condorcet_percent_df, condorcet_winner


def first_second_tables(ctx):
    """
    Return two pandas tables with candidates as columns and first row showing distribution of first round votes.
    Subsequent rows indicate second choice vote distribution for each column.

    first table is vote counts
    second table is percentages
    """

    candidate_set = sorted(candidates(ctx))
    cleaned_dict = deepcopy(cleaned_ballots(ctx))
    ballot_set = [{'ranks': ranks, 'weight': weight}
                  for ranks, weight in zip(cleaned_dict['ranks'], cleaned_dict['weight'])]

    # create data frame that will be populated and output
    percent_no_exhaust_df = pd.DataFrame(NAN, index=['first_choice', *candidate_set], columns=candidate_set)
    percent_df = pd.DataFrame(NAN, index=['first_choice', *candidate_set, 'exhaust'], columns=candidate_set)
    count_df = pd.DataFrame(NAN, index=['first_choice', *candidate_set, 'exhaust'], columns=candidate_set)

    # group ballots by first choice
    first_choices = {cand: [] for cand in candidate_set}
    for b in ballot_set:
        if len(b['ranks']) >= 1:
            first_choices[b['ranks'][0]].append(b)

    # sum total first round votes
    total_first_round_votes = 0
    for cand in first_choices:
        total_first_round_votes += sum([b['weight'] for b in first_choices[cand]])

    # add first choices to tables
    # and calculate second choices
    for cand in candidate_set:

        ############################################################
        # update first round table values
        first_choice_count = sum([b['weight'] for b in first_choices[cand]])
        first_choice_percent = (first_choice_count / total_first_round_votes) * 100

        count_df.loc['first_choice', cand] = first_choice_count
        percent_df.loc['first_choice', cand] = first_choice_percent
        percent_no_exhaust_df.loc['first_choice', cand] = first_choice_percent

        ############################################################
        # calculate second choices, group second choices by candidate
        possible_second_choices = list(set(candidate_set) - {cand})
        second_choices = {backup_cand: [] for backup_cand in possible_second_choices + ['exhaust']}

        # group ballots by second choices
        for b in first_choices[cand]:
            if len(b['ranks']) >= 2:
                second_choices[b['ranks'][1]].append(b['weight'])
            else:
                second_choices['exhaust'].append(b['weight'])

        # sum total second round votes
        total_second_choices = 0
        total_second_choices_no_exhaust = 0
        for backup_cand in second_choices:
            total_second_choices += sum(second_choices[backup_cand])
            if backup_cand != 'exhaust':
                total_second_choices_no_exhaust += sum(second_choices[backup_cand])

        # count second choices and add to table
        for backup_cand in second_choices:

            # fill in second choice values in table
            second_choice_count = sum(second_choices[backup_cand])

            # if there are not backup votes fill with zeros
            if total_second_choices == 0:
                second_choice_percent = 0
            else:
                second_choice_percent = (second_choice_count / total_second_choices) * 100

            if total_second_choices_no_exhaust == 0:
                second_choice_percent_no_exhaust = 0
            else:
                second_choice_percent_no_exhaust = (second_choice_count / total_second_choices_no_exhaust) * 100

            count_df.loc[backup_cand, cand] = second_choice_count
            percent_df.loc[backup_cand, cand] = second_choice_percent
            if backup_cand != 'exhaust':
                percent_no_exhaust_df.loc[backup_cand, cand] = second_choice_percent_no_exhaust

    count_df = count_df.astype(float).round(3)
    percent_df = percent_df.astype(float).round(3)
    percent_no_exhaust_df = percent_no_exhaust_df.astype(float).round(3)

    return count_df, percent_df, percent_no_exhaust_df

def rank_usage_tables(ctx):
    """
    DOES NOT USE BALLOT WEIGHTS
    """
    candidate_set = sorted(candidates(ctx, exclude_writeins=False))

    # remove skipped ranks
    ballot_set = [remove(SKIPPEDRANK, b) for b in ballots(ctx)['ranks']]

    # remove empty ballots and those that start with overvote
    ballot_set = [b for b in ballot_set if len(b) >= 1 and b[0] != OVERVOTE]
    # remove other overvotes
    ballot_set = [remove(OVERVOTE, b) for b in ballot_set]
    # remove duplicate rankings
    ballot_set = [remove_dup(b) for b in ballot_set]

    all_ballots_label = "Any candidate"
    n_ballots_label = "Number of Ballots (excluding undervotes and ballots with first round overvote)"
    mean_label = "Mean Valid Rankings Used (excluding duplicates)"
    median_label = "Median Valid Rankings Used (excluding duplicates)"

    rows = [all_ballots_label] + candidate_set
    cols = [n_ballots_label, mean_label, median_label]
    df = pd.DataFrame(index=rows, columns=cols)
    df.index.name = "Ballots with first choice:"

    n_ballots = len(ballot_set)
    mean_rankings = sum(len(b) for b in ballot_set)/n_ballots
    median_rankings = median(len(b) for b in ballot_set)

    df.loc[all_ballots_label, n_ballots_label] = n_ballots
    df.loc[all_ballots_label, mean_label] = mean_rankings
    df.loc[all_ballots_label, median_label] = median_rankings

    # group ballots by first choice
    first_choices = {cand: [] for cand in candidate_set}
    for b in ballot_set:
        first_choices[b[0]].append(b)

    for cand in candidate_set:
        df.loc[cand, n_ballots_label] = len(first_choices[cand])
        if first_choices[cand]:
            df.loc[cand, mean_label] = sum(len(b) for b in first_choices[cand])/len(first_choices[cand])
            df.loc[cand, median_label] = median(len(b) for b in first_choices[cand])
        else:
            df.loc[cand, mean_label] = 0
            df.loc[cand, median_label] = 0

    return df

def crossover_table(ctx):

    candidate_set = sorted(candidates(ctx, exclude_writeins=False))

    ballot_dict = ballots(ctx)
    ballot_weights = deepcopy(ballot_dict['weight'])
    ranks = [remove(SKIPPEDRANK, b) for b in ballot_dict['ranks']]
    ballot_set = [{'ranks': ranks, 'weight': weight}
                  for ranks, weight in zip(ranks, ballot_weights)]

    index_label = "Ballots with first choice:"
    n_ballots_label = "Number of Ballots"

    colname_dict = {cand: cand + " ranked in top 3" for cand in candidate_set}

    rows = candidate_set
    cols = [n_ballots_label] + list(colname_dict.values())
    count_df = pd.DataFrame(index=rows, columns=cols)
    count_df.index.name = index_label
    percent_df = pd.DataFrame(index=rows, columns=cols)
    percent_df.index.name = index_label

    # group ballots by first choice
    first_choices = {cand: [] for cand in candidate_set}
    for b in ballot_set:
        if len(b['ranks']) >= 1 and b['ranks'][0] != OVERVOTE:
            first_choices[b['ranks'][0]].append(b)

    for cand in candidate_set:

        n_first_choice = sum(b['weight'] for b in first_choices[cand])
        count_df.loc[cand, n_ballots_label] = n_first_choice
        percent_df.loc[cand, n_ballots_label] = n_first_choice

        for opponent in candidate_set:

            if n_first_choice:
                crossover_ballots = [True if opponent in b['ranks'][0:min(3, len(b['ranks']))] else False
                                     for b in first_choices[cand]]
                crossover_val = sum(b['weight'] for b, flag in zip(first_choices[cand], crossover_ballots) if flag)
                count_df.loc[cand, colname_dict[opponent]] = crossover_val
                percent_df.loc[cand, colname_dict[opponent]] = crossover_val*100/n_first_choice
            else:
                count_df.loc[cand, colname_dict[opponent]] = 0
                percent_df.loc[cand, colname_dict[opponent]] = 0

    # convert decimal to float
    count_df = count_df.astype(float).round(3)
    percent_df = percent_df.astype(float).round(3)

    return count_df, percent_df


def first_choice_to_finalist_table(rcv_obj):

    dfs = []
    for iTab in range(1, rcv_obj.n_tabulations()+1):

        # who had any ballot weight allotted
        finalist_candidates = list(rcv_obj.finalist_candidates(tabulation_num=iTab)) + ['exhaust']
        candidate_set = sorted(candidates(rcv_obj.ctx))

        ballot_set = [{'ranks': ranks, 'weight': weight, 'weight_distrib': distrib}
                      for ranks, weight, distrib
                      in zip(rcv_obj.get_initial_ranks(tabulation_num=iTab),
                             rcv_obj.get_initial_weights(tabulation_num=iTab),
                             rcv_obj.get_final_weight_distrib(tabulation_num=iTab))]

        index_label = "Ballots with first choice:"
        n_ballots_label = "Number of Ballots"

        colname_dict = {cand: "% of votes to " + cand for cand in finalist_candidates}

        rows = candidate_set
        cols = [n_ballots_label] + list(colname_dict.values())
        df = pd.DataFrame(index=rows, columns=cols + ['percent_sum'])
        df.index.name = index_label

        # group ballots by first choice
        first_choices = {cand: [] for cand in candidate_set}
        for b in ballot_set:
            if len(b['ranks']) >= 1 and b['ranks'][0] in first_choices:
                first_choices[b['ranks'][0]].append(b)

        for cand in candidate_set:

            total_first_choice_ballots = sum(b['weight'] for b in first_choices[cand])
            df.loc[cand, n_ballots_label] = total_first_choice_ballots

            if total_first_choice_ballots:

                redistrib = {opponent: 0 for opponent in finalist_candidates}
                for b in first_choices[cand]:
                    for el in b['weight_distrib']:
                        if el[0] == 'empty':
                            redistrib['exhaust'] += el[1]
                        else:
                            redistrib[el[0]] += el[1]

                redistrib_total_check = 0
                for opponent in redistrib:
                    redistrib_percent = redistrib[opponent] / total_first_choice_ballots * 100
                    df.loc[cand, colname_dict[opponent]] = redistrib_percent
                    redistrib_total_check += redistrib_percent
                df.loc[cand, 'percent_sum'] = redistrib_total_check

            else:
                for opponent in finalist_candidates:
                    df.loc[cand, colname_dict[opponent]] = 0
                df.loc[cand, 'percent_sum'] = 0

        df = df.astype(float).round(3)

        dfs.append(df)

    return dfs

# def prepare_json(ctx):
# prepare json file for RCVIS
#
#     # get rcv results
#     rounds_full = round_by_round_full(ctx)
#     transfers = round_by_round_transfers(ctx)
#     outcomes = candidate_outcomes(ctx)
#
#     if len(rounds_full) != len(transfers):
#         print('something fishy, debug')
#         exit(1)
#     else:
#         num_rounds = len(rounds_full)
#
#     json_dict = {'config': {'contest': contest_name(ctx),
#                             'date': "",
#                             'jurisdiction': place(ctx),
#                             'office': office(ctx),
#                             'threshold': '0'},
#                  'results': []}
#
#     for i in range(num_rounds):
#
#         round_num = i + 1
#         tally_dict = {cand: str(int(tally)) for cand, tally in zip(*rounds_full[i]) if tally > 0}
#         transfer_list = []
#
#         # transfer any zero-vote candidates who were marked as round zero eliminations
#         if round_num == 1:
#             zero_vote_cands = [d['name'] for d in outcomes if d['round_eliminated'] == 0]
#             for cand in zero_vote_cands:
#                 transfer_list.append({'eliminated': cand, 'transfers:': {}})
#
#         # who had an outcomes this round
#         elected = [d for d in outcomes if d['round_elected'] == round_num]
#         eliminated = [d for d in outcomes if d['round_eliminated'] == round_num]
#
#         if len(eliminated) > 1:
#             # transfers are not saved by source and only as net transfer per round
#             print('json converter cannot properly handle multiple candidates eliminated in a single round')
#             raise RuntimeError
#
#         for d in elected:
#             transfer_list.append({'elected': d['name'], 'transfers': {}})
#
#         for d in eliminated:
#             # remove negative transfer
#             round_transfer = {key: str(int(val)) for key, val in transfers[i].items() if val > 0}
#             round_transfer['exhausted'] = round_transfer['exhaust']
#             del round_transfer['exhaust']
#             transfer_list.append({'eliminated': d['name'], 'transfers': round_transfer})
#
#         json_dict['results'].append(
#             {'round': round_num,
#              'tally': tally_dict,
#              'tallyResults': transfer_list})
#
#     outfile = open(ctx['json_dir'] + '/' + ctx['dop'] + '.json', 'w')
#     json.dump(json_dict, outfile)
#     outfile.close()