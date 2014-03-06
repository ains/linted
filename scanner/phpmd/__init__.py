from scanner.abstract_scanner import AbstractScanner
from linted.models import Scanner, ErrorGroup
from django import forms

import collections
import subprocess
import xml.etree.ElementTree as ElementTree


class PHPMDForm(forms.Form):
    RULE_SETS = (
        ('codesize', 'Code Size'),
        ('naming', 'Naming'),
        ('design', 'Design'),
        ('naming', 'Naming'),
        ('unusedcode', 'Unused Code')
    )
    selected_rule_sets = forms.MultipleChoiceField(
        choices=RULE_SETS)


class PHPMDScanner(AbstractScanner):
    def __init__(self, repository_scan, path, excluded_files='', settings=None):
        if settings is None:
            settings = {}

        scanner = Scanner.objects.get(short_name='phpmd')
        super(PHPMDScanner, self).__init__(repository_scan, scanner, path)

        self.excluded_files = excluded_files
        self.settings = settings

    settings_form = PHPMDForm

    @staticmethod
    def get_error_group(error_name):
        error_group_name = 'phpmd.{}'.format(error_name)
        return ErrorGroup.objects.get(name=error_group_name)

    def process_results(self, scan_result):
        root = ElementTree.fromstring(scan_result)
        violation_dict = collections.defaultdict(list)

        for file_node in root.findall('file'):
            file_path = file_node.get('name')

            for violation_node in file_node.findall('violation'):
                start_line = int(violation_node.get('beginline'))
                end_line = int(violation_node.get('endline'))

                rule = violation_node.get('rule')
                error_group = self.get_error_group(rule)

                message = violation_node.text.strip()

                #If we recognise this error group
                if error_group is not None:
                    violation_dict[file_path].append((start_line, end_line, error_group, message))

        self.save_all_violations(violation_dict)

    def run(self):
        try:
            docker_cmd = ['docker', 'run', '-v', '{}:{}:ro'.format(self.path, self.path), 'linted/phpmd']

            subprocess.check_output(docker_cmd + ['phpmd', self.path, 'xml', 'cleancode'])
        except subprocess.CalledProcessError as e:
            #Exit code 2 means scan completed successfully, but there were rule violations
            if e.returncode == 2:
                scan_result = str(e.output)
                self.process_results(scan_result)