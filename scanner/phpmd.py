from scanner import Scanner
from linted.models import ErrorGroup

import subprocess
import xml.etree.ElementTree as ElementTree


class Phpmd(Scanner):
    def __init__(self, repository_scan, linter, path, excluded_files='', settings={}):
        Scanner.__init__(self, repository_scan, linter, path)

        self.excluded_files = excluded_files
        self.settings = settings

    def get_error_group(self, error_name):
        prefix = 'phpmd'
        error_group = ErrorGroup.objects.get(name='{}.{}'.format(prefix, error_name))
        return error_group

    def process_results(self, scan_result):
        tree = ElementTree.fromstring(scan_result)
        root = tree.getroot()

        for file in root.findall('file'):
            file_path = file.get('name')
            rel_file_path = self.get_relative_path(file_path)

            for violation in file.findall('violation'):
                start_line = violation.get('beginline')
                end_line = violation.get('endline')

                rule = violation.get('rule')
                error_group = self.get_error_group(rule)

                self.save_violation(error_group, rel_file_path, start_line, end_line)

    def run(self):
        try:
            subprocess.check_output(['phpmd', self.path, 'xml', 'cleancode'])
        except subprocess.CalledProcessError as e:
            #Exit code 2 means scan completed successfully, but there were rule violations
            if e.returncode == 2:
                scan_result = str(e.output)
                self.process_results(scan_result)