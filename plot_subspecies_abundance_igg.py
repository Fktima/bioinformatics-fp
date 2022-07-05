#!/usr/bin/python

import glob
import os
import sys

from matplotlib import pyplot as plt

from igg_utils import get_clade_abundances_by_species_id_for_igg_tsv
from plot_utils import survey

def main(argv):
    igg_files = glob.glob(os.getcwd() + '/reads*.fq.gz_igg_profile/species_profile.tsv')

    abundances_by_species_id_by_file = {}
    for igg_file in igg_files:
        file_name = os.path.basename(os.path.dirname(igg_file))
        reads_name = file_name.split('.')[0]
        abundances_by_species_id_by_file.update(
            {reads_name: get_clade_abundances_by_species_id_for_igg_tsv(igg_file)}
        )

    abundances_by_species_name_by_file = {
        reads_name: {clade_abundance.name: clade_abundance for clade_abundance in abundance_by_species.values()} for
        reads_name, abundance_by_species in abundances_by_species_id_by_file.items()
    }

    species_names = set()
    for reads_name, abundance_by_species in abundances_by_species_name_by_file.items():
        species_names = species_names.union(abundance_by_species.keys())

    species_names_ordered = list(species_names)
    species_names_ordered.sort()

    results = {}
    for reads_name, abundance_by_species in abundances_by_species_name_by_file.items():
        results_for_reads = []
        for species_name in species_names_ordered:
            abundance_for_species = abundance_by_species.get(species_name)
            if abundance_for_species is not None:
                results_for_reads.append(abundance_for_species.abundance)
            else:
                results_for_reads.append(0)
        results.update([(reads_name, results_for_reads)])

    survey(results, species_names_ordered)
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])



















