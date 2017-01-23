
def compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id="",
                    docker_volumes=[], runscript_args="", runscript_cmd=""):
    """
    compiles docker command:
    "docker run -v <bids_input_folder>:/data/in -v <bids_output_folder>:/data/out -v \
    [-v additional_docker_volumes:additional_docker_mounts] \
    docker_image [runscript_cmd] /data/in /data/out <analysis_level> [--participant_label <participant_label>] \
    [runscript_args]
    """

    # fixme add ro again, after dcm2niix release
    # docker_cmd_input_mapping = "{bids_input_folder}:/data/in:ro".format(bids_input_folder=bids_input_folder)
    docker_cmd_input_mapping = "{bids_input_folder}:/data/in".format(bids_input_folder=bids_input_folder)
    docker_cmd_output_mapping = "{bids_output_folder}:/data/out".format(bids_output_folder=bids_output_folder)
    docker_mappings = "-v %s -v %s" % (docker_cmd_input_mapping, docker_cmd_output_mapping)

    additional_volumes = " -v ".join([""] + docker_volumes)
    if additional_volumes:
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
