from fabric.api import task, env

from .docker import run


@task
def migrations(app=""):

    run("python ./manage.py makemigrations {}".format(app))
