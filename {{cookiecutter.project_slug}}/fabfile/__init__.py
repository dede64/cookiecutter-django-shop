from fabric.api import env, local

from .django import *

env.hosts = ["localhost:9009"]
env.use_ssh_config = True
env.run = local

env.PROJECT_DIR = "/var/www/app"
env.DOCKER_CONTAINER = "{{cookiecutter.project_slug}}_webapp"
env.RUN_PARAMS = ""
