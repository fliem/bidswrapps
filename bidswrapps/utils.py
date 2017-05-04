import datetime
import os
import stat
import sys

import gc3libs
from bids.grabbids import BIDSLayout
from gc3libs import MB, Application
from gc3libs.cmdline import SessionBasedScript, positive_int
from gc3libs.quantity import Memory, GB
from pkg_resources import resource_filename, Requirement

from bidswrapps import __version__


def compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id="",
                    docker_volumes=[], runscript_args="", runscript_cmd="", input_ro=True):
    """
    compiles docker command:
    "docker run -v <bids_input_folder>:/data/in -v <bids_output_folder>:/data/out -v \
    [-v additional_docker_volumes:additional_docker_mounts] \
    docker_image [runscript_cmd] /data/in /data/out <analysis_level> [--participant_label <participant_label>] \
    [runscript_args]
    """

    if isinstance(subject_id, list):
        # for multiple subjects pass as space sep list
        subject_id = " ".join(subject_id)

    # fixme add ro again, after dcm2niix release
    # docker_cmd_input_mapping = "{bids_input_folder}:/data/in:ro".format(bids_input_folder=bids_input_folder)
    if input_ro:
        ro_str = ":ro"
    else:
        ro_str = ""

    docker_cmd_input_mapping = "{bids_input_folder}:/data/in{ro_str}".format(bids_input_folder=bids_input_folder,
                                                                             ro_str=ro_str)
    docker_cmd_output_mapping = "{bids_output_folder}:/data/out".format(bids_output_folder=bids_output_folder)
    docker_mappings = "-v %s -v %s" % (docker_cmd_input_mapping, docker_cmd_output_mapping)

    if docker_volumes:
        additional_volumes = " -v ".join([""] + docker_volumes)
        docker_mappings += additional_volumes
    docker_cmd = "docker run {docker_mappings} {docker_image}".format(docker_mappings=docker_mappings,
                                                                      docker_image=docker_image)
    if runscript_cmd:
        docker_cmd += " %s" % runscript_cmd

    wf_cmd = " /data/in /data/out {analysis_level}".format(analysis_level=analysis_level)

    if subject_id:
        wf_cmd += " --participant_label {subject_id}".format(subject_id=subject_id)

    if runscript_args:
        wf_cmd += " {runscript_args}".format(runscript_args=runscript_args)

    cmd = "{docker_cmd}{wf_cmd}".format(docker_cmd=docker_cmd, wf_cmd=wf_cmd)

    return cmd



## custom application class

DEFAULT_CORES = 2
DEFAULT_MEMORY = Memory(4000, MB)
DEFAULT_REMOTE_INPUT_FOLDER = "./"
DEFAULT_REMOTE_OUTPUT_FOLDER = "./output"


class BidsWrappsApplication(Application):
    """
    """
    application_name = 'bidswrapps'

    def __init__(self,
                 analysis_level,
                 subject_id,
                 bids_input_folder,
                 bids_output_folder,
                 docker_image,
                 runscript_cmd="",
                 runscript_args="",
                 docker_volumes=[],
                 input_ro=True,
                 **extra_args):
        self.output_dir = []

        inputs = dict()
        outputs = dict()
        self.output_dir = extra_args['output_dir']

        script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        wrapper = resource_filename(Requirement.parse("bidswrapps"), 'bidswrapps/bidswrapps_echo_and_run_cmd.py')
        inputs[wrapper] = os.path.basename(wrapper)

        cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                              docker_volumes, runscript_args, runscript_cmd, input_ro)

        Application.__init__(self,
                             arguments="python ./%s %s" % (inputs[wrapper], cmd),
                             inputs=inputs,
                             outputs=[DEFAULT_REMOTE_OUTPUT_FOLDER],
                             stdout='bidswrapps.log',
                             join=True,
                             **extra_args)


        #


"""
Based on https://github.com/uzh/gc3pie/blob/master/gc3apps/inapic/gtrac.py
by Sergio Maffioletti (https://github.com/smaffiol)
"""


