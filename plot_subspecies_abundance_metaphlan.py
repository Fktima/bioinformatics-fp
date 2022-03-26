#!/usr/bin/python

import csv
import glob
import os
import sys

from matplotlib import pyplot as plt
from plot_utils import survey

def main(argv):
    metaphlan_files = glob.glob(os.getcwd() + '/reads*metaphlan_profile.tsv')

    abundances_by_species_by_file = {}
    for metaphlan_file in metaphlan_files:
        abundances_by_species_by_file.update(get_abundances_by_species_for_file(metaphlan_file))

    species_names = set()
    for reads_name, abundance_by_species in abundances_by_species_by_file.items():
        species_names = species_names.union(abundance_by_species.keys())

    species_names_ordered = list(species_names)
    species_names_ordered.sort()

    results = {}
    for reads_name, abundance_by_species in abundances_by_species_by_file.items():
        results_for_reads = []
        for species_name in species_names_ordered:
            abundance_for_species = abundance_by_species.get(species_name)
            if (abundance_for_species is not None):
                results_for_reads.append(abundance_for_species)
            else:
                results_for_reads.append(0)
        results.update([(reads_name, results_for_reads)])

    survey(results, species_names_ordered)
    plt.show()

def get_abundances_by_species_for_file(metaphlan_file):
    file_name = os.path.basename(metaphlan_file)
    reads_name = file_name.split('.')[0]
    abundances_for_file = {}
    with open(metaphlan_file) as tsv:
        for idx, line in enumerate(csv.reader(tsv, dialect="excel-tab")):
            if len(line) == 4:
                clade_name = line[0]
                if (is_species_level(clade_name)):
                    species_name = clade_name.split('|')[6]
                    abundance = float(line[2])
                    abundances_for_file.update({species_name: abundance})
    abundances_for_file_name = {reads_name: abundances_for_file}
    return abundances_for_file_name

def is_species_level(clade_name):
    return clade_name.count('|') == 6

if __name__ == "__main__":
    main(sys.argv[1:])



















