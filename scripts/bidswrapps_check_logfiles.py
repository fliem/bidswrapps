#! /usr/bin/env python

import argparse
import os
from glob import glob
from bidswrapps.bidswrapps_echo_and_run_cmd import print_stars

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checks bidsapps logfiles')
    parser.add_argument('logfiles_dir',nargs='*',default=os.getcwd(),
                        help='The directory with the bidsapps logfile folders. Default: current directory')
    args = parser.parse_args()

    os.chdir(os.path.abspath(args.logfiles_dir))

    files = glob("*/*.log")
    good = []
    bad = []

    for f in files:
        with open(f) as fi:
            status = fi.readline()

        jobname = f.split(os.sep)[0]

        if status.startswith("[ok]"):
            good.append(jobname)
        else:
            bad.append(jobname)

    print_stars()
    print("ok jobs", good)
    print_stars()
    print("bad jobs", bad)
    print_stars()
    print_stars()

    print("%s ok jobs" % len(good))
    print("%s bad jobs" % len(bad))
