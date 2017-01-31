import configparser
import datetime
import os


def compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id="",
                    docker_volumes=[], runscript_args="", runscript_cmd=""):
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
    docker_cmd_input_mapping = "{bids_input_folder}:/data/in:ro".format(bids_input_folder=bids_input_folder)
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


def update_config_file(info_dict, input_config_file="~/.gc3/gc3pie.conf", output_config_dir="~/bidswrapps_conf",
                       filename_info=""):
    """
    updates a gc3pie config file with data stored in info_dict
    info_dict = {
        "section1": {"key1.1":"value1.1", "key1.2":"value1.2"},
        "section2": {"key2.1":"value2.1", "key2.2":"value2.2"} }
    """

    import configparser
    config = configparser.ConfigParser()
    config.read(input_config_file)

    for section in info_dict.keys():
        print(section)
        for key, value in info_dict[section].items():
            config[section][key] = value

    ap = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if filename_info:
        ap = "%s_%s"%(filename_info, ap)
    output_conf_file = os.path.join(os.path.expanduser(output_config_dir), "bidswrappsConf_%s.gc3pie.conf" % ap)
    if not os.path.isdir(output_config_dir):
        os.makedirs(output_config_dir)
    with open(output_conf_file, "w") as fi:
        config.write(fi)

    return os.path.abspath(output_conf_file)
