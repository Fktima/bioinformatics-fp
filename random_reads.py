#!/usr/bin/python

import sys
import getopt
# import numpy as np
# import matplotlib.pyplot as plt
# import prettyplotlib as ppl
import subprocess
# import seaborn as sns
# from matplotlib.backends.backend_pdf import PdfPages
# from matplotlib.pyplot import *
# from pylab import *


# from BrewerColors import *


def main(argv):
    # get options passed at command line
    try:
        opts, args = getopt.getopt(argv, "", ["ref_file_path="])
    except getopt.GetoptError:
        # print helpString
        sys.exit(2)

    # num reads, coverage, read length

    for opt, arg in opts:
        if opt == '--ref_file_path':
            ref_file_path = arg

    coverage_list = [4, 5, 6, 7]
    read_length_list = range(25, 301, 25)

    for read_length in read_length_list:
        for coverage in coverage_list:
            subprocess.run([
                "/Users/fatemehkamalvand/javad/bbmap/randomreads.sh",
                "-Xmx4G",
                f"ref={ref_file_path}",
                f'out=reads_rl-{read_length}_c-{coverage}.fq.gz',
                "reads=100000",
                f"coverage={coverage}",
                "minlength=100",
                "maxlength=100",
                f"length={read_length}",
                "maxq=50 midq=30 minq=10 snprate=0.02 insrate=0.02 subrate=0.02 nrate=0.02 maxns=10 metagenome",
            ])


if __name__ == "__main__":
    main(sys.argv[1:])



















