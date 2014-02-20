from scanner.abstract_scanner import AbstractScanner
from linted.models import Scanner, ErrorGroup

import collections
import subprocess
import json


class PHPCSScanner(AbstractScanner):
    def __init__(self, repository_scan, path, excluded_files='', settings={}):
        scanner = Scanner.objects.get(short_name='phpcs')
        super(PHPCSScanner, self).__init__(repository_scan, scanner, path)

        self.excluded_files = excluded_files
        self.settings = settings

    @staticmethod
    def get_error_group(error_name):
        error_group_name = 'phpmd.{}'.format(error_name)
        return ErrorGroup.objects.get(name=error_group_name)

    def process_results(self, scan_result):
        decoded_results = json.loads(scan_result)
        violation_dict = collections.defaultdict(list)

        for file_path, file_data in decoded_results['files'].items():
            file_violations = file_data['messages']

            if len(file_violations) > 0:
                for violation in file_violations:
                    start_line = int(violation['line'])
                    end_line = int(violation['line'])
                    message = violation['message']

                    error_group = self.get_error_group(violation['source'])

                    #If we recognise this error group
                    if error_group is not None:
                        violation_dict[file_path].append((start_line, end_line, error_group, message))

        self.save_all_violations(violation_dict)

    def run(self):
        try:
            docker_cmd = ['docker', 'run', '-v', '{}:{}:ro'.format(self.path, self.path), 'linted/phpcs']
            scan_result = subprocess.check_output(docker_cmd + ['phpcs', '--report=json', '--standard=PSR2', self.path])
            self.process_results(scan_result)
        except subprocess.CalledProcessError as e:
            pass