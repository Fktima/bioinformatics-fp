#!/usr/bin/python

import csv
import glob
import gzip
import os
import re
import sys

from collections import Counter

import sklearn
from sklearn.metrics import f1_score, recall_score, precision_score
from sklearn.preprocessing import MultiLabelBinarizer

from igg_utils import get_clade_abundances_by_species_id_for_igg_tsv
from metaphlan_utils import get_clade_abundances_by_species_id_for_metaphlan_tsv

# Random Reads Fasta file format
# @SYN_0_3_27_0_-_62078496_1_._HWUSI-EAS577_102317828:1:101:6557:16029/1 1:
# AATTGCATATATGTCCAGCACAGTA
# +
# <A6J:=EG?D?=25C=++F5G:+/J


def main(argv):
    print(f'Getting ground truth for metaphlan')

    actual_abundance_by_ncbi = get_clade_abundances_by_species_id_for_metaphlan_tsv(os.getcwd() + "/combined_metaphlan_profile.tsv")
    actual_abundance_by_igg_id = get_clade_abundances_by_species_id_for_igg_tsv(os.getcwd() + "/combined_igg_profile_lenient/species_profile.tsv")

    random_reads_gz_files = glob.glob(os.getcwd() + '/reads_*.fq.gz')

    result_rows = []
    for random_reads_gz_file in random_reads_gz_files:
        file_name = os.path.basename(random_reads_gz_file)
        reads_name = file_name.split('.')[0]

        print(f'Calculating precision, recall, and f1 score for metaphlan for {reads_name}')

        metaphlan_file = os.getcwd() + "/" + f"{reads_name}.fq.gz_metaphlan_profile.tsv"
        metaphlan_precision_score, metaphlan_recall_score, metaphlan_f1_score \
            = calculate_precision_recall_f1_score_for_metaphlan(actual_abundance_by_ncbi, metaphlan_file)
        result_rows.append(
            ['metaphlan', reads_name, metaphlan_precision_score, metaphlan_recall_score, metaphlan_f1_score])

        print(f'Calculating precision, recall, and f1 score for igg for {reads_name}')

        igg_file = os.getcwd() + "/" + f"{reads_name}.fq.gz_igg_profile_lenient/species_profile.tsv"
        igg_precision_score, igg_recall_score, igg_f1_score \
            = calculate_precision_recall_f1_score_for_igg(actual_abundance_by_igg_id, igg_file)
        result_rows.append(
            ['igg', reads_name, igg_precision_score, igg_recall_score, igg_f1_score])

    with open(os.getcwd() + f'/precision_recall_scores_lenient.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['tool_name', 'reads_name', 'precision', 'recall', 'f1_score'])
        writer.writerows(result_rows)


def calculate_precision_recall_f1_score_for_metaphlan(actual_abundance_by_ncbi, metaphlan_file):
    metaphlan_abundances_by_species = get_clade_abundances_by_species_id_for_metaphlan_tsv(metaphlan_file)

    truth_labels = list(actual_abundance_by_ncbi.keys())
    pred_labels = list(metaphlan_abundances_by_species.keys())

    return calculate_precision_recall_f1_score(pred_labels, truth_labels)


def calculate_precision_recall_f1_score_for_igg(actual_abundance_by_igg_id, igg_file):
    igg_abundances_by_species = get_clade_abundances_by_species_id_for_igg_tsv(igg_file)

    truth_labels = list(actual_abundance_by_igg_id.keys())
    pred_labels = list(igg_abundances_by_species.keys())

    return calculate_precision_recall_f1_score(pred_labels, truth_labels)


def calculate_precision_recall_f1_score(pred_labels, truth_labels):
    mlb = MultiLabelBinarizer()
    [truth_values, pred_values] = mlb.fit_transform([truth_labels, pred_labels])

    the_precision_score = precision_score(truth_values, pred_values)
    the_recall_score = recall_score(truth_values, pred_values)
    the_f1_score = f1_score(truth_values, pred_values)

    return the_precision_score, the_recall_score, the_f1_score


if __name__ == "__main__":
    main(sys.argv[1:])
