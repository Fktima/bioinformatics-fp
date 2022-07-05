import csv

from clade_abundance import CladeAbundance


def get_clade_abundances_by_species_id_for_metaphlan_tsv(metaphlan_file):
    abundances_for_file = {}
    with open(metaphlan_file) as tsv:
        for idx, line in enumerate(csv.reader(tsv, dialect="excel-tab")):
            if len(line) == 4:
                clade_name = line[0]
                if (is_species_level(clade_name)):
                    species_name = clade_name.split('|')[6]
                    species_id = line[1].split('|')[-1]
                    abundance = float(line[2])
                    abundances_for_file.update({species_id: CladeAbundance(species_id, species_name, abundance)})
    return abundances_for_file


def is_species_level(clade_name):
    return clade_name.count('|') == 6
