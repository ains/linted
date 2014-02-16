from scanner.abstract_scanner import AbstractScanner
from linted.models import Scanner, ErrorGroup

import subprocess
import xml.etree.ElementTree as ElementTree


class PHPMDScanner(AbstractScanner):
    def __init__(self, repository_scan, path, excluded_files='', settings={}):
        scanner = Scanner.objects.get(short_name='phpmd')
        super(PHPMDScanner, self).__init__(repository_scan, scanner, path)

        self.excluded_files = excluded_files
        self.settings = settings

    @staticmethod
    def get_error_group(error_name):
        error_group_name = 'phpmd.{}'.format(error_name)
        return ErrorGroup.objects.get(name=error_group_name)

    def process_results(self, scan_result):
        root = ElementTree.fromstring(scan_result)

        for file_node in root.findall('file'):
            file_path = file_node.get('name')

            for violation_node in file_node.findall('violation'):
                start_line = int(violation_node.get('beginline'))
                end_line = int(violation_node.get('endline'))

                rule = violation_node.get('rule')
                error_group = self.get_error_group(rule)

                #If we recognise this error group
                if error_group is not None:
                    self.save_violation(error_group, file_path, start_line, end_line)

    def run(self):
        try:
            subprocess.check_output(['phpmd', self.path, 'xml', 'cleancode'])
        except subprocess.CalledProcessError as e:
            #Exit code 2 means scan completed successfully, but there were rule violations
            if e.returncode == 2:
                scan_result = str(e.output)
                self.process_results(scan_result)