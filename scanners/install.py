import os
import subprocess
import json

from django.conf import settings
from linted.models import ErrorGroup


def install_scanner(scanner_name):
    scanner_path = os.path.join(settings.PROJECT_ROOT, 'scanners', scanner_name)

    #Install scanner docker image
    docker_command = ['docker', 'build']
    docker_image_name = 'linted/{}'.format(scanner_name)
    try:
        subprocess.check_output(docker_command + ['-t', docker_image_name, scanner_path])
    except subprocess.CalledProcessError as e:
        print("Failed to build Dockerfile for: {} with Return Code: {}".format(scanner_name, e.returncode))
        print("Build Output:")
        print(e.output)

    #Import scanner error groups
    with open(os.path.join(scanner_path, 'error_groups.json')) as error_group_file:
        error_group_data = json.loads(error_group_file.read())
        for error_group in error_group_data["error_groups"]:
            namespaced_group_name = "{}/{}".format(scanner_name, error_group["name"])
            ErrorGroup(name=namespaced_group_name, description=error_group["description"]).save()