#!/usr/bin/python

import sys
import subprocess
import glob
import os

def main(argv):
    files = glob.glob(os.getcwd() + '/reads*.fq.gz')

    for f in files:
        # get filename
        fname = os.path.basename(f)

        print(f'Performing metaphlan analysis for {fname}')
        subprocess.run([
            f"metaphlan --input_type fastq --read_min_len 100 {fname} {fname}_metaphlan_profile.tsv"
        ], shell=True)

        print(f'Performing igg search analysis for {fname}')
        subprocess.run([
            f"/Users/fatemehkamalvand/javad/IGGsearch-master/run_iggsearch.py search --strict --m1 {fname} --outdir {fname}_igg_profile"
        ], shell=True)

if __name__ == "__main__":
    main(sys.argv[1:])



















