import collections
import subprocess
import os
import xml.etree.ElementTree as ElementTree
import lxml.builder as builder
import lxml.etree

from django import forms
from scanners.abstract_scanner import AbstractScanner
from linted.models import Scanner, ErrorGroup
from scanners.php.mixin import XmlConfigureMixin


class PHPMDForm(forms.Form):
    RULE_SETS = (
        ('cleancode.xml', 'Clean Code'),
        ('codesize.xml', 'Code Size'),
        ('naming.xml', 'Naming'),
        ('design.xml', 'Design'),
        ('unusedcode.xml', 'Unused Code'),
        ('controversial.xlm', 'Controversial')
    )
    selected_rule_sets = forms.MultipleChoiceField(
        choices=RULE_SETS, widget=forms.CheckboxSelectMultiple)


class PHPMDScanner(AbstractScanner, XmlConfigureMixin):
    def __init__(self, repository_scan, path, excluded_files='', settings=None):
        scanner = Scanner.objects.get(short_name='phpmd')
        self.excluded_files = excluded_files

        super(PHPMDScanner, self).__init__(repository_scan, scanner, path, settings)

    settings_form = PHPMDForm

    @staticmethod
    def get_error_group(error_name):
        error_group_name = 'phpmd.{}'.format(error_name)
        return ErrorGroup.objects.get(name=error_group_name)

    @property
    def ruleset_file(self):
        return os.path.join(self.path, 'phpmd_ruleset.xml')

    def configure(self):
        E = builder.ElementMaker(namespace='http://pmd.sf.net/ruleset/1.0.0',
                                 nsmap={
                                     None: 'http://pmd.sf.net/ruleset/1.0.0',
                                     'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                     'schemaLocation': 'http://pmd.sf.net/ruleset_xml_schema.xsd',
                                     'noNamespaceSchemaLocation': 'http://pmd.sf.net/ruleset_xml_schema.xsd'
                                 })
        root = E.ruleset(name='Generated Ruleset')

        config = self.settings.get_scanner_config()
        ruleset_xml = self.build_xml_config(root, config['selected_rule_sets'], 'rulesets/')

        with open(self.ruleset_file, 'w+') as f:
            f.write(lxml.etree.tostring(ruleset_xml, pretty_print=True))

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
            phpmd_command = ['phpmd', self.path, 'xml']

            if self.settings is not None:
                phpmd_command += [self.ruleset_file]
            else:
                phpmd_command += ['codesize,unusedcode,naming']

            subprocess.check_output(docker_cmd + phpmd_command)
        except subprocess.CalledProcessError as e:
            #Exit code 2 means scan completed successfully, but there were rule violations
            if e.returncode == 2:
                scan_result = str(e.output)
                self.process_results(scan_result)
