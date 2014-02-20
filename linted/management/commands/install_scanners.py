import os
import subprocess

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Builds dockerfiles for ENABLED_SCANNERS'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        for scanner_name in settings.ENABLED_SCANNERS:
            scanner_path = os.path.join(settings.PROJECT_ROOT, 'scanner', scanner_name)

            docker_command = ['docker', 'build']
            docker_image_name = 'linted/{}'.format(scanner_name)
            try:
                subprocess.check_output(docker_command + ['-t', docker_image_name, scanner_path])
            except subprocess.CalledProcessError as e:
                print("Failed to build Dockerfile for: {} with Return Code: {}".format(scanner_name, e.returncode))
                print("Build Output:")
                print(e.output)