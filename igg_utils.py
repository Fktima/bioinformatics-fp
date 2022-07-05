import csv

from clade_abundance import CladeAbundance


def get_clade_abundances_by_species_id_for_igg_tsv(igg_file):
    abundances_for_file = {}
    with open(igg_file) as tsv:
        for idx, line in enumerate(csv.reader(tsv, dialect="excel-tab")):
            if idx > 0:
                species_id = line[0]
                species_name = line[1]
                abundance = float(line[7])
                abundances_for_file.update({species_id: CladeAbundance(species_id, species_name, abundance)})
    return abundances_for_file
