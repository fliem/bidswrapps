from bidswrapps.utils import compile_run_cmd


def test_basic():
    """test basic bids app use case"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = ""
    docker_volumes = []
    runscript_args = ""
    runscript_cmd = ""
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out testorg/testim:dev /data/in " \
                  "/data/out participant"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)


def test_basic_group():
    """test basic bids app group use case"""
    analysis_level = "group"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = ""
    docker_volumes = []
    runscript_args = ""
    runscript_cmd = ""
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out testorg/testim:dev /data/in " \
                  "/data/out group"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)


def test_basic_group_noro():
    """test basic bids app group use case withou input ro"""
    analysis_level = "group"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = ""
    docker_volumes = []
    runscript_args = ""
    runscript_cmd = ""
    input_ro=False
    correct_cmd = "docker run -v /bids_in_data:/data/in -v /bids_out_data:/data/out testorg/testim:dev /data/in " \
                  "/data/out group"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd,\
          input_ro=input_ro)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)



def test_additional_vols():
    """test additional mount vol use case"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = ""
    docker_volumes = ["/project/vol1:/data/vol1", "/project/vol2:/data/vol2"]
    runscript_args = ""
    runscript_cmd = ""
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out -v /project/vol1:/data/vol1 " \
                  "-v /project/vol2:/data/vol2 testorg/testim:dev /data/in " \
                  "/data/out participant"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)


def test_participant_label():
    """test participant label"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = "sub-11"
    docker_volumes = []
    runscript_args = ""
    runscript_cmd = ""
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out testorg/testim:dev /data/in " \
                  "/data/out participant --participant_label sub-11"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)

def test_multiple_participant_labels():
    """test multiple participant labels"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = ["sub-11", "sub-12"]
    docker_volumes = []
    runscript_args = ""
    runscript_cmd = ""
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out testorg/testim:dev /data/in " \
                  "/data/out participant --participant_label sub-11 sub-12"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)

def test_runscript_args():
    """test runscript args"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = ""
    docker_volumes = []
    runscript_args = "--testarg1 a --testarg2 b"
    runscript_cmd = ""
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out testorg/testim:dev " \
                  "/data/in /data/out participant --testarg1 a --testarg2 b"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)

def test_runscript_cmd():
    """test runscript cmd"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = ""
    docker_volumes = []
    runscript_args = ""
    runscript_cmd = "python run.py"
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out testorg/testim:dev " \
                  "python run.py /data/in /data/out participant"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)


def test_full_cmd():
    """test full cmd"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = "sub-11"
    docker_volumes = ["/project/vol1:/data/vol1", "/project/vol2:/data/vol2"]
    runscript_args = "--testarg1 a --testarg2 b"
    runscript_cmd = "python run.py"
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out -v /project/vol1:/data/vol1 " \
                  "-v /project/vol2:/data/vol2 testorg/testim:dev " \
                  "python run.py /data/in /data/out participant --participant_label sub-11 --testarg1 a --testarg2 b"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)



def test_docker_options():
    """test full cmd"""
    analysis_level = "participant"
    bids_input_folder = "/bids_in_data"
    bids_output_folder = "/bids_out_data"
    docker_image = "testorg/testim:dev"
    subject_id = "sub-11"
    docker_volumes = ["/project/vol1:/data/vol1", "/project/vol2:/data/vol2"]
    runscript_args = "--testarg1 a --testarg2 b"
    runscript_cmd = "python run.py"
    docker_opt = "--entrypoint=/bin/bash"
    correct_cmd = "docker run -v /bids_in_data:/data/in:ro -v /bids_out_data:/data/out -v /project/vol1:/data/vol1 " \
                  "-v /project/vol2:/data/vol2 --entrypoint=/bin/bash testorg/testim:dev " \
                  "python run.py /data/in /data/out participant --participant_label sub-11 --testarg1 a --testarg2 b"

    cmd = compile_run_cmd(analysis_level, bids_input_folder, bids_output_folder, docker_image, subject_id,
                          docker_volumes=docker_volumes, runscript_args=runscript_args, runscript_cmd=runscript_cmd,
                          docker_opt=docker_opt)

    assert cmd == correct_cmd, "cmd:\n%s\n does not macht correct cmd:\n%s"%(cmd, correct_cmd)
