#! /usr/bin/env python
import subprocess
import sys
import os
import time
import argparse

def runme(command):
    """
    Comodity function to run commands using `subprocess` module
    Input: command to run
    Output: none
    Raise Exception in case command fails
    """
    proc = subprocess.Popen(
        [command],
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE)

    (stdout, stderr) = proc.communicate()
    return (proc.returncode, stdout, stderr)


def print_stars():
    print("********************************")


def Usage():
    print("Usage: bidswrapps_echo_and_run_cmd.py <cmd>")
    print("Echoes and runs command")


def echo_and_run_cmd(cmd, tree_dir="", wait_for_nfs=True, nfs_search_path="/data.nfs"):
    """
    Run cmd. If error is returned, tree tree_dir (if specified)
    """
    out_list = []
    if wait_for_nfs:
        nfs_found = False
        wait_time = 10
        timeout = 200
        count_time = 0
        out_list.append("Looking for {} ...".format(nfs_search_path))
        while (not nfs_found) and (count_time < timeout):
            if os.path.isdir(nfs_search_path):
                nfs_found=True
                out_list.append("{} found. Start computing...".format(nfs_search_path))
            else:
                out_list.append("{} not found. Waiting for {} seconds...".format(nfs_search_path, wait_time))
                time.sleep(wait_time)
                count_time+= wait_time
        if not nfs_found:
            print("[failed]")
            print("\n".join(out_list))
            raise Exception("NFS {} could not be mounted. Abort.".format(nfs_search_path))

    (ret, stdout, stderr) = runme(cmd)

    # format byte return
    try:
        stdout = stdout.decode("utf-8")
    except:
        pass
    try:
        stderr = stderr.decode("utf-8")
    except:
        pass

    if ret != 0:
        print("[failed]")
        print_stars()
        print("\n".join(out_list))
        print_stars()
        print("[failed]:\n%s" % cmd)
        print("Execution failed with exit code: %d" % ret)
        print_stars()
        print("Output message:\n%s" % stdout)
        print_stars()
        print("Error message:\n%s" % stderr)
        print_stars()
        if tree_dir:
            print(runme("tree --charset unicode %s" % tree_dir))

    else:
        print("[ok]")
        print_stars()
        print("[ok]:\n%s \n" % cmd)
        print_stars()
        print("Output message:\n%s" % stdout)
        print_stars()
        print("Error message:\n%s" % stderr)
        print_stars()
    print("[COMMAND]:\n'%s' " % cmd)
    return ret


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--cmd', required=True, nargs="+")
    parser.add_argument("--dont_wait_for_nfs", help="Don't wait for nfs before running docker", dest="wait_for_nfs",
                   action='store_false', default=True)
    parser.add_argument("--nfs_search_path", help="Path that should be waited for. Default:/data.nfs",
                   default="/data.nfs")
    args = parser.parse_args()

    cmd = ' '.join(args.cmd)
    sys.exit(echo_and_run_cmd(cmd, "", args.wait_for_nfs, args.nfs_search_path))
