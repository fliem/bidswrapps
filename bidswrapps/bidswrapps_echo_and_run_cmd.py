#! /usr/bin/env python
import subprocess
import sys


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


def echo_and_run_cmd(cmd, tree_dir=""):
    """
    Run cmd. If error is returned, tree tree_dir (if specified)
    """
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
        print(stdout)
    print("[COMMAND]:\n'%s' " % cmd)
    return ret


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        sys.exit(Usage())
    cmd = ' '.join(sys.argv[1:])
    sys.exit(echo_and_run_cmd(cmd))
