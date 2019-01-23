# [WIP] BIDSWRAPPS: BIDS APPS IN THE CLOUD

Bidswrapps is a work-in-progress wrapper to submit
[BIDS Apps](http://bids-apps.neuroimaging.io)
to cloud systems, like the
[UZH's Science cloud](https://www.s3it.uzh.ch/en/scienceit/infrastructure/sciencecloud.html),
or [AWS](https://aws.amazon.com), via
[GC3Pie](https://gc3pie.readthedocs.io/en/master/).

The data has to be organized according to the
[BIDS standard](http://bids.neuroimaging.io)
For the participant-level, processing is submitted to execution
instances in parallel.


## Reqirements
- Distributed file system (e.g., NFS; the example below assumes that
the NFS is available at <nfs_ip> and the data is stored at /srv/nfs.
- A private network to access the NFS (the example below assumes this
nework has the address <private_network_ip>.

## Setup

* Install bidswrapps on your submit instance


        pip install git+https://github.com/fliem/bidswrapps


* Update `~/.gc3/gc3pie.conf` so that it includes:

        user_data=#!/bin/sh -x
               cat <<__EOF__ | sudo tee -a /etc/fstab
               <nfs_ip>:/srv/nfs /data.nfs nfs _netdev,auto,x-systemd.automount,x-systemd.device-timeout=1min,x-systemd.idle-timeout=10min 0 0
               __EOF__
               sudo systemctl daemon-reload
               sudo systemctl restart remote-fs.target


Note that **<nfs_ip>** needs to be replaced with the ip of the nfs.

* Optionally, `~/.gc3/gc3pie.conf` can also include default values
for image_id and instance_type.

        bidswrapps_image_id = 65d8edae-024e-4420-bc45-00a744329f60
        bidswrapps_instance_type = 8cpu-32ram-hpc


## Usage

    usage: bidswrapps_start [-h] [-V] [-v] [--config-files CONFIG_FILES] [-r NAME]
                            [-w DURATION] [-s PATH] [-u URL] [-N] [-C NUM]
                            [-J NUM] [-l [STATES]]
                            [-pl PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                            [-pf PARTICIPANT_FILE]
                            [-pel PARTICIPANT_EXCLUSION_LABEL [PARTICIPANT_EXCLUSION_LABEL ...]]
                            [-pef PARTICIPANT_EXCLUSION_FILE]
                            [--volumes VOLUMES [VOLUMES ...]]
                            [--runscript_cmd RUNSCRIPT_CMD] [-ra RUNSCRIPT_ARGS]
                            [--docker_opt DOCKER_OPT] [--no-input-folder-ro]
                            [-o OUTPUT] [-c NUM] [-m GIGABYTES]
                            [--instance_type INSTANCE_TYPE] [--image_id IMAGE_ID]
                            [--dont_wait_for_nfs]
                            [--nfs_search_path NFS_SEARCH_PATH]
                            [--bidswrapps_version]
                            docker_image bids_input_folder bids_output_folder
                            analysis_level

        The ``bidswrapps`` command keeps a record of jobs (submitted, executed
        and pending) in a session file (set name with the ``-s`` option); at
        each invocation of the command, the status of all recorded jobs is
        updated, output from finished jobs is collected, and a summary table
        of all known jobs is printed.

        Options can specify a maximum number of jobs that should be in
        'SUBMITTED' or 'RUNNING' state; ``bidswrapps`` will delay submission of
        newly-created jobs so that this limit is never exceeded.

        This class is called when bidswrapps command is executed.
        Loops through subjects in bids input folder and starts instance


    positional arguments:
      docker_image          Name of docker image to run. If image has no entry
                            point give container name and entry point under ''
                            e.g. 'container:v1 python script.py'
      bids_input_folder     Root location of input data. Note: expects folder in
                            BIDS format.
      bids_output_folder    xxx
      analysis_level        analysis_level: participant: 1st level group: second
                            level. Bids-Apps specs allow for multiple substeps
                            (e.g., group1, group2

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -v, --verbose         Print more detailed information about the program's
                            activity. Increase verbosity each time this option is
                            encountered on the command line.
      --config-files CONFIG_FILES
                            Comma separated list of configuration files
      -r NAME, --resource NAME
                            Submit jobs to a specific computational resources.
                            NAME is a resource name or comma-separated list of
                            such names. Use the command `gservers` to list
                            available resources.
      -w DURATION, --wall-clock-time DURATION
                            Set the time limit for each job; default is 8 hours.
                            Jobs exceeding this limit will be stopped and
                            considered as 'failed'. The duration can be expressed
                            as a whole number followed by a time unit, e.g., '3600
                            s', '60 minutes', '8 hours', or a combination thereof,
                            e.g., '2hours 30minutes'.
      -s PATH, --session PATH
                            Store the session information in the directory at
                            PATH. (Default: '/home/ubuntu/bidswrapps_start'). If
                            PATH is an existing directory, it will be used for
                            storing job information, and an index file (with
                            suffix '.csv') will be created in it. Otherwise, the
                            job information will be stored in a directory named
                            after PATH with a suffix '.jobs' appended, and the
                            index file will be named after PATH with a suffix
                            '.csv' added.
      -u URL, --store-url URL
                            URL of the persistent store to use.
      -N, --new-session     Discard any information saved in the session directory
                            (see '--session' option) and start a new session
                            afresh. Any information about previous jobs is lost.
      -C NUM, --continuous NUM, --watch NUM
                            Keep running, monitoring jobs and possibly submitting
                            new ones or fetching results every NUM seconds. Exit
                            when all jobs are finished.
      -J NUM, --max-running NUM
                            Set the max NUMber of jobs (default: 50) in SUBMITTED
                            or RUNNING state.
      -l [STATES], --state [STATES]
                            Print a table of jobs including their status.
                            Optionally, restrict output to jobs with a particular
                            STATE or STATES (comma-separated list). The pseudo-
                            states `ok` and `failed` are also allowed for
                            selecting jobs in TERMINATED state with exitcode 0 or
                            nonzero, resp.
      -pl PARTICIPANT_LABEL [PARTICIPANT_LABEL ...], --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                            The label of the participant that should be analyzed.
                            The label corresponds to sub-<participant_label> from
                            the BIDS spec (so it does not include "sub-"). If this
                            parameter is not provided all subjects should be
                            analyzed. Multiple participants can be specified with
                            a space separated list.
      -pf PARTICIPANT_FILE, --participant_file PARTICIPANT_FILE
                            A text file with the labels of the participant that
                            should be analyzed. No header; one subject per
                            line.Specs according to --participant_label. If
                            --participant_label and --participant_file are
                            specified, both are used. Note: If -pl or -pf is not
                            specified, analyze all subjects
      -pel PARTICIPANT_EXCLUSION_LABEL [PARTICIPANT_EXCLUSION_LABEL ...], --participant_exclusion_label PARTICIPANT_EXCLUSION_LABEL [PARTICIPANT_EXCLUSION_LABEL ...]
                            The label of the participant that should NOT be
                            analyzed. Multiple participants can be specified with
                            a space separated list.
      -pef PARTICIPANT_EXCLUSION_FILE, --participant_exclusion_file PARTICIPANT_EXCLUSION_FILE
                            A tsv file with the labels of the participant that
                            should not be analyzed, despite being listed in
                            --participant_file.
      --volumes VOLUMES [VOLUMES ...]
                            Additional volumes that should be mounted in the
                            docker call.Shoud be given as
                            /local_path:/path_inside_docker[:permissions],
                            e.g.:/data/project/freesurfer:/freesurfer. Multiple
                            volumes can be specified with a space separated list
      --runscript_cmd RUNSCRIPT_CMD
                            If docker image has now entrypoint, docker execution
                            command can be given here (under ""). E.g.:
                            --docker_exec_cmd "python /code/dosomething.py"
      -ra RUNSCRIPT_ARGS, --runscript_args RUNSCRIPT_ARGS
                            BIDS Apps: add application-specific arguments passed
                            to the runscripts in qotation marks: e.g. "--
                            license_key xx"
      --docker_opt DOCKER_OPT
                            Additional docker options passed to the runscripts in
                            qotation marks: e.g. "--entrypoint=/bin/bash "
      --no-input-folder-ro  don't make input_folder read only. handle with care.
      -o OUTPUT, --output OUTPUT
                            BIDS Apps: local folder where logfiles are copied to
      -c NUM, --cpu-cores NUM
                            Set the number of CPU cores required for each job
                            (default: 1). NUM must be a whole number. NOTE:
                            Parameter is NOT piped into BIDS Apps' n_cpus.
                            Specifiy --n_cpus as -ra
      -m GIGABYTES, --memory-per-core GIGABYTES
                            Set the amount of memory required per execution core;
                            default: 2GB. Specify this as an integral number
                            followed by a unit, e.g., '512MB' or '4GB'. NOTE:
                            Parameter is NOT piped into BIDS Apps' mem_mb.
                            Specifiy --mem_mb as -ra
      --instance_type INSTANCE_TYPE
                            Type of science cloud instance for execution. If none
                            is specified, instance type is determined by config
                            file.
      --image_id IMAGE_ID   Type of science cloud image for execution. If none is
                            specified, image_id is determined by config file.
      --dont_wait_for_nfs   Don't wait for nfs before running docker
      --nfs_search_path NFS_SEARCH_PATH
                            Path that should be waited for. Default:/data.nfs
      --bidswrapps_version  show program's version number and exit

## Example


    screen bidswrapps_start.py \
    bids/tracula:v6.0.0-4 \
    /data.nfs/project/sourcedata /data.nfs/project/derivates/tracula_v6.0.0-4 participant \
    -ra "--license_key ~/fs.key --n_cpus 4" \
    --image_id 40757134-9756-4054-9ec2-8eeaa1d8d677 \
    --instance_type 4cpu-16ram-hpc \
    -s ~/cloudsessions/tracula -o /data.nfs/project/logfiles/tracula \
    -C 15 -c 4
