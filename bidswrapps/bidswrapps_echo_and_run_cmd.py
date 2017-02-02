#! /usr/bin/env python

import sys

from bidswrapps.utils import echo_and_run_cmd


def Usage():
    print("Usage: bidswrapps_echo_and_run_cmd.py <cmd>")
    print("Echoes and runs command")


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        sys.exit(Usage())
    cmd = ' '.join(sys.argv[1:])
    sys.exit(echo_and_run_cmd(cmd))
