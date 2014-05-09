from scanners.abstract_scanner import AbstractScanner
from linted.models import Scanner, ErrorGroup
from scanners.php.mixin import XmlConfigureMixin

from django import forms

import os
import collections
import subprocess
import json
import lxml.builder as builder
import lxml.etree


class PHPCSForm(forms.Form):
    AVAILABLE_STANDARDS = (
        ('Zend', 'Zend'),
        ('PEAR', 'Pear'),
        ('PSR2', 'PSR2'),
        ('PSR1', 'PSR1'),
        ('PHPCS', 'PHPCS'),
        ('Squiz', 'Squiz')
    )

    standard = forms.ChoiceField(widget=forms.RadioSelect, choices=AVAILABLE_STANDARDS)
    minimum_severity = forms.IntegerField()


class PHPCSScanner(AbstractScanner, XmlConfigureMixin):
    def __init__(self, repository_scan, path, excluded_files='', settings=None):
        scanner = Scanner.objects.get(short_name='phpcs')
        self.excluded_files = excluded_files

        super(PHPCSScanner, self).__init__(repository_scan, scanner, path, settings)


    settings_form = PHPCSForm

    @property
    def ruleset_file(self):
        return os.path.join(self.path, 'phpcs_ruleset.xml')

    def configure(self):
        E = builder.ElementMaker()

        root = E.ruleset(name='Generated Ruleset')

        config = self.settings.get_scanner_config()
        ruleset_xml = self.build_xml_config(root, [config['standard']])

        with open(self.ruleset_file, 'w+') as f:
            f.write(lxml.etree.tostring(ruleset_xml, pretty_print=True))

    @staticmethod
    def get_error_group(error_name):
        error_group_name = 'php/phpcs/{}'.format(error_name)
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
            docker_volume = '{}:{}:ro'.format(self.path, self.path)
            docker_cmd = ['docker', 'run', '-v', docker_volume, 'linted/phpcs']

            standard = self.ruleset_file if self.settings is not None else 'PSR2'
            scan_standard = '--standard={}'.format(standard)

            scan_cmd = docker_cmd + ['phpcs', '--report=json', scan_standard, self.path]
            subprocess.check_output(scan_cmd)

        except subprocess.CalledProcessError as e:
            #PHPCS returns error code 1 when violations are found
            if e.returncode == 1:
                self.process_results(e.output)

            pass