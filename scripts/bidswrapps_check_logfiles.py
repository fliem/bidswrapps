#! /usr/bin/env python

import argparse
import os
from glob import glob
from bidswrapps.bidswrapps_echo_and_run_cmd import print_stars

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checks bidsapps logfiles')
    parser.add_argument('logfiles_dir', nargs='*', default=os.getcwd(),
                        help='The directory with the bidsapps logfile folders. Default: current directory')
    args = parser.parse_args()

    log_dir = os.path.abspath(args.logfiles_dir)
    os.chdir(log_dir)

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

    info_file = os.path.join(log_dir, ".session_path")
    if os.path.exists(info_file):
        with open(info_file) as fi:
            session_path = fi.read()
        if os.path.isdir(session_path):
            print("Session path is {}".format(session_path))
            cmd = "gstat -s {session_path} -v -u -l failed".format(session_path)
            print("Checking for failed jobs {}\n Check for jobs that have something other that TERMINATED... at "
                  "Info".format(cmd))

            os.system(cmd)
        else:
            print("Session path not found. Skipping gstat {}".format(session_path))


    else:
        print("session_path file {} in log dir not foud. Skipping gstat.".format(info_file))