class BidsWrappsScript(SessionBasedScript):
    """

    The ``bidswrapps`` command keeps a record of jobs (submitted, executed
    and pending) in a session file (set name with the ``-s`` option); at
    each invocation of the command, the status of all recorded jobs is
    updated, output from finished jobs is collected, and a summary table
    of all known jobs is printed.

    Options can specify a maximum number of jobs that should be in
    'SUBMITTED' or 'RUNNING' state; ``gnift`` will delay submission of
    newly-created jobs so that this limit is never exceeded.

    This class is called when bidswrapps command is executed.
    Loops through subjects in bids input folder and starts instance
    """

    def __init__(self):
        SessionBasedScript.__init__(
            self,
            version=__version__,  # module version == script version
            application=BidsWrappsApplication,
            stats_only_for=BidsWrappsApplication,
        )

    def setup_args(self):
        self.add_param("docker_image", type=str, help="Name of docker image to run. \n\n"
                                                      "If image has no entry point give container name and entry "
                                                      "point under '' e.g. 'container:v1 python script.py'")

        self.add_param("bids_input_folder", type=str, help="Root location of input data. Note: expects folder in "
                                                           "BIDS format.")

        self.add_param("bids_output_folder", type=str, help="xxx")

        self.add_param("analysis_level", type=str,
                       help="analysis_level: participant: 1st level\n"
                            "group: second level. Bids-Apps specs allow for multiple substeps (e.g., group1, group2")

    def setup_options(self):
        self.add_param("-pl", "--participant_label",
                       help='The label of the participant that should be analyzed. The label '
                            'corresponds to sub-<participant_label> from the BIDS spec '
                            '(so it does not include "sub-"). If this parameter is not '
                            'provided all subjects should be analyzed. Multiple '
                            'participants can be specified with a space separated list.',
                       nargs="+")
        self.add_param("-pf", "--participant_file",
                       help='A text file with the labels of the participant that should be analyzed. No header; one '
                            'subject per line.'
                            'Specs according to --participant_label. If --participant_label and --participant_file '
                            'are specified, both are used. Note: If -pl or -pf is not specified, analyze all subjects')
        self.add_param("-pel", "--participant_exclusion_label",
                       help='The label of the participant that should NOT be analyzed. Multiple '
                            'participants can be specified with a space separated list.',
                       nargs="+")
        self.add_param("-pef", "--participant_exclusion_file",
                       help='A tsv file with the labels of the participant that should not be analyzed, '
                            'despite being listed in --participant_file.')
        self.add_param("--volumes", help="Additional volumes that should be mounted in the docker call."
                                         "Shoud be given as /local_path:/path_inside_docker[:permissions], e.g.:"
                                         "/data/project/freesurfer:/freesurfer. "
                                         "Multiple volumes can be specified with a space separated list", nargs="+")

        self.add_param("--runscript_cmd", help='If docker image has now entrypoint, docker execution '
                                               'command can be given here (under ""). '
                                               'E.g.: --docker_exec_cmd "python /code/dosomething.py')
        self.add_param("-ra", "--runscript_args", type=str, dest="runscript_args", default=None,
                       help='BIDS Apps: add application-specific arguments '
                            'passed to the runscripts in qotation marks: '
                            'e.g. \"--license_key xx\" ')

        self.add_param('--no-input-folder-ro', help="don't make input_folder read only. handle with care.",
                            default=True, dest="input_ro", action='store_false')

        # Overwrite script input options to get more specific help
        self.add_param("-o", "--output", type=str, dest="output", default=None,
                       help="BIDS Apps: local folder where logfiles are copied to")

        self.add_param("-c", "--cpu-cores", dest="ncores",
                       type=positive_int, default=1,  # 1 core
                       metavar="NUM",
                       help="Set the number of CPU cores required for each job"
                            " (default: %(default)s). NUM must be a whole number.\n"
                            " NOTE: Parameter is NOT piped into BIDS Apps' n_cpus. Specifiy --n_cpus as -ra")

        self.add_param("-m", "--memory-per-core", dest="memory_per_core",
                       type=Memory, default=2 * GB,  # 2 GB
                       metavar="GIGABYTES",
                       help="Set the amount of memory required per execution core;"
                            " default: %(default)s. Specify this as an integral number"
                            " followed by a unit, e.g., '512MB' or '4GB'."
                            " NOTE: Parameter is NOT piped into BIDS Apps' mem_mb. Specifiy --mem_mb as -ra")

        self.add_param("--instance_type", type=str, dest="instance_type",
                       help="Type of science cloud instance for execution. If none is specified, "
                            "instance type is determined by config file.")
        self.add_param("--image_id", type=str, dest="image_id",
                       help="Type of science cloud image for execution. If none is specified, "
                            "image_id is determined by config file.")

    def pre_run(self):
        """
        If instance_type or image_id are specified in the command line,
        override config file settings.
        """
        SessionBasedScript.pre_run(self)
        if self.params.instance_type:
            self._core.resources['S3ITSC'].bidswrapps_instance_type = self.params.instance_type
        if self.params.image_id:
            self._core.resources['S3ITSC'].bidswrapps_image_id = self.params.image_id

    def get_subject_list(self):
        """
        build subject list form either input arguments (participant_label, participant_file) or
        (if participant_label and participant_file are not specified) input data in bids_input_folder,
        then remove subjects form list according to participant_exclusion_file (if any)
        """
        subject_list = []

        def read_subject_list(list_file):
            "reads text file with subject id per line and returns as list"
            with open(list_file) as fi:
                l = fi.read().strip().split("\n")
            return [s.strip() for s in l]

        def get_input_subjects(bids_input_folder):
            """
            """
            layout = BIDSLayout(bids_input_folder)
            return layout.get_subjects()

        if self.params.participant_label:
            clean_list = [s.strip() for s in self.params.participant_label]
            subject_list += clean_list

        if self.params.participant_file:
            subject_list += read_subject_list(self.params.participant_file)

        if not subject_list:
            subject_list = get_input_subjects(self.params.bids_input_folder)

        # force unique
        subject_list = list(set(subject_list))

        subject_exclusion_list = []
        if self.params.participant_exclusion_label:
            clean_list = [s.strip() for s in self.params.participant_exclusion_label]
            subject_exclusion_list += clean_list

        if self.params.participant_exclusion_file:
            subject_exclusion_list += read_subject_list(self.params.participant_exclusion_file)

        for exsub in subject_exclusion_list:
            if exsub in subject_list:
                subject_list.remove(exsub)
            else:
                gc3libs.log.warning("Subject on exclusion list, but not in inclusion list: %s" % exsub)
        return subject_list

    def create_output_folder(self):
        """
        create output folder and check permission (others need write permission)
        Riccardo: on the NFS filesystem, `root` is remapped transparently to user
        `nobody` (this is called "root squashing"), which cannot write on the
        `/data/nfs` directory owned by user `ubuntu`.
        """
        if not os.path.exists(self.params.bids_output_folder):
            os.makedirs(self.params.bids_output_folder)
            # add write perm for others
            os.chmod(self.params.bids_output_folder,
                     os.stat(self.params.bids_output_folder).st_mode | stat.S_IWOTH)

        # check if output folder has others write permission
        if not os.stat(self.params.bids_output_folder).st_mode & stat.S_IWOTH:
            raise OSError("BIDS output folder %s \nothers need write permission. "
                          "Stopping." % self.params.bids_output_folder)

    def new_tasks(self, extra):
        """
        - Builds subject list (from cmd line args or input folder)
        - Creates output folder
        - If participant level analysis
            For each subject, create one instance of GniftApplication
        - If group level analysis
            For entire study, create one instance of GniftApplication
        """

        tasks = []
        subject_list = self.get_subject_list()
        self.create_output_folder()

        if self.params.analysis_level.startswith("participant"):
            for subject_id in subject_list:
                extra_args = extra.copy()
                extra_args['jobname'] = subject_id
                extra_args['output_dir'] = self.params.output
                extra_args['output_dir'] = extra_args['output_dir'].replace('NAME', '%s' % extra_args['jobname'])

                # mem_mb = self.params.memory_per_core.amount(unit=MB)
                tasks.append(BidsWrappsApplication(
                    self.params.analysis_level,
                    subject_id,
                    self.params.bids_input_folder,
                    self.params.bids_output_folder,
                    self.params.docker_image,
                    self.params.runscript_cmd,
                    self.params.runscript_args,
                    self.params.volumes,
                    self.input_ro,
                    **extra_args))

        elif self.params.analysis_level.startswith("group"):
            extra_args = extra.copy()
            extra_args['jobname'] = self.params.analysis_level
            extra_args['output_dir'] = self.params.output
            extra_args['output_dir'] = extra_args['output_dir'].replace('NAME', '%s' % extra_args['jobname'])
            tasks.append(BidsWrappsApplication(
                self.params.analysis_level,
                subject_list,
                self.params.bids_input_folder,
                self.params.bids_output_folder,
                self.params.docker_image,
                self.params.runscript_cmd,
                self.params.runscript_args,
                self.params.volumes,
                **extra_args))

        return tasks
