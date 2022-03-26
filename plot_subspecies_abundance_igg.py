#!/usr/bin/python

import csv
import glob
import os
import sys

from matplotlib import pyplot as plt
from plot_utils import survey

def main(argv):
    igg_files = glob.glob(os.getcwd() + '/reads*.fq.gz_igg_profile/species_profile.tsv')

    abundances_by_species_by_file = {}
    for igg_file in igg_files:
        abundances_by_species_by_file.update(get_abundances_by_species_name_for_file(igg_file))

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


def get_abundances_by_species_name_for_file(igg_file):
    dir_name = os.path.basename(os.path.dirname(igg_file))
    reads_name = dir_name.split('.')[0]
    abundances_for_file = {}
    with open(igg_file) as tsv:
        for idx, line in enumerate(csv.reader(tsv, dialect="excel-tab")):
            if idx > 0:
                species_name = line[1]
                abundance = float(line[7])
                abundances_for_file.update({species_name: abundance})
    abundances_for_file_name = {reads_name: abundances_for_file}
    return abundances_for_file_name

if __name__ == "__main__":
    main(sys.argv[1:])



















