from fabric.api import task, env, run as fab_run


@task
def run(cmd, container=None):
    """
    Runs shell command inside project directory.
    """

    cd = False

    if not container:
        container = env.DOCKER_CONTAINER
        cd = True

    cmd = "cd {}; {} {}".format(env.PROJECT_DIR if cd else "", cmd, env.RUN_PARAMS if "manage.py" in cmd else "")

    return fab_run("docker exec -it {} bash -c '{}'".format(container, cmd))
